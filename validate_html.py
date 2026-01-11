
from html.parser import HTMLParser

class DivValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.line_map = [] # To map parser position to lines

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.stack.append(self.getpos())

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.stack:
                self.stack.pop()
            else:
                self.errors.append(f"Extra closing div at {self.getpos()}")

    def validate(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.feed(content)
        
        if self.stack:
            for pos in self.stack:
                print(f"Unclosed div starting at line {pos[0]}, col {pos[1]}")
        else:
            print("All divs balanced.")

        for err in self.errors:
            print(err)

v = DivValidator()
v.validate(r"c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html")
