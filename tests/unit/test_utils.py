from utils.validation import get_valid_number_or_none, get_valid_url_or_none


def test_get_valid_integer():
    assert get_valid_number_or_none("1", int) == 1


def test_get_valid_float():
    assert get_valid_number_or_none("0", float) == 0.0
    assert get_valid_number_or_none("1", float) == 1.0
    assert get_valid_number_or_none("1.5", float) == 1.5


def test_get_invalid_number():
    assert get_valid_number_or_none("1.5", int) is None
    assert get_valid_number_or_none("", int) is None
    assert get_valid_number_or_none("abc", int) is None


def test_valid_url():
    assert get_valid_url_or_none("http://example.com") == "http://example.com"
    assert get_valid_url_or_none("http://www.example.com") == "http://www.example.com"
    assert get_valid_url_or_none("https://example.com") == "https://example.com"
    assert get_valid_url_or_none("https://www.example.com") == "https://www.example.com"
    assert get_valid_url_or_none("https://www.example.co.uk") == "https://www.example.co.uk"
    assert get_valid_url_or_none("https://www.example.com/path") == "https://www.example.com/path"


def test_get_invalid_url():
    assert get_valid_url_or_none("") is None
    assert get_valid_url_or_none("abc") is None
    assert get_valid_url_or_none(".com") is None
    assert get_valid_url_or_none("example.com") is None
    assert get_valid_url_or_none("abc://abc.com") is None
    assert get_valid_url_or_none("www.example.com") is None
    assert get_valid_url_or_none("https:/example.com") is None
