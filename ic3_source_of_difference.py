import os
import json
import glob
import itertools
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
AUTOMATIC_DIR = os.path.join(BASE, "generation", "automatic")
OUTPUT_FILE = os.path.join(BASE, "evaluation", "automatic", os.path.splitext(os.path.basename(__file__))[0] + ".json")
EVALUATION_TYPES = ["m2m", "m2t"]
SOURCES = "source_of_difference"
SEPARATOR = " + "
# predefined categories of prompts/autoeval_m2m.txt and prompts/autoeval_m2t.txt
CATEGORIES = {
    "m2m": ["ACTIVITY_DIFFERENCES", "GATEWAY_DIFFERENCES", "CONNECTION_DIFFERENCES", "LABEL_DIFFERENCES",
            "EVENT_DIFFERENCES", "OTHER_DIFFERENCES"],
    "m2t": ["MISSING_INFORMATION", "ADDED_INFORMATION", "STRUCTURE_DIFFERENCES", "GATEWAY_DIFFERENCES",
            "LABEL_DIFFERENCES"],
}


def source_sets(results):
    """Category sets of all evaluations of a result file."""
    sets = []
    for use_cases in results.values():
        for result in use_cases.values():
            for iteration in result.get("iterations", {}).values():
                evaluation = iteration.get("evaluation")
                if isinstance(evaluation, dict) and isinstance(evaluation.get(SOURCES), list):
                    sets.append(sorted(set(evaluation[SOURCES])))
    return sets


def most_common(counter):
    return dict(counter.most_common())


def count(sets, all_categories=None):
    """all_categories: also list every possible combination of these categories (and every category), with 0 if it never appears."""
    categories, combinations = Counter(), Counter()
    if all_categories:
        categories.update({category: 0 for category in all_categories})
        ordered = sorted(all_categories)
        for size in range(len(ordered) + 1):
            combinations.update({combination: 0 for combination in itertools.combinations(ordered, size)})
    for categories_of_evaluation in sets:
        categories.update(categories_of_evaluation)
        combinations[tuple(categories_of_evaluation)] += 1

    # combinations grouped by their number of categories: single categories, pairs, triples, ...
    by_size = {}
    for size in sorted({len(combination) for combination in combinations}):
        of_size = Counter({SEPARATOR.join(c) or "NONE": n for c, n in combinations.items() if len(c) == size})
        by_size[str(size)] = most_common(of_size)
    return {
        "evaluations": len(sets),
        "categories": most_common(categories),
        "combinations": by_size,
    }


def source_of_difference_statistics():
    report = {}
    for evaluation_type in EVALUATION_TYPES:
        all_sets = []
        per_file = {}
        for results_path in sorted(glob.glob(os.path.join(AUTOMATIC_DIR, evaluation_type + "_*.json"))):
            with open(results_path) as file:
                sets = source_sets(json.load(file))
            name = os.path.splitext(os.path.basename(results_path))[0][len(evaluation_type) + 1:]  # <representation>_<llm>
            per_file[name] = count(sets)
            all_sets += sets
        report[evaluation_type] = {"all": count(all_sets, CATEGORIES[evaluation_type]), **per_file}

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as file:
        json.dump(report, file, indent=4)
    print("Saved {}".format(OUTPUT_FILE))


if __name__ == "__main__":
    source_of_difference_statistics()
