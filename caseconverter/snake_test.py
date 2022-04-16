import pytest
from . import *


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
    assert snakecase(input) == output
