import re
import string
import logging
import sys
from io import StringIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s : %(name)s : %(levelname)s : %(message)s")

ch.setFormatter(formatter)

logger.addHandler(ch)


# 1. Is there a subset of token separation characters? -
# 2. How do we handle repeat separators? -
# 3. Should we strip punctuation? -
# 4. How do we handle integers?


class StringBuffer(StringIO):
    def write(self, s):
        super(StringBuffer, self).write(s)


DELIMETERS = " -_"


def stripable_punctuation(delimeters):
    """Construct a string of stripable punctuation based on delimeters.
    """
    return "".join([c for c in string.punctuation if c not in delimeters])


class BoundaryHandler(object):
    def is_boundary(self, pc, c):
        raise NotImplementedError()

    def handle(self, pc, cc, input_buffer, output_buffer):
        raise NotImplementedError()


class CaseConverter(object):
    def __init__(self, s, delimeters=DELIMETERS, strip_punctuation=True):
        self._delimeters = delimeters

        s = s.strip(delimeters)

        if strip_punctuation:
            punctuation = stripable_punctuation(delimeters)
            s = re.sub("[{}]+".format(re.escape(punctuation)), "", s)

        # Change recurring delimeters into single delimeters.
        s = re.sub("[{}]+".format(re.escape(delimeters)), delimeters[0], s)

        self._raw_input = s
        self._input_buffer = StringBuffer(self.prepare_string(s))
        self._output_buffer = StringBuffer()
        self._boundary_handlers = []

        self.define_boundaries()

    def add_boundary_handler(self, handler):
        self._boundary_handlers.append(handler)

    def define_boundaries(self):
        logger.warn("No boundaries defined")
        return

    def delimeters(self):
        return self._delimeters

    def raw(self):
        return self._raw_input

    def init(self, input_buffer, output_buffer):
        """Initialize the output buffer
        """
        return

    def mutate(self, c):
        """Whenever we write a character to the buffer, optionally mutate.
        """
        return c

    def prepare_string(self, s) -> str:
        """Prepare the raw intput string for operation
        """
        return s

    def handle_boundary(self, pc, cc, input_buffer, output_buffer):
        """When we find a boundary as defined by `is_boundary()` then handle it.
        
        :param pc: Previous character
        :param cc: Current character
        :param input_buffer: Input buffer wrapped around raw input string.
        :param output_buffer: Output buffer for storing transformed string.
        """
        for bh in self._boundary_handlers:
            if bh.is_boundary(cc):
                bh.handle(pc, cc, input_buffer, output_buffer)
                return

    def is_boundary(self, pc, c):
        """Determine if we've hit a boundary or not.
        """
        for bh in self._boundary_handlers:
            if bh.is_boundary(pc, c):
                return bh

        return None

    def convert(self) -> str:
        """Handle converting the input string to an output string.
        """
        self.init(self._input_buffer, self._output_buffer)

        logger.debug("input_buffer = {}".format(self._input_buffer.getvalue()))

        # Previous character (pc) and current character (cc)
        pc = None
        cc = self._input_buffer.read(1)

        while cc:
            logger.debug(
                "pc = '{}'; cc = '{}'; input_buffer.tell() = {}; output_buffer = '{}'".format(
                    pc, cc, self._input_buffer.tell(), self._output_buffer.getvalue()
                )
            )
            bh = self.is_boundary(pc, cc)
            if bh:
                bh.handle(pc, cc, self._input_buffer, self._output_buffer)
            else:
                self._output_buffer.write(self.mutate(cc))

            pc = cc
            cc = self._input_buffer.read(1)

        return self._output_buffer.getvalue()


class OnDelimeterUppercaseNext(BoundaryHandler):
    def __init__(self, delimeters, join_char=""):
        self._delimeters = delimeters
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return c in self._delimeters

    def handle(self, pc, cc, input_buffer, output_buffer):
        output_buffer.write(self._join_char)
        output_buffer.write(input_buffer.read(1).upper())


class OnDelimeterLowercaseNext(BoundaryHandler):
    def __init__(self, delimeters, join_char=""):
        self._delimeters = delimeters
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return c in self._delimeters

    def handle(self, pc, cc, input_buffer, output_buffer):
        output_buffer.write(self._join_char)
        output_buffer.write(input_buffer.read(1).lower())


