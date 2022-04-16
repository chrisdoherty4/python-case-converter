import pytest
from . import *


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
    assert cobolcase(input) == output
