import pytest
from . import *


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
    assert flatcase(input) == output
