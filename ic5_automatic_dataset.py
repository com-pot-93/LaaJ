import os
import statistics

from ic12_automatic_average_statistics import (BASE, LLMS, METRIC_COLUMNS, OUTPUT_DIR, REPRESENTATIONS, metric_values,
                                               read_report, write_csv)

DESCRIPTIONS_DIR = os.path.join(BASE, "data", "llm_generated", "process_descriptions")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "average_dataset.csv")
OVERVIEW_FILE = os.path.join(OUTPUT_DIR, "average_dataset_overview.csv")
DATASETS = ["domain", "pet", "realset"]
ALL = "all"
COLUMNS = ["dataset", "representation", "llm"] + METRIC_COLUMNS
# calculated metrics: file -> {column of the file: column of the overview}
CALCULATED = {
    os.path.join(BASE, "similarity", "similarity.csv"): {  # calculate_similarity.py
        "task": "task", "element": "element", "trace": "trace"},
    os.path.join(BASE, "similarity", "text_similarity.csv"): {  # calculate_text_similarity.py
        "relevance": "calculated_relevance", "truthfulness": "calculated_truthfulness"},
}
OVERVIEW_VALUES = ["mean", "cv"]  # values of the llm metrics in the overview
OVERVIEW_COLUMNS = (["dataset"] + [column for column in METRIC_COLUMNS if column.rsplit("_", 1)[1] in OVERVIEW_VALUES]
                    + [name for names in CALCULATED.values() for name in names.values()])


def dataset_use_cases(dataset):
    """Use cases of the dataset, i.e. the names of its process descriptions."""
    directory = os.path.join(DESCRIPTIONS_DIR, dataset)
    return {f[:-len(".txt")] for f in os.listdir(directory) if f.endswith(".txt")}


def dataset_rows(dataset):
    use_cases = dataset_use_cases(dataset)
    rows = [{"dataset": dataset, "representation": representation, "llm": llm,
             **metric_values(representation, llm, use_cases)}
            for representation in REPRESENTATIONS for llm in LLMS]

    # all: average of the representation and llm rows (rows without a value are left out)
    average = {"dataset": dataset, "representation": ALL, "llm": ALL}
    for column in METRIC_COLUMNS:
        values = [row[column] for row in rows if row[column] != ""]
        average[column] = round(statistics.mean(values), 4) if values else ""
    return rows + [average]


def calculated_metrics(use_cases, reports):
    """Averages of the calculated metrics (CALCULATED) over the use cases (empty values are left out)."""
    values = {}
    for path, names in CALCULATED.items():
        rows = [row for row in reports[path] if row["file name"] in use_cases]
        for column, name in names.items():
            numbers = [float(row[column]) for row in rows if row.get(column, "") != ""]
            values[name] = round(statistics.mean(numbers), 4) if numbers else ""
    return values


if __name__ == "__main__":
    rows = [row for dataset in DATASETS for row in dataset_rows(dataset)]
    write_csv(OUTPUT_FILE, COLUMNS, rows)

    # overview: only the "all" row of every dataset (mean and cv), with the calculated metrics appended
    reports = {path: read_report(path) for path in CALCULATED}
    overview = [{**{column: row[column] for column in OVERVIEW_COLUMNS if column in row},
                 **calculated_metrics(dataset_use_cases(row["dataset"]), reports)}
                for row in rows if row["representation"] == ALL]
    write_csv(OVERVIEW_FILE, OVERVIEW_COLUMNS, overview)
