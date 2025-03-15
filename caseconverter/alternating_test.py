import pytest
from . import *


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation.
        ("Hello, world!", "hElLo WoRlD"),
        # Camel cased
        ("helloWorld", "hElLoWoRlD"),
        # Joined by delimeter.
        ("Hello-World", "hElLo WoRlD"),
        # Cobol cased
        ("HELLO-WORLD", "hElLo WoRlD"),
        # Without punctuation.
        ("Hello world", "hElLo WoRlD"),
        # Repeating single delimeter
        ("Hello   World", "hElLo WoRlD"),
        # Repeating delimeters of different types
        ("Hello -__  World", "hElLo WoRlD"),
        # Wrapped in delimeter
        (" hello world ", "hElLo WoRlD"),
        # End in capital letter
        ("hellO", "hElLo"),
        # Long sentence with punctuation
        (
        r"the quick !b@rown fo%x jumped over the laZy Do'G",
        "tHe QuIcK bRoWn FoX jUmPeD oVeR tHe LaZy DoG",
        ),
        # Alternating character cases
        ("heLlo WoRld", "hElLo WoRlD"),
    ],
)
def test_alternating_with_default_args(input, output):
    assert alternatingcase(input) == output
