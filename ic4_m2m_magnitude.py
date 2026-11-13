import os
import argparse

import pandas as pd
from scipy import stats

from ic3_deterministic_reliability_m2m import ALL, LLMS, OUTPUT_DIR, REPRESENTATIONS, SIM_TYPES, SIMILARITY_FILE, llm_similarity, p_value

ALPHA = 0.05
METRICS = ["llm"] + SIM_TYPES


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spearman test of the relation between average similarity and range of the metrics.")
    parser.add_argument('-r', '--representation', type=str, required=False, default=ALL,
                        help='Representation: {} (default {}: averaged over all)'.format(', '.join(REPRESENTATIONS), ALL))
    parser.add_argument('-l', '--llm', type=str, required=False, default=ALL,
                        help='Llm: {} (default {}: averaged over all)'.format(', '.join(LLMS), ALL))
    args = parser.parse_args()

    if (args.representation == ALL) != (args.llm == ALL):
        parser.error("pass both -r and -l, or none of them")
    if args.representation != ALL and (args.representation not in REPRESENTATIONS or args.llm not in LLMS):
        parser.error("representation has to be one of {}, llm one of {}".format(REPRESENTATIONS, LLMS))

    # the 4 metrics per use case, only use cases with all of them
    df = pd.read_csv(SIMILARITY_FILE).set_index("file name")[SIM_TYPES]
    df["llm"] = llm_similarity(args.representation, args.llm)
    df = df[METRICS].dropna()

    # all 4 metrics together, and the llm with each calculated metric individually
    groups = {"all": METRICS, **{"llm*{}".format(sim_type): ["llm", sim_type] for sim_type in SIM_TYPES}}
    results = []
    for group, metrics in groups.items():
        suffix = "" if group == "all" else "_" + group.split("*")[1]  # avg_sim, range / avg_sim_task, range_task, ...
        df["avg_sim" + suffix] = df[metrics].mean(axis=1)
        df["range" + suffix] = df[metrics].max(axis=1) - df[metrics].min(axis=1)

        rho, p_two_sided = stats.spearmanr(df["avg_sim" + suffix], df["range" + suffix])
        _, p_less = stats.spearmanr(df["avg_sim" + suffix], df["range" + suffix], alternative="less")
        results.append({
            "metrics": group,
            "n": len(df),
            "spearman": round(rho, 4),
            "p_one_sided": p_value(p_less),   # H1: negative relation
            "p_two_sided": p_value(p_two_sided),
            "H0": "rejected" if p_less < ALPHA else "accepted",  # H0: no relation, one-sided test, alpha 0.05
        })
    result = pd.DataFrame(results)
    print(result.to_string(index=False))

    name = "agreement_{}".format(ALL if args.representation == ALL else "{}_{}".format(args.representation, args.llm))
    df.round(4).to_csv(os.path.join(OUTPUT_DIR, name + ".csv"))
    result.to_csv(os.path.join(OUTPUT_DIR, name + "_test.csv"), index=False)
    print("Saved {} and {}".format(os.path.join(OUTPUT_DIR, name + ".csv"), os.path.join(OUTPUT_DIR, name + "_test.csv")))