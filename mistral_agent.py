import requests
import os
from mistralai import Mistral

class MistralAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        
    def generate(self, prompt, model="mistral-large-latest", max_tokens=1000):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. that respond with only code, ready for execution with docs commented."},
                {"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def execute_code_task(self, task_description):
        prompt = f"Generate code to accomplish the following task: {task_description}"
        return self.generate(prompt)

# Example usage
if __name__ == "__main__":
    agent = MistralAgent('4xM2jn6RMjJqGYbkLtnwT4wmWLTU7LPa')
    result = agent.execute_code_task("Create a function to calculate fibonacci numbers")
    print(result)