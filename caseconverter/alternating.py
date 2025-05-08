from .caseconverter import CaseConverter
from .boundaries import BoundaryHandler

class Alternating(CaseConverter):

    def define_boundaries(self):
        self.add_boundary_handler(self.BoundaryOverride())

    def prepare_string(self, s):
        self._toggle_character = False
        return s.lower()

    def mutate(self, c):
        if not c.isalpha():
            return c

        if self._toggle_character:
            self._toggle_character = False
            return c.upper()
        
        self._toggle_character = True
        return c
    

    class BoundaryOverride(BoundaryHandler):
        def is_boundary(self, pc, c):
            return False
    

def alternatingcase(s, **kwargs):
    """Convert a string to alternating case, or its better known name: mocking Spongebob case.

    Example

        Hello World => hElLo WoRlD

    """
    return Alternating(s, **kwargs).convert()
