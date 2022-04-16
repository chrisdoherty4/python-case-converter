from .caseconverter import CaseConverter
from .boundaries import OnDelimeterLowercaseNext, OnUpperPrecededByLowerAppendLower


class Flat(CaseConverter):
    def define_boundaries(self):
        self.add_boundary_handler(OnDelimeterLowercaseNext(self.delimiters()))
        self.add_boundary_handler(OnUpperPrecededByLowerAppendLower())

    def prepare_string(self, s):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


def flatcase(s, **kwargs):
    """Convert a string to flat case

    Example

        Hello World => helloworld

    """
    return Flat(s, **kwargs).convert()
