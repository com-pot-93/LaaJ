import os
import csv
import json
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
PROCESSES_DIR = os.path.join(BASE, "data", "llm_generated")
GROUND_TRUTH_DIR = os.path.join(PROCESSES_DIR, "ground_truth")
GENERATED_DIR = os.path.join(PROCESSES_DIR, "generated")
SIMILARITY_DIR = os.path.join(BASE, "similarity")
SIMILARITY_FILE = os.path.join(SIMILARITY_DIR, "similarity.csv")
DATASETS = ["domain", "pet", "realset"]
CPEE_EXTENSION = ".cpee.xml"

URL = "https://cpee.org/similarity/"
SIM_TYPES = ["task", "element", "trace"]
THRESHOLD = "0.65"


def calculate_similarity(model_a, model_b, sim_type):
    """Similarity of two cpee xml files via cpee.org, sim_type = task, element or trace."""
    with open(model_a, "rb") as file_a, open(model_b, "rb") as file_b:
        files = {
            "rpst_xml_a": (os.path.basename(model_a), file_a, "text/xml"),
            "rpst_xml_b": (os.path.basename(model_b), file_b, "text/xml"),
            "sim_type": (None, sim_type, "text/plain"),
            "threshold": (None, THRESHOLD, "text/plain"),
        }
        response = requests.get(URL, files=files)
    response.raise_for_status()
    return json.loads(response.text)["similarity"]


def calculate_similarities():
    os.makedirs(SIMILARITY_DIR, exist_ok=True)

    rows = []
    for dataset in DATASETS:
        ground_truth_dir = os.path.join(GROUND_TRUTH_DIR, dataset)
        generated_dir = os.path.join(GENERATED_DIR, dataset)
        use_cases = sorted(f[:-len(CPEE_EXTENSION)] for f in os.listdir(ground_truth_dir) if f.endswith(CPEE_EXTENSION))

        for i, use_case in enumerate(use_cases):
            ground_truth = os.path.join(ground_truth_dir, use_case + CPEE_EXTENSION)
            generated = os.path.join(generated_dir, use_case + CPEE_EXTENSION)
            if not os.path.isfile(generated):
                print("No generated model for {} of {}, skipped".format(use_case, dataset))
                continue

            print("{} {}/{} {}".format(dataset, i + 1, len(use_cases), use_case))
            row = {"file name": use_case}
            for sim_type in SIM_TYPES:
                try:
                    row[sim_type] = calculate_similarity(ground_truth, generated, sim_type)
                except Exception as e:  # the value stays empty in the csv
                    print("{} similarity of {} of {} failed: {}".format(sim_type, use_case, dataset, e))
                    row[sim_type] = ""
            rows.append(row)

    with open(SIMILARITY_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["file name"] + SIM_TYPES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    calculate_similarities()
