from .caseconverter import CaseConverter
from .boundaries import OnDelimeterLowercaseNext, OnUpperPrecededByLowerAppendLower


class Snake(CaseConverter):

    JOIN_CHAR = "_"

    def define_boundaries(self):
        self.add_boundary_handler(
            OnDelimeterLowercaseNext(self.delimiters(), self.JOIN_CHAR)
        )
        self.add_boundary_handler(OnUpperPrecededByLowerAppendLower(self.JOIN_CHAR))

    def prepare_string(self, s):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


def snakecase(s, **kwargs):
    """Convert a string to snake case.

    Example

        Hello World => hello_world

    """
    return Snake(s, **kwargs).convert()
