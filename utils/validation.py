from typing import Callable
from urllib.parse import urlparse


def get_valid_number_or_none(value: str, conversion_func: Callable) -> int | float | None:
    """
    Converts a value to a number using a specified conversion function.

    This function attempts to convert the given value into a number
    using the provided conversion function (e.g., `int`, `float`). If the
    conversion fails (raises a `ValueError`), it returns `None`.

    Args:
        value (str): The input value to convert.
        conversion_func (Callable): The function to use for conversion (e.g., `int`, `float`).

    Returns:
        Union[int, float, None]: The converted number if successful, otherwise `None`.

    Example:
        >>> get_valid_number_or_none("123", int)
        123
        >>> get_valid_number_or_none("abc", int)
        None
        >>> get_valid_number_or_none("3.14", float)
        3.14
    """
    try:
        return conversion_func(value)
    except ValueError:
        return None


def get_valid_url_or_none(url: str) -> str | None:
    """Validates a given URL and returns it if valid, otherwise returns None.

    This function checks whether the provided URL has both a scheme
    (e.g., "http" or "https") and a network location (domain). If the URL
    is valid, it returns the original URL; otherwise, it returns None.

    Args:
        url (str): The URL to validate.

    Returns:
        str | None: The original URL if valid, otherwise None.

    Example:
        >>> get_valid_url_or_none("https://example.com")
        'https://example.com'
        >>> get_valid_url_or_none("invalid-url")
        None
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return url
    return None
