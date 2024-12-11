from .caseconverter import CaseConverter
from .boundaries import OnDelimeterUppercaseNext, BoundaryHandler


class Title(CaseConverter):
    def init(self, input_buffer, output_buffer):
        # Capitalize the first character
        output_buffer.write(input_buffer.read(1).upper())

    def define_boundaries(self):
        # On delimiters, write the space and make the next character uppercase
        self.add_boundary_handler(OnDelimeterPreserveAndUpperNext(self.delimiters()))
        # Handle camelCase -> Title Case
        self.add_boundary_handler(OnUpperPrecededByLowerAddSpace())

    def prepare_string(self, s):
        if s.isupper():
            return s.lower()
        return s

    def mutate(self, c):
        return c.lower()


# Boundary handler that preserves spaces
class OnDelimeterPreserveAndUpperNext(OnDelimeterUppercaseNext):
    def __init__(self, delimiters):
        super().__init__(delimiters)
        self._delimiters = delimiters

    def handle(self, pc, cc, input_buffer, output_buffer):
        # Write a single space for any delimiter
        output_buffer.write(" ")
        # Get and capitalize the next character
        output_buffer.write(input_buffer.read(1).upper())


# New boundary handler for camelCase
class OnUpperPrecededByLowerAddSpace(BoundaryHandler):
    def is_boundary(self, pc, c):
        return pc is not None and pc.isalpha() and pc.islower() and c.isupper()

    def handle(self, pc, cc, input_buffer, output_buffer):
        output_buffer.write(" ")
        output_buffer.write(cc)


def titlecase(s, **kwargs):
    """Convert a string to title case.

    Example:
        Hello world => Hello World
        hello-world => Hello World
        helloWorld => Hello World
    """
    return Title(s, **kwargs).convert()
