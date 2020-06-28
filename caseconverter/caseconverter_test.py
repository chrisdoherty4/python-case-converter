import pytest
from .caseconverter import *


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation.
        ("Hello, world!", "helloWorld"),
        # Camel cased
        ("helloWorld", "helloWorld"),
        # Joined by delimeter.
        ("Hello-World", "helloWorld"),
        # Cobol cased
        ("HELLO-WORLD", "helloWorld"),
        # Without punctuation.
        ("Hello world", "helloWorld"),
        # Repeating single delimeter
        ("Hello   World", "helloWorld"),
        # Repeating delimeters of different types
        ("Hello -__  World", "helloWorld"),
        # Wrapped in delimeter
        (" hello world ", "helloWorld"),
        # End in capital letter
        ("hellO", "hellO"),
        # Long sentence with punctuation
        (
            r"the quick !b@rown fo%x jumped over the laZy Do'G",
            "theQuickBrownFoxJumpedOverTheLaZyDoG",
        ),
        # Alternating character cases
        ("heLlo WoRld", "heLloWoRld"),
    ],
)
def test_camel_with_default_args(input, output):
    assert camel_case(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation.
        ("Hello, world!", "HELLO-WORLD"),
        # Camel cased
        ("helloWorld", "HELLO-WORLD"),
        # Joined by delimeter.
        ("Hello-World", "HELLO-WORLD"),
        # Cobol cased
        ("HELLO-WORLD", "HELLO-WORLD"),
        # Without punctuation.
        ("Hello world", "HELLO-WORLD"),
        # Repeating single delimeter
        ("Hello   World", "HELLO-WORLD"),
        # Repeating delimeters of different types
        ("Hello -__  World", "HELLO-WORLD"),
        # Wrapped in delimeter
        (" hello world ", "HELLO-WORLD"),
        # End in capital letter
        ("hellO", "HELL-O"),
        # Long sentence with punctuation
        (
            r"the quick !b@rown fo%x jumped over the laZy Do'G",
            "THE-QUICK-BROWN-FOX-JUMPED-OVER-THE-LA-ZY-DO-G",
        ),
        # Alternating character cases
        ("heLlo WoRld", "HE-LLO-WO-RLD"),
    ],
)
def test_cobol_with_default_args(input, output):
    assert cobol_case(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation.
        ("Hello, world!", "HELLO_WORLD"),
        # Camel cased
        ("helloWorld", "HELLO_WORLD"),
        # Joined by delimeter.
        ("Hello-World", "HELLO_WORLD"),
        # Cobol cased
        ("HELLO-WORLD", "HELLO_WORLD"),
        # Without punctuation.
        ("Hello world", "HELLO_WORLD"),
        # Repeating single delimeter
        ("Hello   World", "HELLO_WORLD"),
        # Repeating delimeters of different types
        ("Hello -__  World", "HELLO_WORLD"),
        # Wrapped in delimeter
        (" hello world ", "HELLO_WORLD"),
        # End in capital letter
        ("hellO", "HELL_O"),
        # Long sentence with punctuation
        (
            r"the quick !b@rown fo%x jumped over the laZy Do'G",
            "THE_QUICK_BROWN_FOX_JUMPED_OVER_THE_LA_ZY_DO_G",
        ),
        # Alternating character cases
        ("heLlo WoRld", "HE_LLO_WO_RLD"),
    ],
)
def test_macro_with_default_args(input, output):
    assert macro_case(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation.
        ("Hello, world!", "hello_world"),
        # Camel cased
        ("helloWorld", "hello_world"),
        # Joined by delimeter.
        ("Hello-World", "hello_world"),
        # Cobol cased
        ("HELLO-WORLD", "hello_world"),
        # Without punctuation.
        ("Hello world", "hello_world"),
        # Repeating single delimeter
        ("Hello   World", "hello_world"),
        # Repeating delimeters of different types
        ("Hello -__  World", "hello_world"),
        # Wrapped in delimeter
        (" hello world ", "hello_world"),
        # End in capital letter
        ("hellO", "hell_o"),
        # Long sentence with punctuation
        (
            r"the quick !b@rown fo%x jumped over the laZy Do'G",
            "the_quick_brown_fox_jumped_over_the_la_zy_do_g",
        ),
        # Alternating character cases
        ("heLlo WoRld", "he_llo_wo_rld"),
    ],
)
def test_snake_with_default_args(input, output):
    assert snake_case(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation.
        ("Hello, world!", "HelloWorld"),
        # Camel cased
        ("helloWorld", "HelloWorld"),
        # Joined by delimeter.
        ("Hello-World", "HelloWorld"),
        # Cobol cased
        ("HELLO-WORLD", "HelloWorld"),
        # Without punctuation.
        ("Hello world", "HelloWorld"),
        # Repeating single delimeter
        ("Hello   World", "HelloWorld"),
        # Repeating delimeters of different types
        ("Hello -__  World", "HelloWorld"),
        # Wrapped in delimeter
        (" hello world ", "HelloWorld"),
        # End in capital letter
        ("hellO", "HellO"),
        # Long sentence with punctuation
        (
            r"the quick !b@rown fo%x jumped over the laZy Do'G",
            "TheQuickBrownFoxJumpedOverTheLaZyDoG",
        ),
        # Alternating character cases
        ("heLlo WoRld", "HeLloWoRld"),
    ],
)
def test_pascal_with_default_args(input, output):
    assert pascal_case(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation.
        ("Hello, world!", "helloworld"),
        # Camel cased
        ("helloWorld", "helloworld"),
        # Joined by delimeter.
        ("Hello-World", "helloworld"),
        # Cobol cased
        ("HELLO-WORLD", "helloworld"),
        # Without punctuation.
        ("Hello world", "helloworld"),
        # Repeating single delimeter
        ("Hello   World", "helloworld"),
        # Repeating delimeters of different types
        ("Hello -__  World", "helloworld"),
        # Wrapped in delimeter
        (" hello world ", "helloworld"),
        # End in capital letter
        ("hellO", "hello"),
        # Long sentence with punctuation
        (
            r"the quick !b@rown fo%x jumped over the laZy Do'G",
            "thequickbrownfoxjumpedoverthelazydog",
        ),
        # Alternating character cases
        ("heLlo WoRld", "helloworld"),
    ],
)
def test_flat_with_default_args(input, output):
    assert flat_case(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation.
        ("Hello, world!", "hello-world"),
        # Camel cased
        ("helloWorld", "hello-world"),
        # Joined by delimeter.
        ("Hello-World", "hello-world"),
        # Cobol cased
        ("HELLO-WORLD", "hello-world"),
        # Without punctuation.
        ("Hello world", "hello-world"),
        # Repeating single delimeter
        ("Hello   World", "hello-world"),
        # Repeating delimeters of different types
        ("Hello -__  World", "hello-world"),
        # Wrapped in delimeter
        (" hello world ", "hello-world"),
        # End in capital letter
        ("hellO", "hell-o"),
        # Long sentence with punctuation
        (
            r"the quick !b@rown fo%x jumped over the laZy Do'G",
            "the-quick-brown-fox-jumped-over-the-la-zy-do-g",
        ),
        # Alternating character cases
        ("heLlo WoRld", "he-llo-wo-rld"),
    ],
)
def test_kebab_with_default_args(input, output):
    assert kebab_case(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation.
        ("Hell9o, world!", "hell9oWorld"),
        ("0Hello, world!", "0helloWorld"),
        ("Hello, world!0", "helloWorld0"),
    ],
)
def test_with_numbers(input, output):
    assert camel_case(input) == output
