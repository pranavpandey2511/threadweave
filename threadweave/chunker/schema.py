from abc import ABC, abstractmethod
from typing import List, Type, Callable
from pydantic import BaseModel, Field, ValidationError, validator
from enum import Enum

from threadweave.dataloaders.utils import num_tokens_from_string
from threadweave.constants import MAX_CHUNK_SIZE_TOKENS

ChunkType = Enum("ChunkType", ["TEXT", "CODE", "TOKENS"])


class Chunk(BaseModel):
    text: str
    chunk_type: ChunkType = Field(
        ..., description="Type of chunking used to generate the chunk"
    )

    @validator("text")
    def validate_text_length(cls, text):
        NUM_TOKENS = num_tokens_from_string(text)
        if NUM_TOKENS > MAX_CHUNK_SIZE_TOKENS:
            raise ValidationError(
                f"Chunk size cannot be greater than MAX_CHUNK_SIZE_TOKENS: {MAX_CHUNK_SIZE_TOKENS}, NUM_TOKENS: {NUM_TOKENS}",
                loc="text",
            )
        return text


class Chunker(ABC):
    @abstractmethod
    def create_chunks(self, input) -> List[Chunk]:
        ...


class TextChunker(ABC):
    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        ...


class CodeChunker(ABC):
    @abstractmethod
    def chunk_code(self, code: str) -> List[str]:
        ...


class TokenChunker(ABC):
    @abstractmethod
    def chunk_tokens(self, code: str) -> List[str]:
        ...
