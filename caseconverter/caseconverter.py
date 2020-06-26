import re
import string


class CaseConverter(object):
    def __init__(self, s):
        self._string = s

    @staticmethod
    def _tokenize(s):
        """Tokenize strings according to the different string types.

        The string types include flat, kebab, pascal, snake, macro and cobol
        case. All except flat strings can be split.

        :param s: The string to split
        :return: A list of split strings. If the string was not splittable, a
          list containing the original string.
        :rtype: list
        """
        if not s:
            return None

        # Attempt to split snake case and kebab case.
        groups = re.split("-|_", s)

        if len(groups) > 1:
            return groups

        # Ensure we don't have a fully capitalized string because that results
        # in the following regex splitting each individual character.
        #
        # 'HELLOWORLD' => ['H', 'E', 'L', 'L', ...]
        if re.match("^[A-Z]+$", s):
            return [s]

        firstCharStore = s[0]
        s = firstCharStore.upper() + s[1:]

        groups = re.findall("[A-Z][^A-Z]*", s)

        groups[0] = firstCharStore + groups[0][1:]

        return groups

    @staticmethod
    def _lower(l):
        return map(lambda s: s.lower(), l)

    @staticmethod
    def _upper(l):
        return map(lambda s: s.upper(), l)

    @staticmethod
    def _capitalize(l):
        return map(lambda s: s.capitalize(), l)

    def flat(self):
        return "".join(self._lower(self._tokenize(self._string)))

    def kebab(self):
        return "-".join(self._lower(self._tokenize(self._string)))

    def pascal(self):
        return "".join(self._capitalize(self._tokenize(self._string)))

    def snake(self):
        return "_".join(self._lower(self._tokenize(self._string)))

    def macro(self):
        return "_".join(self._upper(self._tokenize(self._string)))

    def cobol(self):
        return "-".join(self._upper(self._tokenize(self._string)))

    def camel(self):
        tokens = self._tokenize(self._string)

        if len(tokens) == 1:
            return tokens[0].lower()

        formattedTokens = [tokens[0].lower()]
        formattedTokens.extend(self._capitalize(tokens[1:]))

        return "".join(formattedTokens)


def flat_case(s):
    """Convert a string to flat case

    Example

        Hello World => helloworld

    """
    return CaseConverter(s).flat()


def kebab_case(s):
    """Convert a string to kebab case

    Example

        Hello World => hello-world

    """
    return CaseConverter(s).kebab()


def pascal_case(s):
    """Convert a string to pascal case

    Example

        Hello World => HelloWorld
        hello world => HelloWorld

    """
    return CaseConverter(s).pascal()


def snake_case(s):
    """Convert a string to snake case.

    Example

        Hello World => hello_world

    """
    return CaseConverter(s).snake()


def macro_case(s):
    """Convert a string to macro case

    Example

        Hello World => HELLO_WORLD

    """
    return CaseConverter(s).macro()


def cobol_case(s, delims=" _-", strip_punctuation=True):
    """Convert a string to cobol case

    Example

      Hello World => HELLO-WORLD

    """
    s = s.strip(delims)

    if strip_punctuation:
        s = _strip_punctuation(s, _strippable_punctuation(delims))

    s = _reduce_delims(s, delims)

    def mutate(m):
        # Remove NoneType which reduces the matches down to 1, hence index 0.
        return "-" + list(filter(lambda m: m != None, m.groups()))[0]

    s = _mutate_tokens(
        s,
        "(?<=[{}]|[A-Z])([a-zA-Z]+)".format(re.escape(delims)),
        mutate,
    )
    
    delims = delims.replace("-", "")

    return _strip_delims(s, delims).upper()


def camel_case(s, delims=" _-", strip_punctuation=True):
    """Convert a string to camel case.

    Example
    
      Hello World => helloWorld

    """
    # return CaseConverter(s).camel()

    # hello world
    # Hello World
    # hello-world
    # what's new
    # hello_world
    # helloworld

    # 1. Is there a subset of token separation characters?
    # 2. How do we handle repeat separators?
    # 3. Should we strip punctuation?
    # 4. How do we handle integers?

    # Inputs:
    #   1. characters to split tokens on
    #   2. string
    #   3. should we strip punctuation?

    # strip all punctuation that is not a delimeter
    # reduce delimeters down to single instance
    # lowercase all characters
    # uppercase any char preceeded by a delimeter
    # remove all delimeters

    s = s.strip(delims).lower()

    if strip_punctuation:
        s = _strip_punctuation(s, _strippable_punctuation(delims))

    s = _reduce_delims(s, delims)

    s = _mutate_tokens(
        s,
        "(?<=[{}])([a-z]+)".format(re.escape(delims)),
        lambda m: m.group(1).capitalize(),
    )

    return _strip_delims(s, delims)


def _strip_punctuation(s, chars):
    return re.sub("[{}]+".format(re.escape(chars)), "", s)


def _strippable_punctuation(delims):
    return "".join([c for c in string.punctuation if c not in delims])


def _reduce_delims(s, delims):
    return re.sub("[{}]+".format(re.escape(delims)), delims[0], s)


def _mutate_tokens(s, token_regex, func):
    return re.sub(token_regex, func, s)


def _strip_delims(s, delims):
    return re.sub("[{}]+".format(re.escape(delims)), "", s)
