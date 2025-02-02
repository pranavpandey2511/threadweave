import re
import os
import base64
import mimetypes
from typing import List, Dict, Optional, Union
import tiktoken


def is_url(string: str) -> bool:
    url_pattern = r"/(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?"
    return bool(re.match(url_pattern, string))


def is_base64(string: str) -> bool:
    base64_pattern = r"^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{4}|[A-Za-z0-9+\/]{3}=|[A-Za-z0-9+\/]{2}={2})$"
    return bool(re.match(base64_pattern, string))


def image_to_base64(file_path: str) -> str:
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
            base64_data = base64.b64encode(file_data).decode("utf-8")
            mime_type = get_mimetype(file_path)
            base64_string = f"data:{mime_type};base64,{base64_data}"
            return base64_string
    except Exception as error:
        raise Exception(f"Image to base64 error: {str(error)}")


def omit(d: Dict, key: str) -> Dict:
    if d is None:
        return {}
    return {k: v for k, v in d.items() if k != key}


def filter_args(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def get_mimetype(file_path: str):
    mime_type, encoding = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"


def preprocess_text(text: str) -> str:
    """Cleans an input string by removing unnecessary characters like newlines, tabs, etc. and making it suitable
    for further processing like tokenization, etc.

    Args:
        text (str): Input text string to be cleaned.

    Returns:
        str: Cleaned output string.
    """

    # Strip the string to remove trailing whitespaces
    text = text.strip()

    # Replace multiple newlines with a spaces:
    text = re.sub(r"\n+", " ", text)

    # Replace multiple spaces with a single space:
    text = re.sub(r"\s+", " ", text)

    # Remove all backslashes from the text:
    text = text.replace("\\", "")

    # Eliminating consecutive non-alphanumeric characters:
    # This regex identifies consecutive non-alphanumeric characters (i.e., not
    # a word character [a-zA-Z0-9_] and not a whitespace) in the string
    # and replaces each group of such characters with a single occurrence of
    # that character.
    # For example, "!!! hello !!!" would become "! hello !".
    output_text = re.sub(r"([^\w\s])\1*", r"\1", text)

    return output_text


def num_tokens_from_string(
    string: str, encoding_name: str = "gpt-3.5-turbo"
) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
