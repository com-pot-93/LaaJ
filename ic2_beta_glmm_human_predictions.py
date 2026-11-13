import os
import json
import math
import statistics

import numpy as np
import pandas as pd
import bambi as bmb
import arviz as az
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
HUMAN_DIR = os.path.join(BASE, "generation", "human")
OUTPUT_DIR = os.path.join(BASE, "evaluation", "human")
NAME = os.path.splitext(os.path.basename(__file__))[0]
REPRESENTATIONS = ["bpmn", "mermaid_js", "simple_json"]
LLMS = ["anthropic", "gemini", "gpt"]
EXAMPLES = ["examples", "no_examples"]  # few-shot with examples / system prompt only (file suffix _no_examples)
SCORE = "score"
MAX_SCORE = 5
FORMULA = "score_scaled ~ llm * representation * example + (1|process_model)"
INTERVAL_PROB = 0.95  # as hdi_prob of the fit


def results_file(representation, llm, example):
    suffix = "" if example == "examples" else "_no_examples"
    return os.path.join(HUMAN_DIR, "{}_{}{}.json".format(representation, llm, suffix))


def load_data():
    """Dataframe with process_model, llm, representation, example and score_scaled (mean llm score over the iterations / 5)
    of the 18 result files, only process models with a score in all 18 combinations."""
    rows = []
    for representation in REPRESENTATIONS:
        for llm in LLMS:
            for example in EXAMPLES:
                with open(results_file(representation, llm, example)) as file:
                    results = json.load(file)
                for use_case, models in results.items():
                    for model, result in models.items():
                        evaluations = [it.get("evaluation") for it in result.get("iterations", {}).values()]
                        scores = [float(e[SCORE]) for e in evaluations
                                  if isinstance(e, dict) and isinstance(e.get(SCORE), (int, float))]
                        if scores:
                            rows.append({
                                "process_model": "{}_{}".format(use_case, model),
                                "llm": llm,
                                "representation": representation,
                                "example": example,
                                "score_scaled": statistics.mean(scores) / MAX_SCORE,
                            })
    df = pd.DataFrame(rows)

    # only process models with a score for every llm, representation and example (18 rows), so that all combinations
    # have the same process models
    combinations = len(REPRESENTATIONS) * len(LLMS) * len(EXAMPLES)
    counts = df.groupby("process_model").apply(
        lambda group: len(set(zip(group["llm"], group["representation"], group["example"]))))
    complete = counts[counts == combinations].index
    incomplete = sorted(set(df["process_model"]) - set(complete))
    if incomplete:
        print("{} process models are not present in all llms, representations and examples and are left out: {}".format(
            len(incomplete), ", ".join(incomplete)))
    return df[df["process_model"].isin(complete)].reset_index(drop=True)


def squeeze(df):
    """The beta distribution is only defined in (0, 1): if there are values of exactly 0 or 1, all values are moved
    slightly into (0, 1) with (value * (n - 1) + 0.5) / n (Smithson & Verkuilen, 2006)."""
    boundary = ((df["score_scaled"] <= 0) | (df["score_scaled"] >= 1)).sum()
    if boundary:
        n = len(df)
        print("{} values of 0 or 1, all values are squeezed into (0, 1)".format(boundary))
        df["score_scaled"] = (df["score_scaled"] * (n - 1) + 0.5) / n
    return df


def fit(df):
    model = bmb.Model(FORMULA, data=df, family="beta")
    results = model.fit(
        draws=5000,
        tune=2000,
        chains=4,
        target_accept=0.95,
        hdi_prob=0.95,
        hdi_kind="eti",
        random_seed=24
    )
    return model, results


