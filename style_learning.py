import re
from typing import List, Dict

class StyleLearner:
    def __init__(self):
        self.metrics = {}

    def analyze_codebase(self, code_files: List[Dict]) -> Dict:
        """
        Analyze codebase style: indentation, naming, docstrings, line length, etc.
        Returns a dict of style metrics and suggestions.
        """
        indent_counts = []
        max_line_lengths = []
        snake_case = camel_case = pascal_case = 0
        docstring_count = 0
        for file in code_files:
            lines = file['code'].splitlines()
            for line in lines:
                if line.startswith(' '):
                    indent_counts.append(len(line) - len(line.lstrip(' ')))
                max_line_lengths.append(len(line))
                # Naming conventions
                for match in re.findall(r'def ([a-zA-Z_][a-zA-Z0-9_]*)', line):
                    if '_' in match:
                        snake_case += 1
                    elif match and match[0].isupper():
                        pascal_case += 1
                    else:
                        camel_case += 1
                # Docstrings
                if '"""' in line or "'''" in line:
                    docstring_count += 1
        avg_indent = sum(indent_counts) / len(indent_counts) if indent_counts else 0
        avg_line_length = sum(max_line_lengths) / len(max_line_lengths) if max_line_lengths else 0
        total_funcs = snake_case + camel_case + pascal_case
        self.metrics = {
            'avg_indent': avg_indent,
            'avg_line_length': avg_line_length,
            'snake_case': snake_case,
            'camel_case': camel_case,
            'pascal_case': pascal_case,
            'docstring_count': docstring_count,
            'total_funcs': total_funcs
        }
        suggestions = self._style_suggestions()
        return {'metrics': self.metrics, 'suggestions': suggestions}

    def _style_suggestions(self) -> List[str]:
        s = []
        if self.metrics.get('avg_indent', 0) not in (2, 4):
            s.append(f"Consider using 4 spaces for indentation (found avg: {self.metrics.get('avg_indent', 0):.1f})")
        if self.metrics.get('avg_line_length', 0) > 100:
            s.append("Consider limiting line length to 100 characters.")
        if self.metrics.get('snake_case', 0) < self.metrics.get('total_funcs', 0) * 0.8:
            s.append("Most functions should use snake_case naming.")
        if self.metrics.get('docstring_count', 0) < self.metrics.get('total_funcs', 0) * 0.5:
            s.append("Add more docstrings to your functions/classes.")
        return s 