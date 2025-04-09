import os
import base64
from mistralai import Mistral
from pydantic import BaseModel

class XPathResult(BaseModel):
    feature_name: str    
    xpath: str

class MistralAPI:    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")        
        self.client = Mistral(api_key=self.api_key)

    def generate_xpath(self, file_path, feature_name):
        with open(file_path, 'rb') as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')

        prompt = f"""Given this base64 encoded file content:
{encoded_content}

Generate a robust XPath pattern to extract the following feature: {feature_name}
Make sure the XPath is not using index but using relative path to known element with specific text or attribute.
Return your answer in this format:{{
    "feature_name": "{feature_name}",
    "xpath": "your_xpath_here"
}}"""

        messages = [
            {"role": "system", "content": "You are an expert in HTML parsing and XPath. Provide only the requested output."},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.complete(
            model="mistral-large-latest",
            messages=messages,
            response_format=XPathResult,
            max_tokens=500,
            temperature=0
        )
        return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    api = MistralAPI('your_api_key_here')
    result = api.generate_xpath('/path/to/your/file.html', 'product_name')
    print(result)
