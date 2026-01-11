
from html.parser import HTMLParser

class SlideNestingValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slide_depth = 0
        self.nested_error = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            is_slide = False
            for attr in attrs:
                if attr[0] == 'class' and 'slide' in attr[1].split():
                    is_slide = True
                    break
            
            if is_slide:
                if self.slide_depth > 0:
                    print(f"CRITICAL: Nested slide detected at line {self.getpos()[0]} inside another slide!")
                    self.nested_error = True
                self.slide_depth += 1

    def handle_endtag(self, tag):
        if tag == 'div':
            # We can't know for sure if it's the slide closing div without tracking all divs, 
            # but for this specific bug finding, we assume standard indentation/structural sanity 
            # isn't perfect.
            # actually this logic is flawed because we need to track *all* divs to know when the slide div closes.
            pass

# Better approach: precise stack tracking
class StrictSlideValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.div_stack = [] # boolean stack: True if it's a slide, False otherwise
        self.slide_active = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            is_slide = False
            for attr in attrs:
                if attr[0] == 'class' and 'slide' in attr[1].split() and 'slide-content' not in attr[1].split() and 'slide-number' not in attr[1].split():
                    is_slide = True
            
            if is_slide:
                if self.slide_active:
                    print(f"CRITICAL: Nested slide detected at line {self.getpos()[0]}")
                self.slide_active = True
                self.div_stack.append(True)
            else:
                self.div_stack.append(False)

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.div_stack:
                was_slide = self.div_stack.pop()
                if was_slide:
                    self.slide_active = False

v = StrictSlideValidator()
with open(r"c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html", 'r', encoding='utf-8') as f:
    v.feed(f.read())
print("Nesting check complete.")
