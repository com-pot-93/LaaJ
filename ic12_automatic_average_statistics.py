import os
import csv
import statistics

from automatic_m2m_statistics import BASE, OUTPUT_DIR as REPORTS_DIR

SCRIPT = os.path.splitext(os.path.basename(__file__))[0]
OUTPUT_DIR = os.path.join(BASE, "evaluation", "automatic")
AVERAGE_FILE = os.path.join(OUTPUT_DIR, SCRIPT + ".csv")
REPRESENTATIONS = ["bpmn", "cpee", "mermaid_js", "simple_json"]
LLMS = ["anthropic", "gemini", "gpt"]
# metric -> report name of a representation and llm
METRICS = {
    "similarity": "m2m_{}_{}.csv",
    "relevance": "m2t_{}_{}_relevance.csv",
    "truthfulness": "m2t_{}_{}_truthfulness.csv",
}
VALUES = ["mean", "range", "std", "cv"]  # columns of the reports that are averaged
METRIC_COLUMNS = ["{}_{}".format(metric, value) for metric in METRICS for value in VALUES]


def read_report(report_path):
    if not os.path.isfile(report_path):
        print("Missing {}, left empty".format(report_path))
        return []
    with open(report_path, newline="") as file:
        return list(csv.DictReader(file))


def average_columns(rows):
    """Average of the VALUES columns over the rows (use cases without a value are left out)."""
    averages = {}
    for value in VALUES:
        numbers = [float(row[value]) for row in rows if row[value] != ""]
        averages[value] = round(statistics.mean(numbers), 4) if numbers else ""
    return averages


def metric_values(representation, llm, use_cases=None):
    """METRIC_COLUMNS of a representation and llm, averaged over the given use cases (None = all)."""
    values = {}
    for metric, report_name in METRICS.items():
        rows = read_report(os.path.join(REPORTS_DIR, report_name.format(representation, llm)))
        if use_cases is not None:
            rows = [row for row in rows if row["file name"] in use_cases]
        for value, average in average_columns(rows).items():
            values["{}_{}".format(metric, value)] = average
    return values


def write_csv(path, columns, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print("Saved {}".format(path))


def automatic_average_statistics():
    rows = [{"representation": representation, "llm": llm, **metric_values(representation, llm)}
            for representation in REPRESENTATIONS for llm in LLMS]
    write_csv(AVERAGE_FILE, ["representation", "llm"] + METRIC_COLUMNS, rows)


if __name__ == "__main__":
    automatic_average_statistics()
