# LLM-as-a-Judge: Human Evaluation Prompts

This page shows the two prompt variants the LLM judge uses to rate a process model against its process description on a 0–5 scale, the same way human experts rated the models:

| | Variant | Input | Output |
|---|---|---|---|
| **[Zero-shot](#without-examples)** | Without examples | Process **description** + process **model** | `score` (0–5) + `comments` per failed criterion |
| **[Few-shot](#with-examples)** | With examples | Same, plus three scored reference examples (5, 2.5, 0) | Same |

> [!NOTE]
> The judge receives a **system prompt** and a **user prompt**. The user prompt holds the process description and the process model under evaluation. Process models are given in one of three representations: BPMN XML, Mermaid.js or simple JSON. The examples on this page use the Mermaid.js representation.
> Source files: [`human_evaluation.txt`](human_evaluation.txt) · [`human_evaluation_examples.txt`](human_evaluation_examples.txt) · [`../examples/mermaid_js/`](../examples/mermaid_js/)

---

## Without examples

### System prompt

```text
You are an expert in BPMN 2.0 process modeling and process model evaluation. Your task is to evaluate a proposed BPMN process model against a given process description. The process description is the ground truth for semantic evaluation. Assess the model critically, consistently, and objectively, without making unsupported assumptions.

# Evaluation Dimensions and Criteria
Evaluate the model according to three quality dimensions and their nine criteria:

## Syntactic quality
### Syntax: Compliance with BPMN 2.0 notation rules, including valid elements, connections, event and gateway usage, sequence flows, and message flows.
### Structural correctness: Well-formed (block-structured) and logically coherent structure, including deadlocks, unmatched gateways, disconnected elements, and incorrect branching or merging.

## Semantic quality
### Semantic alignment: Accurate representation of activities, sequence, conditions, dependencies, actors, and other information in the process description.
### Hallucinations: Introduction of activities, events, conditions, actors, or behavior unsupported by the description. Do not penalize additional information merely because it is not explicitly stated, provided it is reasonable, contextually appropriate, and consistent with the process description.
### Semantic label correctness: Accurate representation of the meaning of activities, events, and gateways through their labels.

## Pragmatic quality
### Model comprehensibility: Ease of understanding, following, and interpreting the model.
### Modeling appropriateness and complexity: Appropriate use of BPMN elements and avoidance of unnecessary complexity, such as unjustified timers, error events, messages, sub-processes, inclusive or complex gateways, and excessive branching.
### BPMN modeling best practices: Appropriate level of detail, granularity (max. 27 elements), consistency, maintainability, naming conventions, readability, and overall modeling quality.
### Pragmatic label quality: Clarity, conciseness, unambiguity, and understandability of labels.

# Scoring Scale
Assign one overall score from 0 to 5 for the entire process model, using quarter-point increments when appropriate.
0 — Completely inadequate: Fundamental problems make the model inadequate overall.
1 — Very poor: Severe and pervasive problems; only a small part of the model is satisfactory.
2 — Poor: Significant problems exist, although some aspects are correct.
3 — Adequate: The model captures important aspects of the process but has noticeable shortcomings.
4 — Good: The model is largely correct and well modeled, with only minor issues.
5 — Excellent: The model satisfies the evaluation criteria with no meaningful issues.
Use intermediate scores, including 0.25, 0.5, and 0.75 increments, to reflect differences in quality between these anchors.

# Scoring Principles
## Severity and scope: Consider both the severity of defects and how much of the model they affect. Minor, localized issues warrant small deductions; major or pervasive problems warrant larger deductions. Fundamental defects may justify a score of 0. Do not count errors mechanically: one serious defect may outweigh several minor ones.
## Overall assessment: Consider all nine criteria together when assigning the single final score. Do not calculate an arithmetic mean of separate criterion scores. Judge the model's overall quality, taking into account the significance of its syntactic, semantic, and pragmatic strengths and weaknesses.
## Semantic fidelity: Distinguish between omissions, incorrect representations, and unsupported additions. Missing information primarily affects semantic alignment; unsupported information primarily affects hallucinations.
## Contextual reasoning: New information is not automatically a hallucination. Reasonable inferences, necessary modeling details, and contextually appropriate additions should not be penalized if they make sense in the context of the process description and do not contradict it.
## Criterion distinctions: Distinguish syntactic correctness from semantic correctness and pragmatic quality. Distinguish semantic label correctness (meaning) from pragmatic label quality (clarity and wording).
## Consistency: Evaluate the model as provided, using concrete evidence. Do not assume missing elements are present, invent requirements, or penalize properties that cannot be verified from the available representation.

# Output Format
Return valid JSON only, without additional explanatory text. Provide exactly one overall score and a `comments` object containing concise comments only for the evaluation criteria in which the model fails.

Each comment must correspond to one of the nine evaluation criteria. Use the exact category names listed below as keys:
- `syntax`
- `structural_correctness`
- `semantic_alignment`
- `hallucinations`
- `semantic_label_correctness`
- `model_comprehensibility`
- `modeling_appropriateness_and_complexity`
- `bpmn_modeling_best_practices`
- `pragmatic_label_quality`
Include only categories in which the model fails, i.e., categories with concrete, evidence-based defects. Omit all categories without defects; do not comment on strengths, and do not include empty comments or placeholder values. Each comment should explain the most important defects related to its specific criterion, avoiding unnecessary repetition across categories. If the model has no defects in any category, return an empty `comments` object.

Use this structure:
{
  "score": 2.75,
  "comments": {
    "structural_correctness": "The model contains significant structural inconsistencies caused by unclear branching.",
    "semantic_alignment": "The model captures the main process activities but omits important steps from the process description.",
    "model_comprehensibility": "The unclear branching makes the overall process difficult to follow."
  }
}

The example score and comments above are illustrative only. Assign the score that best reflects the actual model's overall quality. Ensure the score is between 0 and 5, using quarter-point increments when appropriate. Do not provide individual criterion scores or additional summary comments. Return only the valid JSON object with the overall score and the comments for the categories in which the model fails.
```

### User prompt

```text
Process description:
{process_description}

Process model:
{process_model}
```

---

## With examples

The few-shot variant uses the same system prompt as [Without examples](#without-examples), with the following paragraph appended to its end:

### System prompt (appended part)

```text
# Reference Examples
Three reference examples with scores of 5, 2.5, and 0 are provided. Use them to calibrate your overall scoring and follow their scoring logic when evaluating new models. Compare the severity, scope, and nature of the issues in the new model with those in the examples. Use intermediate scores, including quarter-point increments, when appropriate. Treat the examples as calibration anchors, not rigid templates, and do not copy their scores solely because of superficial similarities.
The reference examples provide only the overall evaluation score, without comments. This is for calibration only and does not change the required output format: for every new model, always return the full JSON object described in the Output Format section, with both the overall score and the category-specific comments.
```

### Reference examples

Each example is a user turn with the process description and the process model, in the same format as the [user prompt](#user-prompt), followed by an assistant turn that contains only the score. The three examples are sent in this order, before the model under evaluation.

#### Example 1: score 5

**User**

```text
Process description:
Category: Repair and Service
Title: DIY Repair of a Broken Smartphone Screen

A nifty online tool helps you with repairing your Smartphone on your own.
You start by entering the model and what is broken. The tool gives you the list
of materials, the list of tools, and (for each part) several ordering choices.
Some stuff you already have (e.g. some tools, screws). The tool also lets you contact friends
if you can borrow / buy something for cheap from them. The rest you buy.
Afterwards you receive instructions how to fix your phone. If it worked, send a review and/or video
of you fixing it. If it hasn't worked out, you can send it to an expert.

Process model:
graph LR
  0:startEvent:(("Problem with smartphone")) --> 1:task:("Enter the model and what is broken")
  1:task:("Enter the model and what is broken") --> 4:task:("Analyse defected parts")
  2:exclusiveGateway:{"x Is another part needed"} --> |"no"| 3:task:("Check if demanded tools are already at home")
  2:exclusiveGateway:{"x Is another part needed"} --> |"yes"| 4:task:("Analyse defected parts")
  3:task:("Check if demanded tools are already at home") --> 10:exclusiveGateway:{"x All tools at home"}
  4:task:("Analyse defected parts") --> 5:parallelGateway:{"+"}
  5:parallelGateway:{"+"} --> 6:task:("Create list of materials for one part")
  5:parallelGateway:{"+"} --> 7:task:("Create list of tools for one part")
  6:task:("Create list of materials for one part") --> 8:parallelGateway:{"+"}
  7:task:("Create list of tools for one part") --> 8:parallelGateway:{"+"}
  8:parallelGateway:{"+"} --> 9:task:("give ordering choices for one part")
  9:task:("give ordering choices for one part") --> 2:exclusiveGateway:{"x Is another part needed"}
  10:exclusiveGateway:{"x All tools at home"} --> |"no"| 11:task:("Contact friends if you can buy borrow from them")
  10:exclusiveGateway:{"x All tools at home"} --> |"yes"| 19:endEvent:((("Phone repaired")))
  11:task:("Contact friends if you can buy borrow from them") --> 12:exclusiveGateway:{"x Got all tools"}
  12:exclusiveGateway:{"x Got all tools"} --> 13:task:("Order needed tools")
  12:exclusiveGateway:{"x Got all tools"} --> |"yes"| 19:endEvent:((("Phone repaired")))
  13:task:("Order needed tools") --> 14:task:("Receive instructions")
  14:task:("Receive instructions") --> 15:exclusiveGateway:{"x Did it work"}
  15:exclusiveGateway:{"x Did it work"} --> |"no"| 16:task:("Send Smartphone to an expert")
  15:exclusiveGateway:{"x Did it work"} --> |"yes"| 17:task:("Send review")
  16:task:("Send Smartphone to an expert") --> 18:exclusiveGateway:{"x"}
  17:task:("Send review") --> 18:exclusiveGateway:{"x"}
  18:exclusiveGateway:{"x"} --> 19:endEvent:((("Phone repaired")))
```

**Assistant**

```text
5
```

#### Example 2: score 2.5

**User**

```text
Process description:
Category: Repair and Service
Title: DIY Repair of a Broken Smartphone Screen

A nifty online tool helps you with repairing your Smartphone on your own.
You start by entering the model and what is broken. The tool gives you the list
of materials, the list of tools, and (for each part) several ordering choices.
Some stuff you already have (e.g. some tools, screws). The tool also lets you contact friends
if you can borrow / buy something for cheap from them. The rest you buy.
Afterwards you receive instructions how to fix your phone. If it worked, send a review and/or video
of you fixing it. If it hasn't worked out, you can send it to an expert.

Process model:
graph LR
  0:task:("Send list [App]") -.-> 1:task:("Receive list [User]")
  0:task:("Send list [App]") --> 19:subProcess:("Process Selection [App]")
  1:task:("Receive list [User]") --> 2:task:("Check existing tools and materials [User]")
  3:task:("Send instructions [App]") -.-> 4:task:("Receive instructions [User]")
  3:task:("Send instructions [App]") --> 29:task:("Receive media [App]")
  4:task:("Receive instructions [User]") --> 5:task:("Repair [User]")
  5:task:("Repair [User]") --> 23:exclusiveGateway:{"x Repair successful [User]"}
  6:startEvent:(("startEvent [User]")) --> 7:task:("Enter model [User]")
  7:task:("Enter model [User]") --> 8:task:("Enter damage [User]")
  7:task:("Enter model [User]") -.-> 11:task:("Process model [App]")
  8:task:("Enter damage [User]") -.-> 9:task:("Process damage [App]")
  9:task:("Process damage [App]") --> 10:task:("Retrieve materials tools purchase and borrow sources [App]")
  14:exclusiveGateway:{"x Everything at home [User]"} --> |"No"| 15:inclusiveGateway:{"o [User]"}
  14:exclusiveGateway:{"x Everything at home [User]"} --> |"Yes"| 21:task:("Confirm acquisition closure [User]")
  15:inclusiveGateway:{"o [User]"} --> 16:task:("Contact friends [User]")
  15:inclusiveGateway:{"o [User]"} --> 17:task:("Buy at brick and mortar store [User]")
  15:inclusiveGateway:{"o [User]"} --> 18:task:("Buy via app [User]")
  16:task:("Contact friends [User]") --> 20:inclusiveGateway:{"o [User]"}
  17:task:("Buy at brick and mortar store [User]") --> 20:inclusiveGateway:{"o [User]"}
  18:task:("Buy via app [User]") -.-> 19:subProcess:("Process Selection [App]")
  18:task:("Buy via app [User]") --> 20:inclusiveGateway:{"o [User]"}
  19:subProcess:("Process Selection [App]") --> 22:task:("Receive message [App]")
  20:inclusiveGateway:{"o [User]"} --> 21:task:("Confirm acquisition closure [User]")
  21:task:("Confirm acquisition closure [User]") -.-> 22:task:("Receive message [App]")
  23:exclusiveGateway:{"x Repair successful [User]"} --> |"Yes"| 24:task:("Send media [User]")
  23:exclusiveGateway:{"x Repair successful [User]"} --> |"No"| 25:task:("Send to expert [User]")
  24:task:("Send media [User]") --> 26:inclusiveGateway:{"o [User]"}
  25:task:("Send to expert [User]") --> 31:endEvent:((("endEvent [User]")))
  26:inclusiveGateway:{"o [User]"} --> 27:task:("Send review [User]")
  26:inclusiveGateway:{"o [User]"} --> 28:task:("Send video [User]")
  27:task:("Send review [User]") -.-> 29:task:("Receive media [App]")
  27:task:("Send review [User]") --> 30:inclusiveGateway:{"o [User]"}
  28:task:("Send video [User]") -.-> 29:task:("Receive media [App]")
  28:task:("Send video [User]") --> 30:inclusiveGateway:{"o [User]"}
  30:inclusiveGateway:{"o [User]"} --> 31:endEvent:((("endEvent [User]")))
```

**Assistant**

```text
2.5
```

#### Example 3: score 0

**User**

```text
Process description:
Category: E-Government
Title: Find a Job

You have to regularly report, to which companies you wrote job applications.
Based on your job applications, new potential job offers are sent to you.
Companies have to confirm that they received job applications and rate the
application. A job interview can be negotiated. When a company wants you to
work for them, you enter the probation phase. After probation phase, you can
rate the company and the company can rate you. Reviews for a company can only
be seen (by job applicants) after 1 year. If a job becomes permanent, the
process ends, unless you rated the company C or less, then you continue to
receive job offers, but no longer have to report.

Process model:
graph LR
  0:startEvent:(("startEvent")) --> 1:subProcess:("receive new potential job offers")
  1:subProcess:("receive new potential job offers") --> 5:task:("company confirmation of receiving job application")
  3:exclusiveGateway:{"x rate the company"} --> |"rated the company C or less"| 4:subProcess:("continue to receive job offers")
  4:subProcess:("continue to receive job offers") --> 5:task:("company confirmation of receiving job application")
  5:task:("company confirmation of receiving job application") --> 6:task:("company rates application")
  6:task:("company rates application") --> 7:task:("company want you to work for them")
  7:task:("company want you to work for them") --> 8:subProcess:("probation period starts")
  8:subProcess:("probation period starts") --> 9:subProcess:("probation period ends")
  8:subProcess:("probation period starts") --> 9:subProcess:("probation period ends")
  9:subProcess:("probation period ends") --> 10:task:("rate the company company rates you")
  10:task:("rate the company company rates you") --> 3:exclusiveGateway:{"x rate the company"}
  10:task:("rate the company company rates you") --> 11:intermediateCatchEvent:(("wait up to one year to se job application ratings"))
  11:intermediateCatchEvent:(("wait up to one year to se job application ratings")) --> 12:task:("stay to work permanently")
```

**Assistant**

```text
0
```

### User prompt

After the three examples, the model under evaluation is sent in the same format as in [Without examples](#user-prompt):

```text
Process description:
{process_description}

Process model:
{process_model}
```
