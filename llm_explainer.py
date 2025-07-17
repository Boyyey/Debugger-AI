import openai
from typing import List, Dict

EXPLANATION_DEPTHS = [
    'Beginner',
    'Intermediate',
    'Expert',
    'Explain like I’m 12'
]

class LLMExplainer:
    def __init__(self, api_key: str, depth: str = 'Intermediate'):
        openai.api_key = api_key
        self.depth = depth

    def explain_findings(self, code: str, findings: List[Dict]) -> List[Dict]:
        explanations = []
        for finding in findings:
            prompt = self._build_prompt(code, finding)
            response = self._call_openai(prompt)
            fix = self._extract_fix(response)
            explanations.append({
                'line': finding['line'],
                'type': finding['type'],
                'message': finding['message'],
                'explanation': response,
                'fix': fix
            })
        return explanations

    def _build_prompt(self, code: str, finding: Dict) -> str:
        style = {
            'Beginner': 'Explain in simple terms for a beginner programmer.',
            'Intermediate': 'Explain clearly for someone with some programming experience.',
            'Expert': 'Give a detailed, technical explanation for an expert.',
            'Explain like I’m 12': 'Explain as if teaching a 12-year-old, using analogies and simple language.'
        }[self.depth]
        return f"""
You are an AI coding tutor. {style}\nExplain why this code triggers a {finding['type']} error at line {finding['line']}:

Code:
```python
{code}
```

Error message: {finding['message']}

Explain the bug, suggest a fix, and explain the concept behind the bug. Output the fixed code in a separate code block if possible.
"""

    def _call_openai(self, prompt: str) -> str:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.2
        )
        content = response.choices[0].message.content
        return content.strip() if content else ""

    def _extract_fix(self, response: str) -> str:
        import re
        code_blocks = re.findall(r'```(?:python)?\n([\s\S]+?)```', response)
        if len(code_blocks) > 1:
            return code_blocks[1].strip()
        elif code_blocks:
            return code_blocks[0].strip()
        return "" 