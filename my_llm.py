import ollama

def run_think(ocr_results, options, prompt):
    print(prompt)
    response = ollama.generate(model='gemma3:4b', prompt=prompt)
    llm_output = response['response'].strip()
    run_decision(llm_output)

def run_decision(command):
    print(f'\n--LLM DECISION: {command}')
    if command == 'hello':
        print('Hello! How Are you?')
    if command == 'goodbye':
        print('Goodbye')
        quit()
    else:
        print('--COMMAND ERROR')