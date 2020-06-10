import re

class CaseConverter(object):
  def __init__(self, s):
    self._string = s

  @staticmethod
  def _tokenize(s):
    '''Tokenize strings according to the different string types.

    The string types include flat, kebab, pascal, snake, macro and cobol
    case. All except flat strings can be split.

    :param s: The string to split
    :return: A list of split strings. If the string was not splittable, a
      list containing the original string.
    :rtype: list
    '''
    if not s:
      return None

    # Attempt to split snake case and kebab case.
    groups = re.split('-|_', s)

    if len(groups) > 1:
      return groups

    # Ensure we don't have a fully capitalized string because that results
    # in the following regex splitting each individual character.
    #
    # 'HELLOWORLD' => ['H', 'E', 'L', 'L', ...]
    if re.match('^[A-Z]+$', s):
      return [s]

    firstCharStore = s[0]
    s = firstCharStore.upper() + s[1:]

    groups = re.findall('[A-Z][^A-Z]*', s)

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
    return ''.join(self._lower(self._tokenize(self._string)))

  def kebab(self):
    return '-'.join(self._lower(self._tokenize(self._string)))

  def pascal(self):
    return ''.join(self._capitalize(self._tokenize(self._string)))

  def snake(self):
    return '_'.join(self._lower(self._tokenize(self._string)))

  def macro(self):
    return '_'.join(self._upper(self._tokenize(self._string)))

  def cobol(self):
    return '-'.join(self._upper(self._tokenize(self._string)))

  def camel(self):
    tokens = self._tokenize(self._string)

    if len(tokens) == 1:
      return tokens[0].lower()

    formattedTokens = [tokens[0].lower()]
    formattedTokens.extend(self._capitalize(tokens[1:]))

    return ''.join(formattedTokens)


def FlatCase(s):
  return CaseConverter(s).flat()


def KebabCase(s):
  return CaseConverter(s).kebab()


def PascalCase(s):
  return CaseConverter(s).pascal()


def SnakeCase(s):
  return CaseConverter(s).snake()


def MacroCase(s):
  return CaseConverter(s).macro()


def CobolCase(s):
  return CaseConverter(s).cobol()


def CamelCase(s):
  return CaseConverter(s).camel()


