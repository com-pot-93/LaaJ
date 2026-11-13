import os
import json
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
PROCESSES_DIR = os.path.join(BASE, "data", "llm_generated")
DESCRIPTIONS_DIR = os.path.join(PROCESSES_DIR, "process_descriptions")
GENERATED_DIR = os.path.join(PROCESSES_DIR, "generated")
EMPTY_MODEL = os.path.join(BASE, "cpee_empty_example")
DATASETS = ["domain", "pet", "realset"]

URL = "https://cpee.org/llm/"
LLM = "gemini-3.1-flash-lite"
PROMPT_TYPE = "generate_noendpoints"
TEMPERATURE = "0"


def read(path):
    with open(path, "r") as file:
        return file.read().strip()


def write(path, content):
    with open(path, "w") as file:
        file.write(content)


def generate_model(description):
    """Generates a cpee model of the process description via cpee.org. Returns the cpee xml."""
    with open(EMPTY_MODEL, "rb") as empty_model:
        files = {
            "rpst_xml": (os.path.basename(EMPTY_MODEL), empty_model, "text/xml"),
            "user_input": (None, description, "text/plain"),
            "llm": (None, LLM, "text/plain"),
            "prompt_type": (None, PROMPT_TYPE, "text/plain"),
            "temperature": (None, TEMPERATURE, "text/plain"),
        }
        response = requests.post(URL, files=files)
    response.raise_for_status()
    result = json.loads(response.text)
    return result["output_cpee"]


def generate_models():
    for dataset in DATASETS:
        descriptions_dir = os.path.join(DESCRIPTIONS_DIR, dataset)
        target_dir = os.path.join(GENERATED_DIR, dataset)
        os.makedirs(target_dir, exist_ok=True)

        use_cases = sorted(f[:-len(".txt")] for f in os.listdir(descriptions_dir) if f.endswith(".txt"))
        for i, use_case in enumerate(use_cases):
            print("{} {}/{} {}".format(dataset, i + 1, len(use_cases), use_case))
            try:
                cpee = generate_model(read(os.path.join(descriptions_dir, use_case + ".txt")))
            except Exception as e:
                print("Generation of {} of {} failed: {}".format(use_case, dataset, e))
                continue
            write(os.path.join(target_dir, use_case + ".cpee.xml"), cpee)


if __name__ == "__main__":
    generate_models()
