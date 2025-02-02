from typing import Callable, List
import urllib.parse

import tiktoken


def num_tokens_from_string(
    string: str, model: str = "gpt-3.5-turbo"
) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# def is_valid_url(input_string: str) -> bool:
#     """Check if an input string is a valid URL or not

#     Args:
#         input_string (str): Input string to check

#     Returns:
#         bool: True if the input string is a valid URL
#     """
#     try:
#         result = urllib.parse.urlparse(input_string)
#         return all([result.scheme, result.netloc])
#     except ValueError:
#         return False


# def truncate_text(text: str, text_splitter: TextSplitter) -> str:
#     """Truncate text to fit within the chunk size."""
#     chunks = text_splitter.split_text(text)
#     return chunks[0]


# def split_text_keep_separator(text: str, separator: str) -> List[str]:
#     """Split text with separator and keep the separator at the end of each split."""
#     parts = text.split(separator)
#     result = [separator + s if i > 0 else s for i, s in enumerate(parts)]
#     result = [s for s in result if s]
#     return result


# def split_by_sep(sep: str, keep_sep: bool = True) -> Callable[[str], List[str]]:
#     """Split text by separator."""
#     if keep_sep:
#         return lambda text: split_text_keep_separator(text, sep)
#     else:
#         return lambda text: text.split(sep)


# def split_by_char() -> Callable[[str], List[str]]:
#     """Split text by character."""
#     return lambda text: list(text)


# def split_by_sentence_tokenizer() -> Callable[[str], List[str]]:
#     import nltk
#     import os

#     # from llama_index.utils import get_cache_dir

#     cache_dir = get_cache_dir()
#     nltk_data_dir = os.environ.get("NLTK_DATA", cache_dir)

#     # update nltk path for nltk so that it finds the data
#     if nltk_data_dir not in nltk.data.path:
#         nltk.data.path.append(nltk_data_dir)

#     try:
#         nltk.data.find("tokenizers/punkt")
#     except LookupError:
#         nltk.download("punkt", download_dir=nltk_data_dir)

#     return nltk.sent_tokenize


# def split_by_regex(regex: str) -> Callable[[str], List[str]]:
#     """Split text by regex."""
#     import re

#     return lambda text: re.findall(regex, text)


# def split_by_phrase_regex() -> Callable[[str], List[str]]:
#     """Split text by phrase regex.

    # This regular expression will split the sentences into phrases,
    # where each phrase is a sequence of one or more non-comma,
    # non-period, and non-semicolon characters, followed by an optional comma,
    # period, or semicolon. The regular expression will also capture the
    # delimiters themselves as separate items in the list of phrases.
    # """
    # regex = "[^,.;。]+[,.;。]?"
    # return split_by_regex(regex)




from tree_sitter import Node

def chunk_node(node: Node, text: str, MAX_CHARS: int = 1500) -> list[str]:
	new_chunks = []
	current_chunk = ""
	for child in node.children:
		if child.end_byte - child.start_byte > MAX_CHARS:
			new_chunks.append(current_chunk)
			current_chunk = ""
			new_chunks.extend(chunk_node(child, text, MAX_CHARS))
		elif child.end_byte > MAX_CHARS:
			new_chunks.append(current_chunk)
			current_chunk = text[node.start_byte:node.end_byte]
		else:
			current_chunk += text[node.start_byte:node.end_byte]
	return new_chunks


def read_file_content(filename):
    """
    Reads the content of a file given its filename.

    Args:
    - filename (str): The name of the file (with its extension).

    Returns:
    - str: The content of the file.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

