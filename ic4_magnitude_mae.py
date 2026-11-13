import os
import argparse

import numpy as np
import pandas as pd

from ic3_deterministic_reliability_m2m import ALL, LLMS, OUTPUT_DIR, REPRESENTATIONS, SIM_TYPES, SIMILARITY_FILE, llm_similarity
from ic3_deterministic_reliability_m2t import METRICS as TEXT_METRICS, TEXT_SIMILARITY_FILE, llm_metric
from ic3_human_reliability import EXAMPLES, REPRESENTATIONS as HUMAN_REPRESENTATIONS, scores

# versions of the grouping: name of the output -> (group names, lower bounds of the 2nd, 3rd, ... group)
# a group contains its lower bound and not its upper bound, the last group contains 1: [0, 0.4), [0.4, 0.8), [0.8, 1]
VERSIONS = {
    "agreement_mae": (["0-0.4", "0.4-0.8", "0.8-1"], [0.4, 0.8]),
    "agreement_mae_2_groups": (["0-0.8", "0.8-1"], [0.8]),
}
HUMAN_SCALE = 5.0


def mae_by_group(llm, other, evaluation, pair, groups, bounds, scale=1.0):
    """n and MAE per similarity group of the use cases with both values; grouped by avg_sim / scale."""
    pairs = pd.concat([llm, other], axis=1, join="inner").dropna()
    x, y = pairs.iloc[:, 0].to_numpy(), pairs.iloc[:, 1].to_numpy()
    group = np.digitize((x + y) / 2 / scale, bounds)  # 0, 1, ...
    row = {"evaluation": evaluation, "pair": pair, "n": len(pairs)}
    for index, name in enumerate(groups):
        in_group = group == index
        row["n_" + name] = int(in_group.sum())
        row["mae_" + name] = round(float(np.abs(x[in_group] - y[in_group]).mean()), 4) if in_group.any() else ""
    return row


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MAE of the llm and the compared measures in 3 groups of similarity.")
    parser.add_argument('-r', '--representation', type=str, required=False, default=ALL,
                        help='Representation: {} (default {}: averaged over all)'.format(', '.join(REPRESENTATIONS), ALL))
    parser.add_argument('-l', '--llm', type=str, required=False, default=ALL,
                        help='Llm: {} (default {}: averaged over all)'.format(', '.join(LLMS), ALL))
    args = parser.parse_args()

    if (args.representation == ALL) != (args.llm == ALL):
        parser.error("pass both -r and -l, or none of them")
    if args.representation != ALL and (args.representation not in REPRESENTATIONS or args.llm not in LLMS):
        parser.error("representation has to be one of {}, llm one of {}".format(REPRESENTATIONS, LLMS))

    # the pairs (evaluation, pair name, llm values, compared values, scale)
    pairs = []
    similarity = pd.read_csv(SIMILARITY_FILE).set_index("file name")
    llm = llm_similarity(args.representation, args.llm)
    pairs += [("m2m", "llm*{}".format(sim_type), llm, similarity[sim_type], 1.0) for sim_type in SIM_TYPES]

    text_similarity = pd.read_csv(TEXT_SIMILARITY_FILE).set_index("file name")
    pairs += [("m2t", "llm*{}".format(metric), llm_metric(args.representation, args.llm, metric), text_similarity[metric], 1.0)
              for metric in TEXT_METRICS]

    if args.representation == ALL or args.representation in HUMAN_REPRESENTATIONS:
        for example in EXAMPLES:
            llm_score, human_score = scores(args.representation, args.llm, example)
            pairs.append(("human_{}".format(example), "llm*human", llm_score, human_score, HUMAN_SCALE))
    else:
        print("No human evaluation for {}, human rows left out".format(args.representation))

    suffix = ALL if args.representation == ALL else "{}_{}".format(args.representation, args.llm)
    for output, (groups, bounds) in VERSIONS.items():
        table = pd.DataFrame([mae_by_group(llm_values, other, evaluation, pair, groups, bounds, scale)
                              for evaluation, pair, llm_values, other, scale in pairs])
        print(table.to_string(index=False))
        path = os.path.join(OUTPUT_DIR, "{}_{}.csv".format(output, suffix))
        table.to_csv(path, index=False)
        print("Saved {}".format(path))
