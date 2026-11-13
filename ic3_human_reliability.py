import os
import argparse

import pandas as pd

from ic3_deterministic_reliability_m2m import ALL, OUTPUT_DIR, agreement

STATISTICS_DIR = os.path.join(OUTPUT_DIR, "human")
REPRESENTATIONS = ["bpmn", "mermaid_js", "simple_json"]
LLMS = ["anthropic", "gemini", "gpt"]
EXAMPLES = ["examples", "no_examples"]  # few-shot with examples / system prompt only (file suffix _no_examples)
KEY = ["file name", "model"]  # a process model


def read_report(representation, llm, example):
    suffix = "" if example == "examples" else "_no_examples"
    report = pd.read_csv(os.path.join(STATISTICS_DIR, "{}_{}{}.csv".format(representation, llm, suffix)))
    return report.set_index(KEY)


def scores(representation, llm, example):
    """(llm score, human score) per process model: the mean column of one report, or averaged over all 9 reports of the
    example setting (all = only process models that are present in all of them)."""
    if representation != ALL:
        report = read_report(representation, llm, example)
        return report["mean"], report["human_score"]

    reports = [read_report(r, l, example) for r in REPRESENTATIONS for l in LLMS]
    llm_score = pd.concat([report["mean"] for report in reports], axis=1).dropna().mean(axis=1)
    return llm_score, reports[0]["human_score"]  # the human score of a process model is the same in all reports


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agreement of the llm score with the human score.")
    parser.add_argument('-r', '--representation', type=str, required=False, default=ALL,
                        help='Representation: {} (default {}: averaged over all)'.format(', '.join(REPRESENTATIONS), ALL))
    parser.add_argument('-l', '--llm', type=str, required=False, default=ALL,
                        help='Llm: {} (default {}: averaged over all)'.format(', '.join(LLMS), ALL))
    args = parser.parse_args()

    if (args.representation == ALL) != (args.llm == ALL):
        parser.error("pass both -r and -l, or none of them")
    if args.representation != ALL and (args.representation not in REPRESENTATIONS or args.llm not in LLMS):
        parser.error("representation has to be one of {}, llm one of {}".format(REPRESENTATIONS, LLMS))

    rows = []
    for example in EXAMPLES:
        llm_score, human_score = scores(args.representation, args.llm, example)
        row = agreement(llm_score, human_score, "human")
        # mean scores over the same process models as the agreement (with both scores)
        pairs = pd.concat([llm_score, human_score], axis=1, join="inner").dropna()
        means = {"human_mean": round(float(pairs.iloc[:, 1].mean()), 4),
                 "llm_mean": round(float(pairs.iloc[:, 0].mean()), 4)}
        rows.append({"examples": example, "pair": row.pop("pair"), "n": row.pop("n"), **means, **row})
    table = pd.DataFrame(rows)
    print(table.to_string(index=False))

    name = "correlation_human_{}.csv".format(ALL if args.representation == ALL else "{}_{}".format(args.representation, args.llm))
    path = os.path.join(OUTPUT_DIR, name)
    table.to_csv(path, index=False)
    print("Saved {}".format(path))
