import os
import sys
import glob
import json

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "src", "cpee_converter"))

from cpee_bpmn import convert_cpee_bpmn, open_instance
from cpee_json import convert_cpee_json
from cpee_mermaid import convert_cpee_mermaid

INSTANCE_NUMBER = "113507"  # cpee instance on autobpmn.ai used for the bpmn conversion
GENERATED_DIR = os.path.join(BASE, "data", "llm_generated", "generated")
#GENERATED_DIR = os.path.join(BASE, "data", "llm_generated", "ground_truth")
CPEE_EXTENSION = ".cpee.xml"


def write(path, content):
    with open(path, "w") as file:
        file.write(content)


def convert_generated():
    cpee_files = sorted(glob.glob(os.path.join(GENERATED_DIR, "*", "*" + CPEE_EXTENSION)))

    with open_instance(INSTANCE_NUMBER) as page:  # one browser for all bpmn conversions
        for i, cpee_file in enumerate(cpee_files):
            print("{}/{} {}".format(i + 1, len(cpee_files), cpee_file))
            name = cpee_file[:-len(CPEE_EXTENSION)]

            # each conversion on its own, so one failing conversion does not stop the others
            try:
                model = convert_cpee_json(cpee_file)
                if "error" in model:
                    print("No json for {}: {}".format(cpee_file, model["error"]))
                else:
                    write(name + ".json", json.dumps(model, indent=4))
            except Exception as e:
                print("json conversion of {} failed: {}".format(cpee_file, e))

            try:
                write(name + ".md", convert_cpee_mermaid(cpee_file))
            except Exception as e:
                print("mermaid conversion of {} failed: {}".format(cpee_file, e))

            try:
                write(name + ".bpmn", convert_cpee_bpmn(cpee_file, INSTANCE_NUMBER, page))
            except Exception as e:
                print("bpmn conversion of {} failed: {}".format(cpee_file, e))


if __name__ == "__main__":
    convert_generated()
