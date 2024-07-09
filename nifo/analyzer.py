from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

class Analyzer:
    def __init__(self, files):
        self.files = files

    def analyze(self):
        results = {}
        for file in self.files:
            language = self.detect_language(file)

            with file.open('r', errors='ignore') as f:
                content = f.read()
                total_lines = max(content.count('\n') + 1, 0)
                code_lines = max(sum(1 for line in content.splitlines() if line.strip() and not line.strip().startswith('#')), 0)
                comment_lines = max(total_lines - code_lines, 0)

            if language not in results:
                results[language] = {"files": 0, "total_lines": 0, "code_lines": 0, "comment_lines": 0}
            
            results[language]["files"] += 1
            results[language]["total_lines"] += total_lines
            results[language]["code_lines"] += code_lines
            results[language]["comment_lines"] += comment_lines

        return results

    def detect_language(self, file):
        try:
            lexer = get_lexer_for_filename(file.name)
            language = lexer.name
            return 'txt' if language == 'Text only' else language
        except ClassNotFound:
            # if Pygments can't find a lexer, return it as an unknown file
            return file.suffix.lstrip('.').upper() or "Unknown"