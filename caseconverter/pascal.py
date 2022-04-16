from .caseconverter import CaseConverter
from .boundaries import (
    OnDelimeterUppercaseNext,
    OnUpperPrecededByLowerAppendUpper,
    OnUpperPrecededByUpperAppendCurrent,
)


class Pascal(CaseConverter):
    def init(self, input_buffer, output_buffer):
        output_buffer.write(input_buffer.read(1).upper())

    def define_boundaries(self):
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
