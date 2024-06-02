import re


class Preprocessor:
    def __init__(self):
        pass

    def clean(self, text):
        text = re.sub(r'\[\d+]', '', text)
        text = re.sub(r'\{.*?}', '', text)
        text = re.sub(r'\$.*?\$', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s.,;!?-]', '', text)
        text = re.sub(r'\\sqrt|\\sum|\\pi|\\frac|\\begin\{equation}|\\end\{equation}', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.split(r'\nReferences', text, flags=re.I)[0]
        return text

    def formater(self, input_text):
        lines = input_text.split("**")
        html_output = ""
        for i, line in enumerate(lines):
            if i % 2 == 0:
                html_output += line.strip() + "<br>"
            else:
                html_output += f"<h2>{line.strip()}</h2><br>"
        return html_output
