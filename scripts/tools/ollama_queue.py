import requests
import json
from pathlib import Path
from datetime import datetime

OLLAMA_API_URL = 'http://localhost:11434/api/generate'
MODEL = 'codellama:7b'
RESULTS_DIR = Path('results')
LOG_FILE = Path('results/ollama_queue.log')

# Пример очереди задач (можно заменить на чтение из файла)
tasks = [
    {
        'prompt': 'Write a pytest test for a function that adds two numbers.',
        'task_id': 'test_add_function'
    },
    {
        'prompt': 'Explain what the following Python code does: def foo(x): return x * 2',
        'task_id': 'explain_foo'
    }
]

RESULTS_DIR.mkdir(exist_ok=True)

def log_event(event):
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} | {event}\n")

def send_to_ollama(prompt, model=MODEL):
    payload = {
        'model': model,
        'prompt': prompt,
        'stream': False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    return response.json()['response']

def main():
    for task in tasks:
        log_event(f"START task {task['task_id']}")
        try:
            result = send_to_ollama(task['prompt'])
            result_file = RESULTS_DIR / f"{task['task_id']}.txt"
            with result_file.open('w', encoding='utf-8') as f:
                f.write(result)
            log_event(f"SUCCESS task {task['task_id']} -> {result_file}")
        except Exception as e:
            log_event(f"ERROR task {task['task_id']}: {e}")

if __name__ == '__main__':
    main() 