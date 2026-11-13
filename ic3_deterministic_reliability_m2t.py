import os
import argparse

import pandas as pd

from ic3_deterministic_reliability_m2m import ALL, LLMS, OUTPUT_DIR, REPRESENTATIONS, SIMILARITY_DIR, STATISTICS_DIR, agreement

SCRIPT = os.path.splitext(os.path.basename(__file__))[0]
TEXT_SIMILARITY_FILE = os.path.join(SIMILARITY_DIR, "text_similarity.csv")
REPORT = "m2t_{}_{}_{}.csv"
METRICS = ["relevance", "truthfulness"]


def llm_metric(representation, llm, metric):
    """llm metric per use case: the mean column of one report, or averaged over all 12 reports of the metric
    (all = only use cases that are present in all of them)."""
    if representation != ALL:
        report = pd.read_csv(os.path.join(STATISTICS_DIR, REPORT.format(representation, llm, metric)))
        return report.set_index("file name")["mean"]

    columns = [pd.read_csv(os.path.join(STATISTICS_DIR, REPORT.format(r, l, metric))).set_index("file name")["mean"]
               for r in REPRESENTATIONS for l in LLMS]
    return pd.concat(columns, axis=1).dropna().mean(axis=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agreement of the llm relevance / truthfulness with the calculated ones.")
    parser.add_argument('-r', '--representation', type=str, required=False, default=ALL,
                        help='Representation: {} (default {}: averaged over all)'.format(', '.join(REPRESENTATIONS), ALL))
    parser.add_argument('-l', '--llm', type=str, required=False, default=ALL,
                        help='Llm: {} (default {}: averaged over all)'.format(', '.join(LLMS), ALL))
    args = parser.parse_args()

    if (args.representation == ALL) != (args.llm == ALL):
        parser.error("pass both -r and -l, or none of them")
    if args.representation != ALL and (args.representation not in REPRESENTATIONS or args.llm not in LLMS):
        parser.error("representation has to be one of {}, llm one of {}".format(REPRESENTATIONS, LLMS))

    text_similarity = pd.read_csv(TEXT_SIMILARITY_FILE).set_index("file name")
    table = pd.DataFrame([agreement(llm_metric(args.representation, args.llm, metric), text_similarity[metric], metric)
                          for metric in METRICS])
    print(table.to_string(index=False))

    name = "{}_{}.csv".format(SCRIPT, ALL if args.representation == ALL else "{}_{}".format(args.representation, args.llm))
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, name)
    table.to_csv(path, index=False)
    print("Saved {}".format(path))
