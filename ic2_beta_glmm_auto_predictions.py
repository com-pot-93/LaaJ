import os
import argparse
import math

import numpy as np
import pandas as pd
import bambi as bmb
import arviz as az
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
STATISTICS_DIR = os.path.join(BASE, "similarity", "automatic")
OUTPUT_DIR = os.path.join(BASE, "evaluation", "automatic")
SCRIPT = os.path.splitext(os.path.basename(__file__))[0]
REPRESENTATIONS = ["bpmn", "cpee", "mermaid_js", "simple_json"]
LLMS = ["anthropic", "gemini", "gpt"]
# type -> measure -> report name of a representation and llm
REPORTS = {
    "m2m": {"similarity": "m2m_{}_{}.csv"},
    "m2t": {"relevance": "m2t_{}_{}_relevance.csv", "truthfulness": "m2t_{}_{}_truthfulness.csv"},
}
VALUE_COLUMN = "mean"
INTERVAL_PROB = 0.95  # as hdi_prob of the fit


def load_data(evaluation_type, measure):
    """Dataframe with model_name, llm, representation and value (mean over the iterations) of the 12 reports."""
    frames = []
    for representation in REPRESENTATIONS:
        for llm in LLMS:
            report = pd.read_csv(os.path.join(STATISTICS_DIR, REPORTS[evaluation_type][measure].format(representation, llm)))
            frames.append(pd.DataFrame({
                "model_name": report["file name"],
                "llm": llm,
                "representation": representation,
                "value": report[VALUE_COLUMN],
            }))
    df = pd.concat(frames, ignore_index=True)

    missing = df["value"].isna().sum()
    if missing:
        print("{} rows without a value are left out".format(missing))
    df = df.dropna(subset=["value"])

    # only models with a value for every llm and representation (12 rows), so that all combinations have the same models
    combinations = len(REPRESENTATIONS) * len(LLMS)
    counts = df.groupby("model_name").apply(lambda rows: len(set(zip(rows["llm"], rows["representation"]))))
    complete = counts[counts == combinations].index
    incomplete = sorted(set(df["model_name"]) - set(complete))
    if incomplete:
        print("{} models are not present in all llms and representations and are left out: {}".format(
            len(incomplete), ", ".join(incomplete)))
    return df[df["model_name"].isin(complete)].reset_index(drop=True)


def squeeze(df):
    """The beta distribution is only defined in (0, 1): if there are values of exactly 0 or 1, all values are moved
    slightly into (0, 1) with (value * (n - 1) + 0.5) / n (Smithson & Verkuilen, 2006)."""
    boundary = ((df["value"] <= 0) | (df["value"] >= 1)).sum()
    if boundary:
        n = len(df)
        print("{} values of 0 or 1, all values are squeezed into (0, 1)".format(boundary))
        df["value"] = (df["value"] * (n - 1) + 0.5) / n
    return df


def posterior_predictions(model, results, df):
    """Posterior draws (chain * draw, 12) of the mean value of every llm and representation, without random effects."""
    grid = pd.DataFrame([(llm, representation) for llm in LLMS for representation in REPRESENTATIONS],
                        columns=["llm", "representation"])
    grid["model_name"] = df["model_name"].iloc[0]  # not used, the group specific effects are left out

    try:  # bambi >= 0.13
        predicted = model.predict(results, data=grid, kind="response_params", inplace=False, include_group_specific=False)
    except (TypeError, ValueError):  # older bambi
        predicted = model.predict(results, data=grid, kind="mean", inplace=False, include_group_specific=False)

    # the predicted mean is the posterior variable over the new observations ("mu", or "value_mean" in older bambi)
    name = next(var for var in ["mu", "value_mean"] if var in predicted.posterior)
    draws = predicted.posterior[name].values  # (chain, draw, 12)
    return grid[["llm", "representation"]], draws.reshape(-1, draws.shape[-1])


def prediction_table(grid, draws):
    rows = []
    for i, (llm, representation) in enumerate(grid.itertuples(index=False)):
        values = draws[:, i]
        # equal tailed interval, as hdi_kind="eti" of the fit
        low, high = np.quantile(values, [(1 - INTERVAL_PROB) / 2, (1 + INTERVAL_PROB) / 2])
        rows.append({
            "llm": llm,
            "representation": representation,
            "mean": round(float(values.mean()), 4),
            "median": round(float(np.median(values)), 4),
            "sd": round(float(values.std()), 4),
            "eti_low": round(float(low), 4),
            "eti_high": round(float(high), 4),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beta GLMM of the automatic evaluation with posterior predictions.")
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

    name = "{}_{}_{}".format(SCRIPT, args.type, args.measure)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    parameters = az.summary(results)
    print(parameters)
    parameters.to_csv(os.path.join(OUTPUT_DIR, name + "_parameters.csv"))

    # Posterior mean of the intercept
    intercept = results.posterior["Intercept"].mean().item()

    # Posterior mean of kappa
    kappa = results.posterior["kappa"].mean().item()

    # Convert intercept to expected proportion
    mu = 1 / (1 + np.exp(-intercept))

    # Calculate beta variance
    var = mu * (1 - mu) / (kappa + 1)

    print(f"Mu: {mu:.4f}")
    print(f"Variance: {var:.6f}")
    print(f"SD: {math.sqrt(var):.3f}")
    random_sigma = results.posterior["1|model_name_sigma"].mean().item()
    print(f"Model name sigma: {random_sigma:.4f}")
    lower_logit = intercept - 1.96 * random_sigma
    upper_logit = intercept + 1.96 * random_sigma
    lower_mu = 1 / (1 + np.exp(-lower_logit))
    upper_mu = 1 / (1 + np.exp(-upper_logit))
    print("random effect upper", lower_mu)
    print("random effect lower", upper_mu)

    az.plot_trace(
        results,
        var_names=["Intercept"]
    )
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, name + "_intercept.svg")
    plt.savefig(plot_path, format="svg")
    plt.close()
    print("Saved {}".format(plot_path))

    grid, draws = posterior_predictions(model, results, df)
    if squeezed:  # back to the original scale of the values: inverse of squeeze
        draws = (draws * n - 0.5) / (n - 1)
    predictions = prediction_table(grid, draws)
    print(predictions.to_string(index=False))
    predictions_path = os.path.join(OUTPUT_DIR, name + ".csv")
    predictions.to_csv(predictions_path, index=False)
    print("Saved {}".format(predictions_path))

    # posterior means only: llms as rows, representations as columns
    means = predictions.pivot(index="llm", columns="representation", values="mean").reindex(index=LLMS, columns=REPRESENTATIONS)
    print(means.to_string())
    means_path = os.path.join(OUTPUT_DIR, name + "_mean.csv")
    means.to_csv(means_path)
    print("Saved {}".format(means_path))

    print("Models taken into account: {} ({} rows)".format(df["model_name"].nunique(), len(df)))
