import os
import argparse
from itertools import combinations

import numpy as np
import pandas as pd
import bambi as bmb

from ic2_beta_glmm_auto_predictions import (INTERVAL_PROB, LLMS, REPORTS, REPRESENTATIONS, STATISTICS_DIR, load_data,
                                            posterior_predictions, squeeze)


def difference_row(values_a, values_b):
    diff = values_a - values_b
    low, high = np.quantile(diff, [(1 - INTERVAL_PROB) / 2, (1 + INTERVAL_PROB) / 2])
    return {
        "mean": round(float(diff.mean()), 4),
        "median": round(float(np.median(diff)), 4),
        "sd": round(float(diff.std()), 4),
        "eti_low": round(float(low), 4),
        "eti_high": round(float(high), 4),
        "p_greater": round(float((diff > 0).mean()), 4),
    }


def comparison_table(grid, draws, fixed, compared, fixed_levels, compared_levels):
    """All pairs a - b of the compared factor (e.g. representation) within each level of the fixed factor (e.g. llm)."""
    column = {(row.llm, row.representation): i for i, row in enumerate(grid.itertuples(index=False))}
    rows = []
    for level in fixed_levels:
        for a, b in combinations(compared_levels, 2):
            key_a = {fixed: level, compared: a}
            key_b = {fixed: level, compared: b}
            values_a = draws[:, column[(key_a["llm"], key_a["representation"])]]
            values_b = draws[:, column[(key_b["llm"], key_b["representation"])]]
            rows.append({fixed: level, "a": a, "b": b, **difference_row(values_a, values_b)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beta GLMM of the automatic evaluation with pairwise comparisons of the predictions.")
    parser.add_argument('-t', '--type', type=str, required=True, choices=list(REPORTS),
                        help='Evaluation type: m2m or m2t')
    parser.add_argument('-m', '--measure', type=str, required=True,
                        help='Measure: similarity for m2m, relevance or truthfulness for m2t')
    args = parser.parse_args()

    if args.measure not in REPORTS[args.type]:
        parser.error("measure for {} has to be one of: {}".format(args.type, ", ".join(REPORTS[args.type])))

    df = load_data(args.type, args.measure)
    squeezed = ((df["value"] <= 0) | (df["value"] >= 1)).any()
    n = len(df)
    df = squeeze(df)

    model = bmb.Model(
        "value ~ llm * representation + (1|model_name)",
        data=df,
        family="beta"
    )

    results = model.fit(
        draws=5000,
        tune=2000,
        chains=4,
        target_accept=0.95,
        hdi_prob=0.95,
        hdi_kind="eti",
        random_seed=24
    )

    grid, draws = posterior_predictions(model, results, df)
    if squeezed:  # back to the original scale of the values: inverse of squeeze
        draws = (draws * n - 0.5) / (n - 1)

    name = "beta_glmm_{}_{}".format(args.type, args.measure)
    tables = {
        "representation": comparison_table(grid, draws, "llm", "representation", LLMS, REPRESENTATIONS),
        "llm": comparison_table(grid, draws, "representation", "llm", REPRESENTATIONS, LLMS),
    }
    for compared, table in tables.items():
        print(table.to_string(index=False))
        path = os.path.join(STATISTICS_DIR, "{}_comparisons_{}.csv".format(name, compared))
        table.to_csv(path, index=False)
        print("Saved {}".format(path))

    print("Models taken into account: {} ({} rows)".format(df["model_name"].nunique(), len(df)))
