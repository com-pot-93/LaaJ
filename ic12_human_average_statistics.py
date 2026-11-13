import os
import csv
import glob
import statistics

BASE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.splitext(os.path.basename(__file__))[0]
REPORTS_DIR = os.path.join(BASE, "similarity", "human")  # human_statistics.py
OUTPUT_DIR = os.path.join(BASE, "evaluation", "human")
AVERAGE_FILE = os.path.join(OUTPUT_DIR, SCRIPT + ".csv")
NO_EXAMPLES = "_no_examples"
LLMS = ["anthropic", "gemini", "gpt"]
# columns of the reports that are averaged over the models
AVERAGED = ["human_score", "mean", "median", "range", "std", "cv"]
COLUMNS = ["representation", "llm", "examples", "models"] + AVERAGED


def average(rows, column):
    numbers = [float(row[column]) for row in rows if row[column] != ""]
    return round(statistics.mean(numbers), 4) if numbers else ""


def parse_name(name):
    """<representation>_<llm>[_no_examples] -> (representation, llm, examples), None if the name is not a report name."""
    examples = not name.endswith(NO_EXAMPLES)
    if not examples:
        name = name[:-len(NO_EXAMPLES)]
    parts = name.rsplit("_", 1)
    if len(parts) != 2 or parts[1] not in LLMS:
        return None
    representation, llm = parts
    return representation, llm, examples


def human_average_statistics():
    rows = []
    for report_path in sorted(glob.glob(os.path.join(REPORTS_DIR, "*.csv"))):
        parsed = parse_name(os.path.splitext(os.path.basename(report_path))[0])
        if parsed is None:  # e.g. a copy of an old average file
            print("Skipped {} (not a <representation>_<llm>[_no_examples].csv report)".format(report_path))
            continue
        with open(report_path, newline="") as file:
            report = list(csv.DictReader(file))

        representation, llm, examples = parsed
        row = {"representation": representation, "llm": llm, "examples": examples, "models": len(report)}
        for column in AVERAGED:
            row[column] = average(report, column)
        rows.append(row)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(AVERAGE_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print("Saved {}".format(AVERAGE_FILE))


if __name__ == "__main__":
    human_average_statistics()
