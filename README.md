# Case Converter

[![pipline](https://img.shields.io/gitlab/pipeline/chrisdoherty4/python-case-converter)](https://gitlab.com/chrisdoherty4/python-case-converter/-/pipelines) [![wheel](https://img.shields.io/pypi/wheel/case-converter)](https://pypi.org/project/case-converter/) ![coverage](https://gitlab.com/chrisdoherty4/python-case-converter/badges/master/coverage.svg) ![license](https://img.shields.io/github/license/chrisdoherty4/python-case-converter)

A robust python package for transforming string cases such as `Hello, world!` into
 `helloWorld` (camelcase).

## General usage

Import a case conversion helper function, or the conversion object itself.

```python
from caseconverter import camelcase, Camel

camelcase("Hello, world!") # output: helloWorld
Camel("Hello, world!").convert() # output: helloWorld
```

By default, case conversion takes into consideration 2 boundary conditions for
token separation.

1. Delimiters.
2. Lowercase char followed by an uppercase char.

The action taken when a boundary is identified depends on the case conversion.

If the input string is all uppercase it can only be processed based on delimiters.

#### Customizing delimiters

Default delimiters used to denote a token boundary.

```python
# Default delimiters
DELIMITERS = " -_"
```

You can pass `delims` to each case conversion function to specify a custom
set of delimiters.

```python
from caseconverter import camelcase

# Use a pipe `|` as the only delimiter.
camelcase("Hello,|world!", delims="|") # output: helloWorld
```

#### Stripping punctuation

Generally, punctuation is stripped when doing a case conversion. However, should you
wish to keep the punctuation you can do so by passing `strip_punctuation=False`.

```python
from caseconverter import camelcase

camelcase("Hello, world!", strip_punctuation=False) # output: hello,World!
```

## Available conversions

### `camelcase`

```python
from caseconverter import camelcase

camelcase("Hello, world!") 
```

```text
helloWorld
```

### `pascalcase`

```python
from caseconverter import pascalcase

pascalcase("Hello, world!")
```

```text
HelloWorld
```

### `snakecase`

```python
from caseconverter import snakecase

snakecase("Hello, world!")
```

```text
hello_world
```

### `flatcase`

```python
from caseconverter import flatcase

flatcase("Hello, world!")
```

```text
helloworld
```

### `kebabcase`

```python

from caseconverter import kebabcase

kebabcase("Hello, world!")
```

```text
hello-world
```

### `cobolcase`

```python
from caseconverter import cobolcase

cobolcase("Hello, world!")
```

```text
HELLO-WORLD
```

### `macrocase`

```python
from caseconverter import macrocase

macrocase("Hello, world!")
```

```text
HELLO_WORLD
```

## Contributing

1. Write clean code.
2. Write new tests for new use-cases.
3. Test your code before raising a PR.
4. Use [black](https://pypi.org/project/black/) to format your code.
