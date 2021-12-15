import xml.etree.ElementTree as ET
from mwparserfromhell import parse
import sys

class Visitor:

    def __init__(self, node=None):
        if node is not None:
            self.visit(node)

    def visit(self, node):
        for child in node:
            method_name = f"visit_{child.tag}"
            if hasattr(self, method_name):
                getattr(self, method_name)(child)

class PageVisitor(Visitor):

    def __init__(self, node=None):
        self.id = None
        self.title = None
        self.text = None

        super().__init__(node)

    def visit_id(self, node):
        self.id = int(node.text)

    def visit_title(self, node):
        self.title = node.text

    def visit_revision(self, node):
        visitor = RevisionVisitor(node)
        self.text = visitor.text
        self.short_text = str(visitor)

    def __str__(self):
        return f"Page {self.id}: {self.title}\n  {self.short_text}"

class RevisionVisitor(Visitor):

    def __init__(self, node=None):
        self.timestamp = None
        self.format = None
        self.model = None
        self.text = None

        super().__init__(node)

    def visit_timestamp(self, node):
        self.timestamp = node.text

    def visit_format(self, node):
        self.format = node.text

    def visit_model(self, node):
        self.model = node.text
    
    def visit_text(self, node):
        if self.format == "text/x-wiki":
            self.text = parse(node.text)

    def __str__(self):
        if self.text is not None:
            as_str = str(self.text).encode("unicode_escape").decode("utf-8")
            return as_str[:128] + ("..." if len(as_str) > 64 else "")
        else:
            return f"{self.model} page ({self.format})"

tree = ET.parse(sys.argv[1])
for child in tree.getroot():
    visitor = PageVisitor(child)
    wikitext = visitor.text
    for template in wikitext.filter_templates(recursive=False):
        # print(template.name)
        if "Infobox" in (name := template.name.strip()):
            print(visitor.title, "::", name)
            # print(" ",template. get(1).value)
