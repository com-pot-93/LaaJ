import os
import csv
import json
import glob
import statistics

BASE = os.path.dirname(os.path.abspath(__file__))
HUMAN_DIR = os.path.join(BASE, "generation", "human")
OUTPUT_DIR = os.path.join(BASE, "similarity", "human")
SCORE = "score"

COLUMNS = [
    "file name",
    "model",
    "human_score",
    "mean",
    "median",
    "range",                     # max - min
    "std",                       # sample standard deviation
    "cv",                        # coefficient of variation = std / mean
]


def rounded(value):
    return "" if value is None else round(value, 4)


def statistics_row(use_case, model, result):
    """Statistics of the llm score over the iterations of one model, compared to its human score."""
    evaluations = [it["evaluation"] for it in result.get("iterations", {}).values() if isinstance(it.get("evaluation"), dict)]
    scores = [float(e[SCORE]) for e in evaluations if isinstance(e.get(SCORE), (int, float))]
    human_score = result.get("human_score")

    row = {column: "" for column in COLUMNS}
    row["file name"] = use_case
    row["model"] = model
    row["human_score"] = "" if human_score is None else human_score
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


def human_statistics():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for results_path in sorted(glob.glob(os.path.join(HUMAN_DIR, "*.json"))):
        with open(results_path) as file:
            results = json.load(file)

        rows = [statistics_row(use_case, model, result)
                for use_case, models in results.items() for model, result in models.items()]

        name = os.path.splitext(os.path.basename(results_path))[0]
        with open(os.path.join(OUTPUT_DIR, name + ".csv"), "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        print("{}: {} models".format(name, len(rows)))


if __name__ == "__main__":
    human_statistics()
