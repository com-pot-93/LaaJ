import os
from itertools import combinations

import numpy as np
import pandas as pd

from ic2_beta_glmm_human_predictions import EXAMPLES, INTERVAL_PROB, LLMS, OUTPUT_DIR, REPRESENTATIONS, prepared_draws

NAME = os.path.splitext(os.path.basename(__file__))[0]

FACTORS = {"llm": LLMS, "representation": REPRESENTATIONS, "example": EXAMPLES}


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


def comparison_table(grid, draws, compared):
    """All pairs a - b of the levels of the compared factor, within each combination of the levels of the other two factors."""
    column = {tuple(row): i for i, row in enumerate(grid[list(FACTORS)].itertuples(index=False))}
    fixed = [factor for factor in FACTORS if factor != compared]
    rows = []
    for level_1 in FACTORS[fixed[0]]:
        for level_2 in FACTORS[fixed[1]]:
            for a, b in combinations(FACTORS[compared], 2):
                levels = {fixed[0]: level_1, fixed[1]: level_2}
                values_a = draws[:, column[tuple({**levels, compared: a}[f] for f in FACTORS)]]
                values_b = draws[:, column[tuple({**levels, compared: b}[f] for f in FACTORS)]]
                rows.append({**levels, "a": a, "b": b, **difference_row(values_a, values_b)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df, results, grid, draws = prepared_draws()

    for compared in FACTORS:
        table = comparison_table(grid, draws, compared)
        print(table.to_string(index=False))
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path = os.path.join(OUTPUT_DIR, "{}_{}.csv".format(NAME, compared))
        table.to_csv(path, index=False)
        print("Saved {}".format(path))

    print("Process models taken into account: {} ({} rows)".format(df["process_model"].nunique(), len(df)))
