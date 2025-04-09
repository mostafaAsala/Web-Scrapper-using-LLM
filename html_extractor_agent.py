import requests
import os
from bs4 import BeautifulSoup
import re
import lxml.html
from pydantic import BaseModel
from mistralai import Mistral


class xpathvalues(BaseModel):
    feature_name:list[str]
    xpath: list[str]

class HTMLExtractorAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        
    def generate(self, prompt, model="mistral-large-latest", max_tokens=1000):
        
        client = Mistral(api_key=self.api_key)
        messages = [
            {"role": "system", "content": "You are an expert in HTML parsing, XPath, and regex patterns. Provide only code and explanations."},
                {"role": "user", "content": prompt}
            ]
        
        chat_response = client.chat.complete(
            model = model,
            messages = messages,
            response_format =xpathvalues,
            max_tokens=max_tokens,
            temperature=0
        )
        
        
        
        return chat_response.choices[0].message.content
    
    def extract_feature(self, html_code, feature_description):
        prompt = f"""
Given this HTML:
```
{html_code}
```

Generate a robust XPath patterns to extract the following features make sure the xpaths is not using index but using relative path to known element with specific text or attribute: {feature_description}

Return your answer in this format:
```python
# XPath solution
xpath = "your_xpath_here"

# Brief explanation of approach
```
"""
        return self.generate(prompt)
    
    def test_extraction(self, html_code, xpath=None, regex=None):
        """Test the extraction using provided XPath and/or regex"""
        results = {}
        
        if xpath:
            try:
                tree = lxml.html.fromstring(html_code)
                elements = tree.xpath(xpath)
                results["xpath_results"] = [lxml.html.tostring(el).decode() if hasattr(el, 'tag') else str(el) for el in elements]
            except Exception as e:
                results["xpath_error"] = str(e)
        
        if regex:
            try:
                matches = re.findall(regex, html_code)
                results["regex_results"] = matches
            except Exception as e:
                results["regex_error"] = str(e)
                
        return results

