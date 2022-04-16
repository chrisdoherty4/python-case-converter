import pytest
from . import *


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
        ("HelloXWorld", "HELLO_X_WORLD"),
    ],
)
def test_macro_with_default_args(input, output):
    assert macrocase(input) == output


@pytest.mark.parametrize(
    "input, output",
    [("IP Address", "IP_ADDRESS"), ("Hello IP Address", "HELLO_IP_ADDRESS")],
)
def test_macro_with_delims_only(input, output):
    assert macrocase(input, delims_only=True) == output
