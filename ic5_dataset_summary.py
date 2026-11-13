import os
import json
import glob
import statistics

import pandas as pd
from scipy import stats

from ic12_automatic_average_statistics import LLMS, METRIC_COLUMNS, REPRESENTATIONS, metric_values, read_report, write_csv
from ic3_deterministic_reliability_m2m import ALL, SIM_TYPES, SIMILARITY_FILE, agreement, llm_similarity, p_value
from ic3_deterministic_reliability_m2t import METRICS as TEXT_METRICS, TEXT_SIMILARITY_FILE, llm_metric
from ic3_source_of_difference import AUTOMATIC_DIR, CATEGORIES, EVALUATION_TYPES, count, source_sets
from ic4_m2m_magnitude import ALPHA, METRICS as M2M_METRICS
from ic5_automatic_dataset import CALCULATED, DATASETS, OVERVIEW_COLUMNS, calculated_metrics, dataset_use_cases

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE, "similarity", "dataset")
AVERAGE_FILE = os.path.join(OUTPUT_DIR, "average.csv")
RELIABILITY_FILE = os.path.join(OUTPUT_DIR, "reliability.csv")
SOURCE_OF_DIFFERENCE_FILE = os.path.join(OUTPUT_DIR, "source_of_difference.json")
MAGNITUDE_FILE = os.path.join(OUTPUT_DIR, "magnitude.csv")


def only(series, use_cases):
    return series[series.index.isin(use_cases)]


def average_row(name, use_cases, reports):
    """ic12: mean and cv of the llm metrics (average of the 12 representation and llm rows) and the calculated metrics."""
    rows = [metric_values(representation, llm, use_cases) for representation in REPRESENTATIONS for llm in LLMS]
    row = {"dataset": name}
    for column in METRIC_COLUMNS:
        if column in OVERVIEW_COLUMNS:
            values = [r[column] for r in rows if r[column] != ""]
            row[column] = round(statistics.mean(values), 4) if values else ""
    return {**row, **calculated_metrics(use_cases, reports)}


def reliability_rows(name, use_cases, data):
    """ic3: agreement of the llm with the calculated metrics, only the use cases of the dataset."""
    rows = [agreement(only(data["llm_m2m"], use_cases), data["similarity"][sim_type], sim_type) for sim_type in SIM_TYPES]
    rows += [agreement(only(data["llm_m2t"][metric], use_cases), data["text"][metric], metric) for metric in TEXT_METRICS]
    return [{"dataset": name, "evaluation": "m2m" if row["pair"].split("*")[1] in SIM_TYPES else "m2t", **row}
            for row in rows]


def spearman_test(avg_sim, value_range):
    rho, p_two_sided = stats.spearmanr(avg_sim, value_range)
    _, p_less = stats.spearmanr(avg_sim, value_range, alternative="less")
    return {
        "spearman": round(rho, 4),
        "p_one_sided": p_value(p_less),   # H1: negative relation
        "p_two_sided": p_value(p_two_sided),
        "H0": "rejected" if p_less < ALPHA else "accepted",  # H0: no relation, one-sided test, alpha 0.05
    }


def magnitude_rows(name, use_cases, data):
    """ic4: spearman test of avg_sim and range, m2m (all 4 metrics and llm with each calculated metric) and m2t."""
    rows = []
    m2m = data["similarity"][SIM_TYPES].copy()
    m2m["llm"] = data["llm_m2m"]
    m2m = m2m[M2M_METRICS].dropna()
    m2m = m2m[m2m.index.isin(use_cases)]
    groups = {"all": M2M_METRICS, **{"llm*{}".format(sim_type): ["llm", sim_type] for sim_type in SIM_TYPES}}
    for group, metrics in groups.items():
        values = m2m[metrics]
        rows.append({"dataset": name, "evaluation": "m2m", "metrics": group, "n": len(values),
                     **spearman_test(values.mean(axis=1), values.max(axis=1) - values.min(axis=1))})

    for metric in TEXT_METRICS:
        values = pd.DataFrame({"llm": data["llm_m2t"][metric], "calculated": data["text"][metric]}).dropna()
        values = values[values.index.isin(use_cases)]
        rows.append({"dataset": name, "evaluation": "m2t", "metrics": "llm*{}".format(metric), "n": len(values),
                     **spearman_test(values.mean(axis=1), values.max(axis=1) - values.min(axis=1))})
    return rows


def source_of_difference(datasets):
    """ic3: counts of the source_of_difference categories of the use cases of every dataset, over all 12 files."""
    report = {}
    for evaluation_type in EVALUATION_TYPES:
        sets = {name: [] for name in datasets}
        for results_path in sorted(glob.glob(os.path.join(AUTOMATIC_DIR, evaluation_type + "_*.json"))):
            with open(results_path) as file:
                results = json.load(file)
            for name, use_cases in datasets.items():
                subset = {group: {use_case: result for use_case, result in group_results.items() if use_case in use_cases}
                          for group, group_results in results.items()}
                sets[name] += source_sets(subset)
        report[evaluation_type] = {name: count(name_sets, CATEGORIES[evaluation_type]) for name, name_sets in sets.items()}
    return report


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    datasets = {dataset: dataset_use_cases(dataset) for dataset in DATASETS}
    datasets[ALL] = set().union(*datasets.values())

    data = {
        "similarity": pd.read_csv(SIMILARITY_FILE).set_index("file name"),
        "text": pd.read_csv(TEXT_SIMILARITY_FILE).set_index("file name"),
        "llm_m2m": llm_similarity(ALL, ALL),
        "llm_m2t": {metric: llm_metric(ALL, ALL, metric) for metric in TEXT_METRICS},
    }

    # ic12
    reports = {path: read_report(path) for path in CALCULATED}
    write_csv(AVERAGE_FILE, OVERVIEW_COLUMNS, [average_row(name, use_cases, reports) for name, use_cases in datasets.items()])

    # ic3
    reliability = pd.DataFrame([row for name, use_cases in datasets.items() for row in reliability_rows(name, use_cases, data)])
    print(reliability.to_string(index=False))
    reliability.to_csv(RELIABILITY_FILE, index=False)
    print("Saved {}".format(RELIABILITY_FILE))

    with open(SOURCE_OF_DIFFERENCE_FILE, "w") as file:
        json.dump(source_of_difference(datasets), file, indent=4)
    print("Saved {}".format(SOURCE_OF_DIFFERENCE_FILE))

    # ic4
    magnitude = pd.DataFrame([row for name, use_cases in datasets.items() for row in magnitude_rows(name, use_cases, data)])
    print(magnitude.to_string(index=False))
    magnitude.to_csv(MAGNITUDE_FILE, index=False)
    print("Saved {}".format(MAGNITUDE_FILE))
