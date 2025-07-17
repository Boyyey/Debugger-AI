from collections import Counter, defaultdict
from typing import List, Dict

class BugPatternSummarizer:
    def __init__(self):
        self.patterns = Counter()
        self.by_type = defaultdict(list)

    def summarize(self, all_explanations: List[List[Dict]]) -> Dict:
        """
        all_explanations: List of explanations per file (each is a list of dicts)
        Returns: dict with pattern counts and examples
        """
        for file_explanations in all_explanations:
            for ex in file_explanations:
                key = (ex['type'], ex['message'].split(':')[0])
                self.patterns[key] += 1
                self.by_type[ex['type']].append(ex['message'])
        top_patterns = self.patterns.most_common(10)
        summary = {
            'top_patterns': [
                {'type': t[0][0], 'pattern': t[0][1], 'count': t[1]} for t in top_patterns
            ],
            'by_type': {k: v[:5] for k, v in self.by_type.items()}
        }
        return summary 