def posterior_predictions(model, results, df):
    """Posterior draws (chain * draw, 18) of the mean score_scaled of every llm, representation and example, without
    random effects."""
    grid = pd.DataFrame([(llm, representation, example)
                         for llm in LLMS for representation in REPRESENTATIONS for example in EXAMPLES],
                        columns=["llm", "representation", "example"])
    grid["process_model"] = df["process_model"].iloc[0]  # not used, the group specific effects are left out

    try:  # bambi >= 0.13
        predicted = model.predict(results, data=grid, kind="response_params", inplace=False, include_group_specific=False)
    except (TypeError, ValueError):  # older bambi
        predicted = model.predict(results, data=grid, kind="mean", inplace=False, include_group_specific=False)

    # the predicted mean is the posterior variable over the new observations ("mu", or "score_scaled_mean" in older bambi)
    name = next(var for var in ["mu", "score_scaled_mean"] if var in predicted.posterior)
    draws = predicted.posterior[name].values  # (chain, draw, 18)
    return grid[["llm", "representation", "example"]], draws.reshape(-1, draws.shape[-1])


def prepared_draws():
    """Data, fit and the posterior prediction draws on the scale of score_scaled (squeeze undone)."""
    df = load_data()
    squeezed = ((df["score_scaled"] <= 0) | (df["score_scaled"] >= 1)).any()
    n = len(df)
    df = squeeze(df)
    model, results = fit(df)
    grid, draws = posterior_predictions(model, results, df)
    if squeezed:  # back to the original scale of the values: inverse of squeeze
        draws = (draws * n - 0.5) / (n - 1)
    return df, results, grid, draws


def prediction_table(grid, draws):
    rows = []
    for i, (llm, representation, example) in enumerate(grid.itertuples(index=False)):
        values = draws[:, i]
        # equal tailed interval, as hdi_kind="eti" of the fit
        low, high = np.quantile(values, [(1 - INTERVAL_PROB) / 2, (1 + INTERVAL_PROB) / 2])
        rows.append({
            "llm": llm,
            "representation": representation,
            "example": example,
            "mean": round(float(values.mean()), 4),
            "median": round(float(np.median(values)), 4),
            "sd": round(float(values.std()), 4),
            "eti_low": round(float(low), 4),
            "eti_high": round(float(high), 4),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df, results, grid, draws = prepared_draws()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    parameters = az.summary(results, ci_prob=INTERVAL_PROB, ci_kind="eti")
    print(parameters)
    parameters.to_csv(os.path.join(OUTPUT_DIR, NAME + "_parameters.csv"))

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
    random_sigma = results.posterior["1|process_model_sigma"].mean().item()
    print(f"Process model sigma: {random_sigma:.4f}")
    lower_logit = intercept - 1.96 * random_sigma
    upper_logit = intercept + 1.96 * random_sigma
    lower_mu = 1 / (1 + np.exp(-lower_logit))
    upper_mu = 1 / (1 + np.exp(-upper_logit))
    print("random effect lower", lower_mu)
    print("random effect upper", upper_mu)

    az.plot_trace(
        results,
        var_names=["Intercept"]
    )
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, NAME + "_intercept.svg")
    plt.savefig(plot_path, format="svg")
    plt.close()
    print("Saved {}".format(plot_path))

    predictions = prediction_table(grid, draws)
    print(predictions.to_string(index=False))
    predictions_path = os.path.join(OUTPUT_DIR, NAME + ".csv")
    predictions.to_csv(predictions_path, index=False)
    print("Saved {}".format(predictions_path))

    # posterior means only: llms as rows, <representation>_<example> as columns
    means = predictions.assign(column=predictions["representation"] + "_" + predictions["example"])
    columns = ["{}_{}".format(representation, example) for representation in REPRESENTATIONS for example in EXAMPLES]
    means = means.pivot(index="llm", columns="column", values="mean").reindex(index=LLMS, columns=columns)
    means.columns.name = None
    print(means.to_string())
    means_path = os.path.join(OUTPUT_DIR, NAME + "_mean.csv")
    means.to_csv(means_path)
    print("Saved {}".format(means_path))

    print("Process models taken into account: {} ({} rows)".format(df["process_model"].nunique(), len(df)))
