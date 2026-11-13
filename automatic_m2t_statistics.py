import os
import csv
import json
import glob

from automatic_m2m_statistics import AUTOMATIC_DIR, OUTPUT_DIR, COLUMNS, statistics_row

METRICS = ["relevance", "truthfulness"]


def automatic_m2t_statistics():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for results_path in sorted(glob.glob(os.path.join(AUTOMATIC_DIR, "m2t_*.json"))):
        with open(results_path) as file:
            results = json.load(file)

        name = os.path.splitext(os.path.basename(results_path))[0]
        for metric in METRICS:
            rows = [statistics_row(use_case, result.get("iterations", {}), metric)
                    for use_cases in results.values() for use_case, result in use_cases.items()]

            with open(os.path.join(OUTPUT_DIR, "{}_{}.csv".format(name, metric)), "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=COLUMNS)
                writer.writeheader()
                writer.writerows(rows)
            print("{}_{}: {} use cases".format(name, metric, len(rows)))


if __name__ == "__main__":
    automatic_m2t_statistics()
