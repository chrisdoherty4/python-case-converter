import re
import string
import logging
import sys
from io import StringIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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


DELIMITERS = " -_"


def stripable_punctuation(delimiters):
    """Construct a string of stripable punctuation based on delimiters.
    """
    return "".join([c for c in string.punctuation if c not in delimiters])


class BoundaryHandler(object):
    """A boundary handler that both detects and handles a boundary.

    The BoundaryHandler is an interface for a CaseConverter instance.
    """

    def is_boundary(self, pc, c):
        """Determine if we're on a boundary.

        :param pc: Previous character
        :param cc: Current character
        :return: True if a boundary is found, else false.
        :rtype: boolean
        """
        raise NotImplementedError()

    def handle(self, pc, cc, input_buffer, output_buffer):
        """Handle a detected boundary.

        :param pc: Previous character
        :type pc: str
        :param cc: Current character
        :type cc: str
        :param input_buffer: The raw string wrapped in a buffer.
        :type input_buffer: StringBuffer
        :param output_buffer: The output buffer that stores the new string as
            it's constructed.
        :type output_buffer: StringBuffer
        """
        raise NotImplementedError()


class CaseConverter(object):
    def __init__(self, s, delimiters=DELIMITERS, strip_punctuation=True):
        """Initialize a case conversion.

        On initialization, punctuation can be optionally stripped. If punctuation
        is seen in the input string it will appear in the same position in
        the output string.

        BoundaryHandlers should take into consideration whether or not
        they are evaluating the first character in a string and whether or
        not a character is punctuation.

        Delimeters will not be stripped if strip_punctuation is true.

        During initialization the raw input string will be passed through 
        the prepare_string() method. Child classes should overwrite this 
        method if they wish to perform pre-conversion checks and manipulate
        the string accordingly.

        :param s: The raw string to convert.
        :type s: str
        :param delimiters: A set of delimiters used to identify boundaries.
            Defaults to DELIMITERS
        :type delimiters: str
        """
        self._delimiters = delimiters

        s = s.strip(delimiters)

        if strip_punctuation:
            punctuation = stripable_punctuation(delimiters)
            s = re.sub("[{}]+".format(re.escape(punctuation)), "", s)

        # Change recurring delimiters into single delimiters.
        s = re.sub("[{}]+".format(re.escape(delimiters)), delimiters[0], s)

        self._raw_input = s
        self._input_buffer = StringBuffer(self.prepare_string(s))
        self._output_buffer = StringBuffer()
        self._boundary_handlers = []

        self.define_boundaries()

    def add_boundary_handler(self, handler):
        """Add a boundary handler.

        :type handler: BoundaryHandler
        """
        self._boundary_handlers.append(handler)

    def define_boundaries(self):
        """Define boundary handlers.

        define_boundaries() is called when a CaseConverter is initialized.
        Typically, a child instance of CaseConverter will add boundary handlers.
        A CaseConverter without boundary handlers makes little sense, therefore
        a lack of boundary handlers generates a warning.
        """
        logger.warn("No boundaries defined")
        return

    def delimiters(self):
        """Retrieve the delimiters.

        :rtype: str
        """
        return self._delimiters

    def raw(self):
        """Retrieve the raw string to be converted.

        :rtype: str
        """
        return self._raw_input

    def init(self, input_buffer, output_buffer):
        """Initialize the output buffer.

        See convert() for call order.
        """
        return

    def mutate(self, c):
        """Mutate a character that's being added.

        See convert() for call order.
        """
        return c

    def prepare_string(self, s) -> str:
        """Prepare the raw intput string for conversion.

        Executed during CaseConverter initialization providing an opportunity
        for child classes to manipulate the string.

        :param s: The raw string supplied to the CaseConverter constructor.
        :type s: str
        :return: A raw string to be used in conversion.
        :rtype: str
        """
        return s

    def _is_boundary(self, pc, c):
        """Determine if we've hit a boundary or not.

        :rtype: BoundaryHandler
        """
        for bh in self._boundary_handlers:
            if bh.is_boundary(pc, c):
                return bh

        return None

    def convert(self) -> str:
        """Convert the raw string.

        
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
            bh = self._is_boundary(pc, cc)
            if bh:
                bh.handle(pc, cc, self._input_buffer, self._output_buffer)
            else:
                self._output_buffer.write(self.mutate(cc))

            pc = cc
            cc = self._input_buffer.read(1)

        return self._output_buffer.getvalue()


class OnDelimeterUppercaseNext(BoundaryHandler):
    def __init__(self, delimiters, join_char=""):
        self._delimiters = delimiters
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return c in self._delimiters

    def handle(self, pc, cc, input_buffer, output_buffer):
        output_buffer.write(self._join_char)
        output_buffer.write(input_buffer.read(1).upper())


class OnDelimeterLowercaseNext(BoundaryHandler):
    def __init__(self, delimiters, join_char=""):
        self._delimiters = delimiters
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return c in self._delimiters

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
        self.add_boundary_handler(OnDelimeterUppercaseNext(self.delimiters()))
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
            OnDelimeterLowercaseNext(self.delimiters(), self.JOIN_CHAR)
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
            OnDelimeterUppercaseNext(self.delimiters(), self.JOIN_CHAR)
        )
        self.add_boundary_handler(OnUpperPrecededByLowerAppendUpper(self.JOIN_CHAR))

    def convert(self):
        if self.raw().isupper():
            return re.sub(
                "[{}]+".format(re.escape(self.delimiters())),
                self.JOIN_CHAR,
                self.raw(),
            )

        return super(Cobol, self).convert()

    def mutate(self, c):
        return c.upper()


class Macro(Cobol):

    JOIN_CHAR = "_"


def camel_case(s, delims=DELIMITERS, strip_punctuation=True):
    """Convert a string to camel case.

    Example
    
      Hello World => helloWorld

    """
    return Camel(s, delimiters=delims, strip_punctuation=strip_punctuation).convert()


def cobol_case(s, delims=DELIMITERS, strip_punctuation=True):
    """Convert a string to cobol case

    Example

      Hello World => HELLO-WORLD

    """
    return Cobol(s, delimiters=delims, strip_punctuation=strip_punctuation).convert()


def macro_case(s, delims=DELIMITERS, strip_punctuation=True):
    """Convert a string to macro case

    Example

        Hello World => HELLO_WORLD

    """
    return Macro(s, delimiters=delims, strip_punctuation=strip_punctuation).convert()


def snake_case(s, delims=DELIMITERS, strip_punctuation=True):
    """Convert a string to snake case.

    Example

        Hello World => hello_world

    """
    return Snake(s, delimiters=delims, strip_punctuation=strip_punctuation).convert()


def pascal_case(s, delims=DELIMITERS, strip_punctuation=True):
    """Convert a string to pascal case

    Example

        Hello World => HelloWorld
        hello world => HelloWorld

    """
    return Pascal(s, delimiters=delims, strip_punctuation=strip_punctuation).convert()


def flat_case(s, delims=DELIMITERS, strip_punctuation=True):
    """Convert a string to flat case

    Example

        Hello World => helloworld

    """
    return Flat(s, delimiters=delims, strip_punctuation=strip_punctuation).convert()


def kebab_case(s, delims=DELIMITERS, strip_punctuation=True):
    """Convert a string to kebab case

    Example

        Hello World => hello-world

    """
    return Kebab(s, delimiters=delims, strip_punctuation=strip_punctuation).convert()