# Example usage
if __name__ == "__main__":
    agent = HTMLExtractorAgent('4xM2jn6RMjJqGYbkLtnwT4wmWLTU7LPa')
    html_sample = """
<div class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1" style="margin-bottom:15px"><div class="MuiGrid-root rounded jss39 MuiGrid-item"><div class="loaded"><div style="display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0"><div style="box-sizing:border-box;display:block;max-width:100%"><img style="max-width:100%;display:block;margin:0;border:none;padding:0" alt="" aria-hidden="true" role="presentation" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIi8+"></div><img alt="Typ EW-PAB Halogenfrei" src="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F4ifkqr4a3t56n543vlhi383k0u&amp;w=128&amp;q=75" decoding="async" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" srcset="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F4ifkqr4a3t56n543vlhi383k0u&amp;w=64&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F4ifkqr4a3t56n543vlhi383k0u&amp;w=128&amp;q=75 2x"></div></div></div><div class="MuiGrid-root rounded jss39 MuiGrid-item"><div class="loaded"><div style="display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0"><div style="box-sizing:border-box;display:block;max-width:100%"><img style="max-width:100%;display:block;margin:0;border:none;padding:0" alt="" aria-hidden="true" role="presentation" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIi8+"></div><img alt="Typ EW-PAB UV-beständig" src="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fvlsuagoe4h5f98ui5dm7d2le28&amp;w=128&amp;q=75" decoding="async" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" srcset="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fvlsuagoe4h5f98ui5dm7d2le28&amp;w=64&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fvlsuagoe4h5f98ui5dm7d2le28&amp;w=128&amp;q=75 2x"></div></div></div><div class="MuiGrid-root rounded jss39 MuiGrid-item"><div class="loaded"><div style="display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0"><div style="box-sizing:border-box;display:block;max-width:100%"><img style="max-width:100%;display:block;margin:0;border:none;padding:0" alt="" aria-hidden="true" role="presentation" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIi8+"></div><img alt="Typ EW-PAB Innenbereich" src="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fv67c2tpsdt22tcc6ps1gk8fe5e&amp;w=128&amp;q=75" decoding="async" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" srcset="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fv67c2tpsdt22tcc6ps1gk8fe5e&amp;w=64&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fv67c2tpsdt22tcc6ps1gk8fe5e&amp;w=128&amp;q=75 2x"></div></div></div><div class="MuiGrid-root rounded jss39 MuiGrid-item"><div class="loaded"><div style="display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0"><div style="box-sizing:border-box;display:block;max-width:100%"><img style="max-width:100%;display:block;margin:0;border:none;padding:0" alt="" aria-hidden="true" role="presentation" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIi8+"></div><img alt="Typ EW-PAB Außenbereich" src="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fvm46j66a6575pfn7j69cu6hp7o&amp;w=128&amp;q=75" decoding="async" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" srcset="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fvm46j66a6575pfn7j69cu6hp7o&amp;w=64&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fvm46j66a6575pfn7j69cu6hp7o&amp;w=128&amp;q=75 2x"></div></div></div><div class="MuiGrid-root rounded jss39 MuiGrid-item"><div class="loaded"><div style="display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0"><div style="box-sizing:border-box;display:block;max-width:100%"><img style="max-width:100%;display:block;margin:0;border:none;padding:0" alt="" aria-hidden="true" role="presentation" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIi8+"></div><img alt="Typ EW-PAB ROHS-Konform" src="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F883dds7n6h15padmd1c2m3mj5q&amp;w=128&amp;q=75" decoding="async" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" srcset="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F883dds7n6h15padmd1c2m3mj5q&amp;w=64&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F883dds7n6h15padmd1c2m3mj5q&amp;w=128&amp;q=75 2x"></div></div></div><div class="MuiGrid-root rounded jss39 MuiGrid-item" title=""><div class="loaded"><div style="display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0"><div style="box-sizing:border-box;display:block;max-width:100%"><img style="max-width:100%;display:block;margin:0;border:none;padding:0" alt="" aria-hidden="true" role="presentation" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIi8+"></div><img alt="Typ EW-PAB filters.VERBRENNUNGSBESTTEST_ECE324R118" src="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F9hecgua50t5olcmlhhfcu5v05u&amp;w=128&amp;q=75" decoding="async" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" srcset="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F9hecgua50t5olcmlhhfcu5v05u&amp;w=64&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F9hecgua50t5olcmlhhfcu5v05u&amp;w=128&amp;q=75 2x"></div></div></div><div class="MuiGrid-root rounded jss39 MuiGrid-item"><div class="loaded"><div style="display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0"><div style="box-sizing:border-box;display:block;max-width:100%"><img style="max-width:100%;display:block;margin:0;border:none;padding:0" alt="" aria-hidden="true" role="presentation" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIi8+"></div><img alt="Typ EW-PAB Bahn EU-Zulassung" src="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fvhtu84f2b563j9603inirnm157&amp;w=128&amp;q=75" decoding="async" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" srcset="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fvhtu84f2b563j9603inirnm157&amp;w=64&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fvhtu84f2b563j9603inirnm157&amp;w=128&amp;q=75 2x"></div></div></div><div class="MuiGrid-root rounded jss39 MuiGrid-item"><div class="loaded"><div style="display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0"><div style="box-sizing:border-box;display:block;max-width:100%"><img style="max-width:100%;display:block;margin:0;border:none;padding:0" alt="" aria-hidden="true" role="presentation" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIi8+"></div><img alt="Typ EW-PAB CURUS-Zulassung" src="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fa3ag8rhv1t5dj89q8377hgd26r&amp;w=128&amp;q=75" decoding="async" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" srcset="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fa3ag8rhv1t5dj89q8377hgd26r&amp;w=64&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2Fa3ag8rhv1t5dj89q8377hgd26r&amp;w=128&amp;q=75 2x"></div></div></div><div class="MuiGrid-root rounded jss39 MuiGrid-item" title=""><div class="loaded"><div style="display:inline-block;max-width:100%;overflow:hidden;position:relative;box-sizing:border-box;margin:0"><div style="box-sizing:border-box;display:block;max-width:100%"><img style="max-width:100%;display:block;margin:0;border:none;padding:0" alt="" aria-hidden="true" role="presentation" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIi8+"></div><img alt="Typ EW-PAB Hergestellt in Deutschland" src="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F070am3161p36t8kdj1oa9lqp00&amp;w=128&amp;q=75" decoding="async" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:contain" srcset="/_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F070am3161p36t8kdj1oa9lqp00&amp;w=64&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fmurrplastik.canto.global%2Fpreview%2Fimage%2F070am3161p36t8kdj1oa9lqp00&amp;w=128&amp;q=75 2x"></div></div></div></div>

"""
    result = agent.extract_feature(html_sample, "Rohs image, halogenfree image, part number")
    print(result)