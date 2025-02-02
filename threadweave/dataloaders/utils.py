import urllib.parse

import tiktoken


def num_tokens_from_string(
    string: str, encoding_name: str = "gpt-3.5-turbo"
) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def is_valid_url(input_string: str) -> bool:
    """Check if an input string is a valid URL or not

    Args:
        input_string (str): Input string to check

    Returns:
        bool: True if the input string is a valid URL
    """
    try:
        result = urllib.parse.urlparse(input_string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
