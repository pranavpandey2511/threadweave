from abc import ABC, abstractmethod
from typing import List, Type, Callable, Optional
from pydantic import BaseModel, Field, ValidationError, validator
from enum import Enum

from threadweave.chunker.utils import num_tokens_from_string
from threadweave.constants import MAX_CHUNK_SIZE_TOKENS
from threadweave.document.chunk.schema import Chunk
import re


class Chunker(ABC):
    @abstractmethod
    def create_chunks(self, *args, **kwargs ) -> List[Chunk]:
        ...

    # Write a function which takes a string text and divides it into paragraphs, the paragrpahs can be random in nature
    def _split_paragraphs(self, text: str) -> List[str]:
        """Divide a string text into paragraphs.

        Args:
            text (str): Text to be divided

        Returns:
            List[str]: List of paragraphs
        """
        paragraphs = text.split("\n")
        return paragraphs

    # def _split_sentences(self, text: str):
    #     """Split text into sentances"""
    #     return sent_tokenize(text)

    def _split_and_keep_separator(self, text: str, separator: str = "."):
        """Split text by a separator and keep the separator in the splitted strings.

        Args:
            text (str): Text to be divided
            separator (str): Separator to split the text

        Returns:
            List[str]: List of splitted strings with separator attached to the previous string
        """
        splitted_strings = re.split(f"({separator})", text)
        return [
            "".join(x)
            for x in zip(splitted_strings[0::2], splitted_strings[1::2])
        ]

    def _postprocess_chunks(self, chunks: List[str]) -> List[str]:
        """Post process and validate chunks."""
        updated_chunks = []
        for entry in chunks:
            if entry.replace(" ", "") == "":
                continue
            updated_chunks.append(entry)
        return updated_chunks

    def _split_by_sep(text: str, separator: str = "."):
        """Split text by a separator."""
        return text.split(separator)


class Span(BaseModel):
    start: int
    end: int

    def extract(self, s: str) -> str:
        return "\n".join(s.splitlines()[self.start : self.end])

    def __add__(self, other):
        if isinstance(other, int):
            return Span(start=self.start + other, end=self.end + other)
        elif isinstance(other, Span):
            return Span(start=self.start, end=other.end)
        else:
            raise NotImplementedError()

    def __len__(self):
        return self.end - self.start
