import os
import argparse

import numpy as np
import pandas as pd
import pingouin as pg
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
STATISTICS_DIR = os.path.join(BASE, "similarity", "automatic")
SIMILARITY_FILE = os.path.join(BASE, "similarity", "similarity.csv")
OUTPUT_DIR = os.path.join(BASE, "similarity")
REPRESENTATIONS = ["bpmn", "cpee", "mermaid_js", "simple_json"]
LLMS = ["anthropic", "gemini", "gpt"]
REPORT = "m2m_{}_{}.csv"
SIM_TYPES = ["task", "element", "trace"]
ALL = "all"


def llm_similarity(representation, llm):
    """llm similarity per use case: the mean column of one report, or averaged over all 12 reports (all = only use cases
    that are present in all of them)."""
    if representation != ALL:
        report = pd.read_csv(os.path.join(STATISTICS_DIR, REPORT.format(representation, llm)))
        return report.set_index("file name")["mean"]

    columns = [pd.read_csv(os.path.join(STATISTICS_DIR, REPORT.format(r, l))).set_index("file name")["mean"]
               for r in REPRESENTATIONS for l in LLMS]
    return pd.concat(columns, axis=1).dropna().mean(axis=1)


def icc_3_1(x, y):
    """ICC(3,1) of two raters (Shrout & Fleiss 1979: two-way mixed, consistency, single rater) and its p value:
    H0: ICC(3,1) = 0, calculated with pingouin (row ICC(C,1), which is ICC(3,1) in the McGraw & Wong naming)."""
    n = len(x)
    ratings = pd.DataFrame({
        "model": list(range(n)) * 2,
        "rater": ["llm"] * n + ["calculated"] * n,
        "score": list(x) + list(y),
    })
    row = pg.intraclass_corr(data=ratings, targets="model", raters="rater", ratings="score").set_index("Type").loc["ICC(C,1)"]
    return row["ICC"], row["pval"]


def p_value(p):
    """p value with 3 significant digits, small values in scientific notation (e.g. 0.0312, 4.27e-09)."""
    return "{:.3g}".format(p)


def agreement(llm, other, name):
    pairs = pd.concat([llm, other], axis=1, join="inner").dropna()
    x, y = pairs.iloc[:, 0].to_numpy(), pairs.iloc[:, 1].to_numpy()
    pearson, pearson_p = stats.pearsonr(x, y)
    spearman, spearman_p = stats.spearmanr(x, y)
    icc, icc_p = icc_3_1(x, y)
    return {
        "pair": "llm*{}".format(name),
        "n": len(pairs),
        "pearson": round(pearson, 4),
        "pearson_p": p_value(pearson_p),
        "spearman": round(spearman, 4),
        "spearman_p": p_value(spearman_p),
        "mae": round(float(np.abs(x - y).mean()), 4),
        "icc_3_1": round(icc, 4),
        "icc_3_1_p": p_value(icc_p),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agreement of the llm similarity with the calculated similarities.")
    parser.add_argument('-r', '--representation', type=str, required=False, default=ALL,
                        help='Representation: {} (default {}: averaged over all)'.format(', '.join(REPRESENTATIONS), ALL))
    parser.add_argument('-l', '--llm', type=str, required=False, default=ALL,
                        help='Llm: {} (default {}: averaged over all)'.format(', '.join(LLMS), ALL))
    args = parser.parse_args()

    if (args.representation == ALL) != (args.llm == ALL):
        parser.error("pass both -r and -l, or none of them")
    if args.representation != ALL and (args.representation not in REPRESENTATIONS or args.llm not in LLMS):
        parser.error("representation has to be one of {}, llm one of {}".format(REPRESENTATIONS, LLMS))

    llm = llm_similarity(args.representation, args.llm)
    similarity = pd.read_csv(SIMILARITY_FILE).set_index("file name")
    table = pd.DataFrame([agreement(llm, similarity[sim_type], sim_type) for sim_type in SIM_TYPES])
    print(table.to_string(index=False))

    name = "correlation_llm_{}.csv".format(ALL if args.representation == ALL else "{}_{}".format(args.representation, args.llm))
    path = os.path.join(OUTPUT_DIR, name)
    table.to_csv(path, index=False)
    print("Saved {}".format(path))
