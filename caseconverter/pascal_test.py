import pytest
from . import *


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
        ("helloWORLD", "HelloWORLD"),
    ],
)
def test_pascal_with_default_args(input, output):
    assert pascalcase(input) == output
