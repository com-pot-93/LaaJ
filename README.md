# LLM-as-a-Judge (LaaJ) for Process Models

Code and data for evaluating process models with LLMs as judges. Details on the
evaluation design, metrics and statistical models are in the paper.

## Evaluation steps

The analysis is organized in four evaluation steps (investigation criteria, IC):

| Step | Question |
|------|----------|
| **IC1** | Variability across runs. |
| **IC2** | Effect of configurations on runs (LLMs, representation, random effects). |
| **IC3** | Reliability of LaaJ scores when compared to deterministic metrics. |
| **IC4** | Magnitude of similarity between LaaJ and deterministic metrics. |

Each step has its own scripts (`ic<N>_*.py`). They usually come in pairs: one
for the **deterministic metrics** evaluation (`auto` / `m2m` / `m2t`) and one for
the **human judgement** evaluation (`human`).

## Setup

The project uses [Poetry](https://python-poetry.org/) (Python 3.11):

```bash
poetry install
poetry shell
python <script.py>
```
### LLM access

LLM calls go through **Blinded Generative AI Hub** (`src/gen_ai_llm_call.py`), which
needs credentials.

Models used: GPT-5, Gemini 2.5 Pro, Claude 4.5 Opus.

To use another provider or LLM, see `src/example_openai_call.py`. It calls
OpenAI directly with the same call shape. It needs `OPENAI_API_KEY` in `.env`.

## Workflow

### 1. Generate LaaJ data

There are two types of LaaJ evaluation. Run both pipelines before any evaluation
script:

| Script | LaaJ type | Output |
|--------|-----------|--------|
| `human_evaluation_pipeline.py` | **Simulating human judgements**: the LLM grades human-created models (0–5), with or without few-shot examples | `generation/human/` |
| `automatic_evaluation_pipeline.py` | **Deterministic metrics**: the LLM scores generated models against the ground truth (m2m: similarity) and against the process description (m2t: relevance, truthfulness) | `generation/automatic/` |

```bash
python human_evaluation_pipeline.py -r bpmn -l gpt -e true        # -e false: no few-shot examples
python automatic_evaluation_pipeline.py -r cpee -l gemini -t m2m  # -t m2t for text comparison
```

`-l`: `gpt`, `gemini`, `anthropic`. `-r`: `bpmn`, `mermaid_js`, `simple_json` (+ `cpee`
for automatic). `scripts/scripts_auto.sh` and `scripts/scripts_human.sh` run all
combinations. These cripts need to be placed in root directory to be run.

### 2. Compute deterministic metrics and aggregate

| Script | Description |
|--------|-------------|
| `calculate_similarity.py` | Task, element and trace similarity between ground truth and generated models, via [cpee.org/similarity/](https://cpee.org/similarity/) → `similarity/similarity.csv` |
| `calculate_text_similarity.py` | Relevance and truthfulness of generated models w.r.t. their descriptions, via [cpee.org/similarity/text/](https://cpee.org/similarity/text/) → `similarity/text_similarity.csv` |
| `automatic_m2m_statistics.py` | Per-use-case statistics of the LLM m2m scores over iterations → `similarity/automatic/` |
| `automatic_m2t_statistics.py` | Same for m2t (relevance, truthfulness) → `similarity/automatic/` |
| `human_statistics.py` | Per-model human score and LLM score statistics → `similarity/human/` |

### 3. Evaluation (IC1–IC4)

| Step | Deterministic metrics | Human judgements |
|------|-----------------------|------------------|
| IC1, IC2 | `ic12_automatic_average_statistics.py` – mean, range, SD, CV over runs | `ic12_human_average_statistics.py` – same for human evaluation |
| IC2 | `ic2_beta_glmm_auto_predictions.py` – Beta GLMM, posterior predictions per LLM × representation | `ic2_beta_glmm_human_predictions.py` – Beta GLMM incl. few-shot factor |
| IC2 | `ic2_beta_glmm_auto_comparisons.py` – pairwise comparisons of LLMs / representations | `ic2_beta_glmm_human_comparisons.py` – pairwise comparisons incl. few-shot |
| IC3 | `ic3_deterministic_reliability_m2m.py` – correlation, MAE, ICC vs. task/element/trace | `ic3_human_reliability.py` – correlation, MAE, ICC vs. human scores |
| IC3 | `ic3_deterministic_reliability_m2t.py` – same vs. relevance/truthfulness | |
| IC3 | `ic3_source_of_difference.py` – categories of differences named by the LLM | `ic3_source_of_score.py` – criteria the LLM commented on |
| IC4 | `ic4_m2m_magnitude.py` – does agreement grow with similarity (m2m) | `ic4_human_magnitude.py` – same for human vs. LLM |
| IC4 | `ic4_m2t_magnitude.py` – same for m2t | |
| IC4 | `ic4_magnitude_mae.py` – MAE per similarity group (m2m, m2t and human) | |

The IC3 reliability scripts and the IC4 scripts accept `-r <representation> -l <llm>`
for a single configuration; without them they average over all configurations.

## Helper scripts

| Script | Description |
|--------|-------------|
| `generate_models_with_autobpmn.py` | Generates CPEE models from process descriptions, via [cpee.org/llm/](https://cpee.org/llm/) |
| `convert_generated.py` | Converts generated CPEE models to BPMN, Mermaid and simplified JSON |
| `convert_bpmn_json.py` | Converts human-created BPMN models to simplified JSON |
| `convert_bpmn_mermaid.py` | Converts human-created BPMN models to Mermaid |
| `count_models.py` | Overview of the human-created models per example (`-m full` adds quality scores) |

## Repository layout

```
data/
  human/            human-created models (bpmn, mermaid_js, simple_json) with
                    process descriptions and human quality scores
  llm_generated/    process descriptions, ground truth and LLM-generated models
                    (bpmn, cpee, mermaid, simple json) for datasets domain, pet, realset
generation/         raw LaaJ outputs (automatic/, human/)
similarity/         computed metrics and evaluation results
src/
  gen_ai_llm_call.py      LLM calls via SAP Generative AI Hub
  example_openai_call.py  example for calling OpenAI directly
  human_evaluation.py     prompt construction for human-judgement evaluation
  automatic_evaluation.py prompt construction for m2m / m2t evaluation
  bpmn_json.py, bpmn_mermaid.py  BPMN converters
  cpee_converter/         CPEE → BPMN / Mermaid / JSON converters
  prompts/                prompt templates
  examples/               few-shot examples per representation
scripts/            shell scripts to run all pipeline combinations
```

## Generative AI Disclaimer

Generative AI tools were used to assist with code formatting and structuring,
particularly for indentation and visual presentation (including the formatting
of tables printed to the console), as well as for converting text into Markdown
format for the README. Generative AI was also used to replicate scripts that
differ only in the data they process: the scripts for the m2m evaluation were
written first, and the corresponding m2t and human-evaluation variants (e.g.,
the IC scripts) were derived from them, as they differ only in the dataset and
in how the input files are read. All generated code and text were subsequently
reviewed, revised, and tested by the authors.

## License

See [LICENSE](LICENSE).
