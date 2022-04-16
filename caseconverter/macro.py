import re
from .caseconverter import CaseConverter
from .boundaries import (
    OnDelimeterUppercaseNext,
    OnUpperPrecededByLowerAppendUpper,
    OnUpperPrecededByUpperAppendJoin,
)


class Macro(CaseConverter):

    JOIN_CHAR = "_"

    def __init__(self, *args, delims_only=False, **kwargs):
        self._delims_only = delims_only
        super(Macro, self).__init__(*args, **kwargs)

    def define_boundaries(self):
        self.add_boundary_handler(
            OnDelimeterUppercaseNext(self.delimiters(), self.JOIN_CHAR)
        )

        if not self._delims_only:
            self.add_boundary_handler(OnUpperPrecededByLowerAppendUpper(self.JOIN_CHAR))
            self.add_boundary_handler(OnUpperPrecededByUpperAppendJoin(self.JOIN_CHAR))

    def convert(self):
        if self.raw().isupper():
            return re.sub(
                "[{}]+".format(re.escape(self.delimiters())),
                self.JOIN_CHAR,
                self.raw(),
            )

        return super(Macro, self).convert()

    def mutate(self, c):
        return c.upper()


def macrocase(s, **kwargs):
    """Convert a string to macro case

    Example

        Hello World => HELLO_WORLD

    """
    return Macro(s, **kwargs).convert()
