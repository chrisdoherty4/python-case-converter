# Case Converter

A python package for transforming string cases such as `Hell, world!` into
camel case, `helloWorld`.

## General usage

Import a case conversion helper function, or the conversion object itself.

```python
from caseconverter import camel_case, Camel

camel_case("Hello, world!") # helloWorld
Camel("Hello, world!").convert() # helloWorld
```

#### Customizing delimiters

There are a set of default delimiters used to denote a character boundary.
These delimiters are defined in caseconverter.py as `DELIMITER`.

```python
from caseconverter import camel_case

# Use a pipe `|` as the only delimiter.
camel_case("Hello,|world!", delims="|") # helloWorld
```

#### Stripping punctuation

Generally, punctuation is stripped when doing a case conversion. However, should you
wish to keep the punctuation you can do so by passing `strip_punctuation=False`.

```python
from caseconverter import camel_case

camel_case("Hello, world!", strip_punctuation=False) # hello,World!
```

## Available conversions

### Camel case

```text
Hello, world! => helloWorld
```

### Pascal case

```text
Hello, world! => HelloWorld
```

### Snake case

```text
Hello, world! => hello_world
```

### Flat case

```text
Hello, world! => helloworld
```

### Kebab case

```text
Hello, world! => hello-world
```

### Cobol case

```text
Hello, world! => HELLO-WORLD
```

### Macro case

```text
Hello, world! => HELLO_WORLD
```

## Contributing

1. Write clean code.
2. Write new tests for new use-cases.
3. Test your code before raising a PR.
4. Use [black](https://pypi.org/project/black/) to format your code.
