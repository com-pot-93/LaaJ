import os
import json

from ic3_source_of_difference import count

BASE = os.path.dirname(os.path.abspath(__file__))
HUMAN_DIR = os.path.join(BASE, "generation", "human")
OUTPUT_FILE = os.path.join(BASE, "evaluation", "human", os.path.splitext(os.path.basename(__file__))[0] + ".json")
REPRESENTATIONS = ["bpmn", "mermaid_js", "simple_json"]
LLMS = ["anthropic", "gemini", "gpt"]
EXAMPLES = ["examples", "no_examples"]  # few-shot with examples / system prompt only (file suffix _no_examples)
COMMENTS = "comments"
# the nine criteria of prompts/human_evaluation.txt, the allowed keys of comments
CRITERIA = ["syntax", "structural_correctness", "semantic_alignment", "hallucinations", "semantic_label_correctness",
            "model_comprehensibility", "modeling_appropriateness_and_complexity", "bpmn_modeling_best_practices",
            "pragmatic_label_quality"]


def results_file(representation, llm, example):
    suffix = "" if example == "examples" else "_no_examples"
    return os.path.join(HUMAN_DIR, "{}_{}{}.json".format(representation, llm, suffix))


def criteria_sets(results):
    """Sets of commented criteria (keys of comments) of all evaluations of a result file."""
    sets = []
    for models in results.values():
        for result in models.values():
            for iteration in result.get("iterations", {}).values():
                evaluation = iteration.get("evaluation")
                if isinstance(evaluation, dict) and isinstance(evaluation.get(COMMENTS), dict):
                    sets.append(sorted(set(evaluation[COMMENTS])))
    return sets


def human_source_of_difference_statistics():
    report = {}
    for example in EXAMPLES:
        all_sets = []
        per_file = {}
        for representation in REPRESENTATIONS:
            for llm in LLMS:
                path = results_file(representation, llm, example)
                if not os.path.isfile(path):
                    print("Missing {}, skipped".format(path))
                    continue
                with open(path) as file:
                    sets = criteria_sets(json.load(file))
                per_file["{}_{}".format(representation, llm)] = count(sets)
                all_sets += sets
        report[example] = {"all": count(all_sets, CRITERIA), **per_file}

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as file:
        json.dump(report, file, indent=4)
    print("Saved {}".format(OUTPUT_FILE))


if __name__ == "__main__":
    human_source_of_difference_statistics()
