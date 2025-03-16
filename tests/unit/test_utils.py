from utils.validation import get_valid_number_or_none, get_valid_url_or_none


def test_get_valid_integer():
    """
    Test the function get_valid_number_or_none with a valid integer string.

    This test verifies that the `get_valid_number_or_none()` function correctly
    converts a valid integer string (e.g., "1") to an integer (1).
    """
    assert get_valid_number_or_none("1", int) == 1


def test_get_valid_float():
    """
    Test the function get_valid_number_or_none with valid float strings.

    This test ensures that the `get_valid_number_or_none()` function correctly
    converts valid float strings (e.g., "1", "1.5", "0") to the corresponding float values.
    """
    assert get_valid_number_or_none("0", float) == 0.0
    assert get_valid_number_or_none("1", float) == 1.0
    assert get_valid_number_or_none("1.5", float) == 1.5


def test_get_invalid_number():
    """
    Test the function get_valid_number_or_none with invalid number strings.

    This test verifies that the `get_valid_number_or_none()` function returns `None`
    when given invalid strings, such as non-numeric values, empty strings, or values
    that cannot be converted to integers.
    """
    assert get_valid_number_or_none("1.5", int) is None
    assert get_valid_number_or_none("", int) is None
    assert get_valid_number_or_none("abc", int) is None


def test_valid_url():
    """
    Test the function get_valid_url_or_none with valid URL strings.

    This test ensures that the `get_valid_url_or_none()` function correctly identifies
    and returns valid URLs with different schemes (e.g., "http://", "https://") and paths.
    """
    assert get_valid_url_or_none("http://example.com") == "http://example.com"
    assert get_valid_url_or_none("http://www.example.com") == "http://www.example.com"
    assert get_valid_url_or_none("https://example.com") == "https://example.com"
    assert get_valid_url_or_none("https://www.example.com") == "https://www.example.com"
    assert get_valid_url_or_none("https://www.example.co.uk") == "https://www.example.co.uk"
    assert get_valid_url_or_none("https://www.example.com/path") == "https://www.example.com/path"


def test_get_invalid_url():
    """
    Test the function get_valid_url_or_none with invalid URL strings.

    This test ensures that the `get_valid_url_or_none()` function returns `None`
    when given invalid or incorrectly formatted URLs, such as those without a valid scheme,
    missing domains, or malformed URLs.
    """
    assert get_valid_url_or_none("") is None
    assert get_valid_url_or_none("abc") is None
    assert get_valid_url_or_none(".com") is None
    assert get_valid_url_or_none("example.com") is None
    assert get_valid_url_or_none("abc://abc.com") is None
    assert get_valid_url_or_none("www.example.com") is None
    assert get_valid_url_or_none("https:/example.com") is None
