import pytest
from . import camel_case, cobol_case


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("Hello World", "helloWorld"),
        ("What's new with, you", "whatsNewWithYou"),
        ("Hello   World", "helloWorld"),
        ("Hello -__  World", "helloWorld"),
        (" hello world ", "helloWorld"),
        (
            r"the quick !b@rown f%ox jumped over the 'fence",
            "theQuickBrownFoxJumpedOverTheFence",
        ),
    ],
)
def test_camel_case_with_default_args(input, expected_output):
    assert camel_case(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output, delims",
    [
        ("Hello|World", "helloWorld", "|"),
        ("|hello|World|", "helloWorld", "|"),
        (" hello | world | ", "helloWorld", "| "),
    ],
)
def test_camel_case_custom_delims(input, expected_output, delims):
    assert camel_case(input, delims=delims) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("Hello|World", "hello|world"),
        ("|hello|World|", "|hello|world|"),
        (" hello | world | ", "hello|World|"),
    ],
)
def test_camel_case_no_strip_punctuation(input, expected_output):
    assert camel_case(input, strip_punctuation=False) == expected_output

@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("Hello World", "HELLO-WORLD"),
        ("What's new with, you", "WHATS-NEW-WITH-YOU"),
        ("Hello   World", "HELLO-WORLD"),
        ("Hello -__  World", "HELLO-WORLD"),
        (" hello world ", "HELLO-WORLD"),
        (
            r"the quick !b@rown f%ox jumped over the 'fence",
            "THE-QUICK-BROWN-FOX-JUMPED-OVER-THE-FENCE",
        ),
        ("Hello-World", "HELLO-WORLD")
    ],
)
def test_cobol_case_with_default_args(input, expected_output):
    assert cobol_case(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output, delims",
    [
        ("Hello|World", "HELLO-WORLD", "|"),
        ("|hello|World|", "HELLO-WORLD", "|"),
        (" hello | world | ", "HELLO-WORLD", "| "),
    ],
)
def test_cobol_case_custom_delims(input, expected_output, delims):
    assert cobol_case(input, delims=delims) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("hell'oWorld", "HELL'O-WORLD"),
        ("helloWorld|", "HELLO-WORLD|"),
        (" hel'lo wo'rld  ", "HEL'LO-WO'RLD"),
    ],
)
def test_cobol_case_no_strip_punctuation(input, expected_output):
    assert cobol_case(input, strip_punctuation=False) == expected_output
