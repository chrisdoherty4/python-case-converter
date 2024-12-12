import pytest
from . import titlecase


@pytest.mark.parametrize(
    "input, output",
    [
        # With punctuation
        ("Hello, world!", "Hello World"),
        # Camel cased
        ("helloWorld", "Hello World"),
        # Joined by delimiter
        ("Hello-World", "Hello World"),
        # All caps
        ("HELLO-WORLD", "Hello World"),
        # Without punctuation
        ("Hello world", "Hello World"),
        # Repeating single delimiter
        ("Hello   World", "Hello World"),
        # Repeating delimiters of different types
        ("Hello -__  World", "Hello World"),
        # Wrapped in delimiter
        (" hello world ", "Hello World"),
        # Long sentence with punctuation
        (
            r"the quick !b@rown fo%x jumped over the lazy Dog",
            "The Quick Brown Fox Jumped Over The Lazy Dog"
        ),
        # Multiple words
        ("this is a long title", "This Is A Long Title"),
    ],
)
def test_title_with_default_args(input, output):
    assert titlecase(input) == output
