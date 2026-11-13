import os
import argparse

import pandas as pd
from scipy import stats

from ic3_deterministic_reliability_m2m import ALL, OUTPUT_DIR, p_value
from ic3_human_reliability import EXAMPLES, LLMS, REPRESENTATIONS, scores
from ic4_m2m_magnitude import ALPHA


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spearman test of the relation between average and range of the llm and human score.")
    parser.add_argument('-r', '--representation', type=str, required=False, default=ALL,
                        help='Representation: {} (default {}: averaged over all)'.format(', '.join(REPRESENTATIONS), ALL))
    parser.add_argument('-l', '--llm', type=str, required=False, default=ALL,
                        help='Llm: {} (default {}: averaged over all)'.format(', '.join(LLMS), ALL))
    args = parser.parse_args()

    if (args.representation == ALL) != (args.llm == ALL):
        parser.error("pass both -r and -l, or none of them")
    if args.representation != ALL and (args.representation not in REPRESENTATIONS or args.llm not in LLMS):
        parser.error("representation has to be one of {}, llm one of {}".format(REPRESENTATIONS, LLMS))

    frames, results = [], []
    for example in EXAMPLES:
        # the 2 scores per process model, only process models with both
        llm_score, human_score = scores(args.representation, args.llm, example)
        df = pd.concat({"llm": llm_score, "human": human_score}, axis=1, join="inner").dropna()
        df["avg_sim"] = df[["llm", "human"]].mean(axis=1)
        df["range"] = df[["llm", "human"]].max(axis=1) - df[["llm", "human"]].min(axis=1)

        rho, p_two_sided = stats.spearmanr(df["avg_sim"], df["range"])
        _, p_less = stats.spearmanr(df["avg_sim"], df["range"], alternative="less")
        results.append({
            "examples": example,
            "n": len(df),
            "spearman": round(rho, 4),
            "p_one_sided": p_value(p_less),   # H1: negative relation
            "p_two_sided": p_value(p_two_sided),
            "H0": "rejected" if p_less < ALPHA else "accepted",  # H0: no relation, one-sided test, alpha 0.05
        })
        frames.append(df.add_prefix(example + "_"))

    result = pd.DataFrame(results)
    print(result.to_string(index=False))

    name = "agreement_human_{}".format(ALL if args.representation == ALL else "{}_{}".format(args.representation, args.llm))
    pd.concat(frames, axis=1).round(4).to_csv(os.path.join(OUTPUT_DIR, name + ".csv"))
    result.to_csv(os.path.join(OUTPUT_DIR, name + "_test.csv"), index=False)
    print("Saved {} and {}".format(os.path.join(OUTPUT_DIR, name + ".csv"), os.path.join(OUTPUT_DIR, name + "_test.csv")))
