import re
import markdown
from bs4 import BeautifulSoup


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

    def formater(self, md_text):
        """Convert Markdown text to HTML with proper code block handling and copy buttons."""
        html_output = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

        # Inject copy buttons and language labels into the code blocks
        def add_copy_button_and_language_label(html):
            soup = BeautifulSoup(html, 'html.parser')
            for pre in soup.find_all('pre'):
                code = pre.find('code')
                if code:
                    # Determine the language from the class name
                    lang_class = next((cls for cls in code.get('class', []) if cls.startswith('language-')), None)
                    lang = lang_class.split('-')[1] if lang_class else 'shell'

                    container = soup.new_tag('div', **{'class': 'code-container'})
                    copy_button = soup.new_tag('button', **{'class': 'copy-button'})
                    copy_button.string = 'Copy'

                    language_label = soup.new_tag('div', **{'class': 'language-label'})
                    language_label.string = lang

                    pre.wrap(container)
                    container.insert(0, language_label)
                    container.append(copy_button)
            return str(soup)

        html_output = add_copy_button_and_language_label(html_output)
        return html_output

