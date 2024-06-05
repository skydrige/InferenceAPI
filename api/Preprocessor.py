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
        # Split the input text based on code blocks denoted by triple backticks
        blocks = re.split(r'(```.*?```)', input_text, flags=re.DOTALL)
        html_output = ""

        for block in blocks:
            if block.startswith("```") and block.endswith("```"):
                # It's a code block, strip the backticks and get the code content
                code_content = block.strip("```")
                # Extract the language if specified
                language = re.match(r'(\w+)\n', code_content)
                if language:
                    language_name = language.group(1)
                    code_content = code_content[len(language_name):].strip()
                    html_output += f"<div><strong>{language_name}</strong></div>"
                else:
                    language_name = "Code"
                    html_output += f"<div><strong>{language_name}</strong></div>"

                # Format the code block with black background and add a copy button
                html_output += f"""
                <div style="position: relative;">
                    <pre style="background-color: black; color: white; padding: 10px;"><code>{code_content}</code></pre>
                    <button onclick="copyToClipboard(this.previousElementSibling.querySelector('code').innerText)" 
                            style="position: absolute; top: 5px; right: 5px;">Copy</button>
                </div>
                <br>
                """
            else:
                # It's a normal text block, format bullet points and headers
                lines = block.split("*")
                for i, line in enumerate(lines):
                    if i % 2 == 0:
                        html_output += line.strip().replace("\n", "<br>") + "<br>"
                    else:
                        html_output += f"<ul><li>{line.strip()}</li></ul><br>"

        return html_output
