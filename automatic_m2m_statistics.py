import os
import csv
import json
import glob
import statistics

BASE = os.path.dirname(os.path.abspath(__file__))
AUTOMATIC_DIR = os.path.join(BASE, "generation", "automatic")
OUTPUT_DIR = os.path.join(BASE, "similarity", "automatic")
SCORE = "element_based_similarity"  # key of the similarity in the llm answer (prompts/autoeval_m2m.txt)

COLUMNS = [
    "file name",
    "mean",
    "median",
    "range",                   # max - min
    "std",                     # sample standard deviation
    "cv",                      # coefficient of variation = std / mean
]


def rounded(value):
    return "" if value is None else round(value, 4)


def statistics_row(use_case, iterations, score=SCORE):
    """Statistics of the metric `score` of the evaluations over the iterations of one use case."""
    evaluations = [it["evaluation"] for it in iterations.values() if isinstance(it.get("evaluation"), dict)]
    scores = [float(e[score]) for e in evaluations if isinstance(e.get(score), (int, float))]

    row = {column: "" for column in COLUMNS}
    row["file name"] = use_case
    if scores:
        mean = statistics.mean(scores)
        std = statistics.stdev(scores) if len(scores) > 1 else 0.0
        row.update({
            "mean": rounded(mean),
            "median": rounded(statistics.median(scores)),
            "range": rounded(max(scores) - min(scores)),
            "std": rounded(std),
            "cv": rounded(std / mean) if mean else "",
        })
    return row


def automatic_similarity_statistics():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for results_path in sorted(glob.glob(os.path.join(AUTOMATIC_DIR, "m2m_*.json"))):
        with open(results_path) as file:
            results = json.load(file)

        rows = [statistics_row(use_case, result.get("iterations", {}))
                for use_cases in results.values() for use_case, result in use_cases.items()]

        name = os.path.splitext(os.path.basename(results_path))[0]
        with open(os.path.join(OUTPUT_DIR, name + ".csv"), "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        print("{}: {} use cases".format(name, len(rows)))


if __name__ == "__main__":
    automatic_similarity_statistics()
