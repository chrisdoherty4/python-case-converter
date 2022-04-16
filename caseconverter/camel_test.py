import pytest
from . import *


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
    assert camelcase(input) == output
