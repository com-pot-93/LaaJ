import os
import csv
import json
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
PROCESSES_DIR = os.path.join(BASE, "data", "llm_generated")
GROUND_TRUTH_DIR = os.path.join(PROCESSES_DIR, "ground_truth")
GENERATED_DIR = os.path.join(PROCESSES_DIR, "generated")
DESCRIPTIONS_DIR = os.path.join(PROCESSES_DIR, "process_descriptions")
SIMILARITY_DIR = os.path.join(BASE, "similarity")
SIMILARITY_FILE = os.path.join(SIMILARITY_DIR, "text_similarity.csv")
DATASETS = ["domain", "pet", "realset"]
CPEE_EXTENSION = ".cpee.xml"
DESCRIPTION_EXTENSION = ".txt"

URL = "https://cpee.org/similarity/text/"
SIM_TYPES = ["relevance", "truthfulness"]
THRESHOLD = "0.65"


def calculate_text_similarity(text, model, sim_type):
    """Similarity of a process description (txt file) and a cpee xml file via cpee.org, sim_type = relevance or truthfulness."""
    with open(text, "rb") as text_file, open(model, "rb") as model_file:
        files = {
            "text": (os.path.basename(text), text_file, "text/plain"),
            "rpst_xml": (os.path.basename(model), model_file, "text/xml"),
            "sim_type": (None, sim_type, "text/plain"),
            "threshold": (None, THRESHOLD, "text/plain"),
        }
        response = requests.get(URL, files=files)
    response.raise_for_status()
    return json.loads(response.text)["similarity"]


def calculate_text_similarities():
    os.makedirs(SIMILARITY_DIR, exist_ok=True)

    rows = []
    for dataset in DATASETS:
        ground_truth_dir = os.path.join(GROUND_TRUTH_DIR, dataset)
        generated_dir = os.path.join(GENERATED_DIR, dataset)
        descriptions_dir = os.path.join(DESCRIPTIONS_DIR, dataset)
        use_cases = sorted(f[:-len(CPEE_EXTENSION)] for f in os.listdir(ground_truth_dir) if f.endswith(CPEE_EXTENSION))

        for i, use_case in enumerate(use_cases):
            generated = os.path.join(generated_dir, use_case + CPEE_EXTENSION)
            description = os.path.join(descriptions_dir, use_case + DESCRIPTION_EXTENSION)
            if not os.path.isfile(generated):
                print("No generated model for {} of {}, skipped".format(use_case, dataset))
                continue
            if not os.path.isfile(description):
                print("No process description for {} of {}, skipped".format(use_case, dataset))
                continue

            print("{} {}/{} {}".format(dataset, i + 1, len(use_cases), use_case))
            row = {"file name": use_case}
            for sim_type in SIM_TYPES:
                try:
                    row[sim_type] = calculate_text_similarity(description, generated, sim_type)
                except Exception as e:  # the value stays empty in the csv
                    print("{} of {} of {} failed: {}".format(sim_type, use_case, dataset, e))
                    row[sim_type] = ""
            rows.append(row)

    with open(SIMILARITY_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["file name"] + SIM_TYPES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    calculate_text_similarities()
