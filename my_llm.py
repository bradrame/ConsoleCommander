import ollama
import re

def run_think(ocr_results, prompt):
    global llm_output
    response = ollama.generate(model='qwen3:8b', prompt=prompt, stream=False)
    llm_output = re.sub(r'<think>.*?</think>\s*', '', response["response"].strip(), flags=re.DOTALL)
    return llm_output