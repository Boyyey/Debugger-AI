import subprocess
import tempfile
import re
from typing import List, Dict

class StaticAnalyzer:
    @staticmethod
    def analyze_code(code: str, language: str, filename: str = "temp") -> List[Dict]:
        if language == 'Python':
            return StaticAnalyzer._analyze_python(code)
        elif language == 'C++':
            return StaticAnalyzer._analyze_cpp(code, filename)
        elif language == 'JavaScript':
            return StaticAnalyzer._analyze_js(code, filename)
        elif language == 'Java':
            return StaticAnalyzer._analyze_java(code, filename)
        else:
            return []

    @staticmethod
    def _analyze_python(code: str) -> List[Dict]:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            tmp_name = tmp.name
        try:
            result = subprocess.run([
                'pylint', tmp_name, '--output-format=text', '--score=n', '--disable=all', '--enable=E,W,C,R'
            ], capture_output=True, text=True)
            findings = []
            for line in result.stdout.splitlines():
                # Match: filename:lineno:col: type: message
                m = re.match(r'^(.*?):(\d+):(\d*):\s*([A-Z]\d+):\s*(.*)$', line)
                if m:
                    _, lineno, _, msg_type, msg = m.groups()
                    findings.append({
                        'line': int(lineno),
                        'type': msg_type,
                        'message': msg
                    })
            return findings
        finally:
            import os
            os.unlink(tmp_name)

    @staticmethod
    def _analyze_cpp(code: str, filename: str) -> List[Dict]:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            tmp_name = tmp.name
        try:
            result = subprocess.run([
                'clang-tidy', tmp_name, '--', '-std=c++17'
            ], capture_output=True, text=True)
            findings = []
            for line in result.stdout.splitlines():
                # Match: filename:lineno:col: error|warning|note: message
                m = re.match(r'^(.*?):(\d+):(\d*):\s*(error|warning|note):\s*(.*)$', line)
                if m:
                    _, lineno, _, msg_type, msg = m.groups()
                    findings.append({
                        'line': int(lineno),
                        'type': msg_type,
                        'message': msg
                    })
            return findings
        finally:
            import os
            os.unlink(tmp_name)

    @staticmethod
    def _analyze_js(code: str, filename: str) -> List[Dict]:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            tmp_name = tmp.name
        try:
            result = subprocess.run([
                'eslint', tmp_name, '--format', 'compact'
            ], capture_output=True, text=True)
            findings = []
            for line in result.stdout.splitlines():
                # Match: filename:lineno:col: message [type]
                m = re.match(r'^(.*?):(\d+):(\d+):\s*(.*)\s\[(.*)\]$', line)
                if m:
                    _, lineno, _, msg, msg_type = m.groups()
                    findings.append({
                        'line': int(lineno),
                        'type': msg_type,
                        'message': msg
                    })
            return findings
        finally:
            import os
            os.unlink(tmp_name)

    @staticmethod
    def _analyze_java(code: str, filename: str) -> List[Dict]:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            tmp_name = tmp.name
        try:
            result = subprocess.run([
                'checkstyle', '-f', 'plain', tmp_name
            ], capture_output=True, text=True)
            findings = []
            for line in result.stdout.splitlines():
                # Match: [ERROR] filename:lineno:col: message
                m = re.match(r'^\[.*?\]\s*(.*?):(\d+):(\d*):\s*(.*)$', line)
                if m:
                    _, lineno, _, msg = m.groups()
                    findings.append({
                        'line': int(lineno),
                        'type': 'checkstyle',
                        'message': msg
                    })
            return findings
        finally:
            import os
            os.unlink(tmp_name) 