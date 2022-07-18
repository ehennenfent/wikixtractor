class Visitor:
    def visit(self, visit_me):
        for key in visit_me:
            if hasattr(self, f"visit_{key}"):
              getattr(self, f"visit_{key}")(visit_me[key])
        return self
