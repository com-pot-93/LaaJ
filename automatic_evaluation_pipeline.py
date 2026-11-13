import os, sys
import logging
import argparse
import time
from functools import partial

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "src"))

from automatic_evaluation import EVALUATION_TYPES, format_input, generate_prompt_gemini, generate_prompt_gpt, read
from human_evaluation_pipeline import GPT_STYLE_CALLS, SUPPORTED_LLMS, generate_gemini_with_timeout, parse_evaluation, _write_json_atomic

PROCESSES_DIR = os.path.join(BASE, "data", "llm_generated")
GROUND_TRUTH_DIR = os.path.join(PROCESSES_DIR, "ground_truth")
GENERATED_DIR = os.path.join(PROCESSES_DIR, "generated")
DESCRIPTIONS_DIR = os.path.join(PROCESSES_DIR, "process_descriptions")
GENERATION_DIR = os.path.join(BASE, "generation", "automatic")
DATASETS = ["domain", "pet", "realset"]
DESCRIPTION_EXTENSION = ".txt"
# representation -> extension of the model files in data/llm_generated
EXTENSIONS = {
    'bpmn': '.bpmn',
    'cpee': '.cpee.xml',
    'mermaid_js': '.md',
    'simple_json': '.json',
}


class Prompt:
    """Wraps an LLM's automatic evaluation prompt behind a uniform call(prompt, temperature, response_format) interface."""

    def __init__(self, llm, evaluation_type):
        if llm == 'gemini':
            system_prompt, example_strings = generate_prompt_gemini(evaluation_type)
            self.call = partial(generate_gemini_with_timeout, system_prompt, example_strings)
        elif llm in GPT_STYLE_CALLS:
            system_prompt, user_prompts, assistant_prompts = generate_prompt_gpt(evaluation_type)
            self.call = partial(GPT_STYLE_CALLS[llm], system_prompt, user_prompts, assistant_prompts)
        else:
            raise ValueError(f"Unsupported llm: {llm}")


def use_cases(dataset, extension):
    """Use cases of the dataset with a generated model in the representation, e.g. 10-10 for 10-10.bpmn."""
    directory = os.path.join(GENERATED_DIR, dataset)
    return sorted(f[:-len(extension)] for f in os.listdir(directory) if f.endswith(extension))


def build_input(evaluation_type, dataset, use_case, extension):
    """User prompt of the use case: generated vs. ground truth model (m2m) or generated model vs. process description (m2t)."""
    generated_model = read(os.path.join(GENERATED_DIR, dataset, use_case + extension))
    if evaluation_type == 'm2m':
        ground_truth_model = read(os.path.join(GROUND_TRUTH_DIR, dataset, use_case + extension))
        return format_input(evaluation_type, model_A=ground_truth_model, model_B=generated_model)
    description = read(os.path.join(DESCRIPTIONS_DIR, dataset, use_case + DESCRIPTION_EXTENSION))
    return format_input(evaluation_type, process_description=description, generated_model=generated_model)


def automatic_evaluation_pipeline(llm, representation, evaluation_type, temperature, iterations):
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger("{}Logger".format(llm.upper()))
    logger.setLevel(logging.INFO)

    prompt = Prompt(llm, evaluation_type)
    extension = EXTENSIONS[representation]

    os.makedirs(GENERATION_DIR, exist_ok=True)
    results_path = os.path.join(GENERATION_DIR, '{}_{}_{}.json'.format(evaluation_type, representation, llm))
    results = {}
    _write_json_atomic(results_path, results)

    logger.info('Starting the {} evaluation of models'.format(evaluation_type))

    for dataset in DATASETS:
        results[dataset] = {}
        cases = use_cases(dataset, extension)
        for i, use_case in enumerate(cases):
            print('--------------------------{} {}/{} {}-----------------------------------'.format(dataset, i + 1, len(cases), use_case))
            try:
                user_prompt = build_input(evaluation_type, dataset, use_case, extension)

                results[dataset][use_case] = {'iterations': {}}
                for j in range(iterations):
                    logger.info(f'Iteration {j + 1}/{iterations}: evaluating {use_case} of {dataset}')
                    start_time = time.perf_counter()
                    response = prompt.call(user_prompt, temperature, response_format=True)
                    running = time.perf_counter() - start_time
                    logger.info(f'TIME {running} for {use_case} of {dataset}')

                    evaluation = parse_evaluation(response) if response else None
                    if response and evaluation is None:
                        logger.error(f'Could not parse the evaluation in iteration {j + 1} of {use_case} of {dataset}')

                    result = {'evaluation': evaluation, 'time': running}
                    if evaluation is None:  # keep the raw llm answer only when it is not valid JSON (or missing)
                        result['response'] = response
                    results[dataset][use_case]['iterations'][j] = result

            except Exception as e:
                logger.error(f"An error occurred while processing use case {use_case} of {dataset}: {e}")

            _write_json_atomic(results_path, results)  # save after each use case

    logger.info('Completed evaluation of all models')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the generated process models automatically via an llm, with retries and timeout.")
    parser.add_argument('-l', '--llm', type=str, required=True, help='Select llm mode: {}'.format(', '.join(sorted(SUPPORTED_LLMS))))
    parser.add_argument('-r', '--representation', type=str, required=True,
                        help='Model representation: {}'.format(', '.join(EXTENSIONS)))
    parser.add_argument('-t', '--type', type=str, required=True, choices=EVALUATION_TYPES,
                        help='m2m: generated vs. ground truth model, m2t: generated model vs. process description')
    parser.add_argument('--temperature', type=float, required=False, default=0, help='Sampling temperature (default 0)')
    parser.add_argument('-i', '--iterations', type=int, required=False, default=5,
                        help='Number of evaluations per model (default 5)')

    args = parser.parse_args()
    llm = args.llm.lower()
    representation = args.representation.lower()

    if llm not in SUPPORTED_LLMS:
        print('Please check selected llm model (only {} are acceptable)!!!'.format(', '.join(sorted(SUPPORTED_LLMS))))
    elif representation not in EXTENSIONS:
        print('Please check selected representation (only {} are acceptable)!!!'.format(', '.join(EXTENSIONS)))
    else:
        automatic_evaluation_pipeline(llm, representation, args.type, args.temperature, args.iterations)
