#!/bin/bash

python automatic_evaluation_pipeline.py -r mermaid_js -l gpt -t m2t
python automatic_evaluation_pipeline.py -r cpee -l gpt -t m2m
python automatic_evaluation_pipeline.py -r cpee -l gpt -t m2t
python automatic_evaluation_pipeline.py -r bpmn -l gpt -t m2m
python automatic_evaluation_pipeline.py -r bpmn -l gpt -t m2t
python automatic_evaluation_pipeline.py -r simple_json -l gpt -t m2m
python automatic_evaluation_pipeline.py -r simple_json -l gpt -t m2t

python automatic_evaluation_pipeline.py -r mermaid_js -l gemini -t m2m
python automatic_evaluation_pipeline.py -r mermaid_js -l gemini -t m2t
python automatic_evaluation_pipeline.py -r cpee -l gemini -t m2m
python automatic_evaluation_pipeline.py -r cpee -l gemini -t m2t
python automatic_evaluation_pipeline.py -r bpmn -l gemini -t m2m
python automatic_evaluation_pipeline.py -r bpmn -l gemini -t m2t
python automatic_evaluation_pipeline.py -r simple_json -l gemini -t m2m
python automatic_evaluation_pipeline.py -r simple_json -l gemini -t m2t

python automatic_evaluation_pipeline.py -r mermaid_js -l anthropic -t m2m
python automatic_evaluation_pipeline.py -r mermaid_js -l anthropic -t m2t
python automatic_evaluation_pipeline.py -r cpee -l anthropic -t m2m
python automatic_evaluation_pipeline.py -r cpee -l anthropic -t m2t
python automatic_evaluation_pipeline.py -r bpmn -l anthropic -t m2m
python automatic_evaluation_pipeline.py -r bpmn -l anthropic -t m2t
python automatic_evaluation_pipeline.py -r simple_json -l anthropic -t m2m
python automatic_evaluation_pipeline.py -r simple_json -l anthropic -t m2t

