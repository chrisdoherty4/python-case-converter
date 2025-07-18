from .caseconverter import CaseConverter
from .boundaries import (
    BoundaryHandler,
    OnDelimeterUppercaseNext,
    OnUpperPrecededByLowerAppendUpper,
    OnUpperPrecededByUpperAppendCurrent,
)

class OnFirstCharUpper(BoundaryHandler):
    """Boundary handler that ensures the first character is uppercase."""

    def is_boundary(self, pc, c):
        return pc is None

    def handle(self, pc, cc, input_buffer, output_buffer):
        output_buffer.write(cc.upper())


class Pascal(CaseConverter):

    def define_boundaries(self):
        self.add_boundary_handler(OnFirstCharUpper())
        self.add_boundary_handler(OnDelimeterUppercaseNext(self.delimiters()))
        self.add_boundary_handler(OnUpperPrecededByLowerAppendUpper())
        self.add_boundary_handler(OnUpperPrecededByUpperAppendCurrent())

    def prepare_string(self, s):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


def pascalcase(s, **kwargs):
    """Convert a string to pascal case

    Example

        Hello World => HelloWorld
        hello world => HelloWorld

    """
    return Pascal(s, **kwargs).convert()