class OnUpperPrecededByLowerAppendUpper(BoundaryHandler):
    def __init__(self, join_char=""):
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return pc != None and pc.isalpha() and pc.islower() and c.isupper()

    def handle(self, pc, cc, input_buffer, output_buffer):
        output_buffer.write(self._join_char)
        output_buffer.write(cc)


class OnUpperPrecededByLowerAppendLower(BoundaryHandler):
    def __init__(self, join_char=""):
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return pc != None and pc.isalpha() and pc.islower() and c.isupper()

    def handle(self, pc, cc, input_buffer, output_buffer):
        output_buffer.write(self._join_char)
        output_buffer.write(cc.lower())


class Camel(CaseConverter):
    def define_boundaries(self):
        self.add_boundary_handler(OnDelimeterUppercaseNext(self.delimeters()))
        self.add_boundary_handler(OnUpperPrecededByLowerAppendUpper())

    def prepare_string(self, s):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


class Pascal(Camel):
    def init(self, input_buffer, output_buffer):
        output_buffer.write(input_buffer.read(1).upper())


class Snake(CaseConverter):

    JOIN_CHAR = "_"

    def define_boundaries(self):
        self.add_boundary_handler(
            OnDelimeterLowercaseNext(self.delimeters(), self.JOIN_CHAR)
        )
        self.add_boundary_handler(OnUpperPrecededByLowerAppendLower(self.JOIN_CHAR))

    def prepare_string(self, s):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


class Flat(Snake):

    JOIN_CHAR = ""


class Kebab(Snake):

    JOIN_CHAR = "-"


class Cobol(CaseConverter):

    JOIN_CHAR = "-"

    def define_boundaries(self):
        self.add_boundary_handler(
            OnDelimeterUppercaseNext(self.delimeters(), self.JOIN_CHAR)
        )
        self.add_boundary_handler(OnUpperPrecededByLowerAppendUpper(self.JOIN_CHAR))

    def convert(self):
        if self.raw().isupper():
            return re.sub(
                "[{}]+".format(re.escape(self.delimeters())),
                self.JOIN_CHAR,
                self.raw(),
            )

        return super(Cobol, self).convert()

    def mutate(self, c):
        return c.upper()


class Macro(Cobol):

    JOIN_CHAR = "_"


def camel_case(s, delims=DELIMETERS, strip_punctuation=True):
    """Convert a string to camel case.

    Example
    
      Hello World => helloWorld

    """
    return Camel(s, delimeters=delims, strip_punctuation=strip_punctuation).convert()


def cobol_case(s, delims=DELIMETERS, strip_punctuation=True):
    """Convert a string to cobol case

    Example

      Hello World => HELLO-WORLD

    """
    return Cobol(s, delimeters=delims, strip_punctuation=strip_punctuation).convert()


def macro_case(s, delims=DELIMETERS, strip_punctuation=True):
    """Convert a string to macro case

    Example

        Hello World => HELLO_WORLD

    """
    return Macro(s, delimeters=delims, strip_punctuation=strip_punctuation).convert()


def snake_case(s, delims=DELIMETERS, strip_punctuation=True):
    """Convert a string to snake case.

    Example

        Hello World => hello_world

    """
    return Snake(s, delimeters=delims, strip_punctuation=strip_punctuation).convert()


def pascal_case(s, delims=DELIMETERS, strip_punctuation=True):
    """Convert a string to pascal case

    Example

        Hello World => HelloWorld
        hello world => HelloWorld

    """
    return Pascal(s, delimeters=delims, strip_punctuation=strip_punctuation).convert()


def flat_case(s, delims=DELIMETERS, strip_punctuation=True):
    """Convert a string to flat case

    Example

        Hello World => helloworld

    """
    return Flat(s, delimeters=delims, strip_punctuation=strip_punctuation).convert()


def kebab_case(s, delims=DELIMETERS, strip_punctuation=True):
    """Convert a string to kebab case

    Example

        Hello World => hello-world

    """
    return Kebab(s, delimeters=delims, strip_punctuation=strip_punctuation).convert()
