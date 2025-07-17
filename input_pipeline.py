import os
from typing import List, Dict, Optional

SUPPORTED_EXTENSIONS = {
    'Python': ['.py'],
    'C++': ['.cpp', '.cc', '.cxx', '.h', '.hpp'],
    'JavaScript': ['.js', '.jsx'],
    'Java': ['.java']
}

def scan_files(path: str, language: str) -> List[Dict]:
    """
    Recursively scan a file or directory for code files of the given language.
    Returns a list of dicts: {filename, code, relpath}
    """
    exts = SUPPORTED_EXTENSIONS.get(language, [])
    found = []
    if os.path.isfile(path):
        if any(path.endswith(ext) for ext in exts):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                found.append({'filename': os.path.basename(path), 'relpath': path, 'code': f.read()})
    else:
        for root, _, files in os.walk(path):
            for file in files:
                if any(file.endswith(ext) for ext in exts):
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        found.append({'filename': file, 'relpath': full_path, 'code': f.read()})
    return found 