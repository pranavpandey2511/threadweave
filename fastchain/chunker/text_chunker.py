"""Text chunkers"""
import os
from typing import Callable, List, Optional, Union

from fastchain.document.chunk.base import Chunk
from fastchain.document.chunk.schema import TextChunk
from fastchain.chunker.base import Chunker, Span
from fastchain.constants import *
from fastchain.dataloaders.utils import num_tokens_from_string
import tiktoken
from pydantic import BaseModel, Field, PrivateAttr
import spacy
import spacy.cli
import math
import re
import logging
import logging.config
from dotenv import load_dotenv
from fastchain.utils import num_tokens_from_string
from docarray import DocList
from fastchain.chunker.utils import num_tokens_from_string
from uuid import UUID as UUID4

load_dotenv()

logging.config.fileConfig(
    fname=os.environ.get("LOGGER_CONF_FILE"), disable_existing_loggers=False
)

# Get the logger specified in the file
logger = logging.getLogger(__name__)


class TextChunker(BaseModel):
    """This class is used to chunk text using text length limits."""


    chunk_size: int = Field(default=DEFAULT_CHUNK_SIZE, alias="text_chunk_size")
    chunk_overlap: int = Field(
        default=DEFAULT_CHUNK_OVERLAP_SIZE, alias="text_chunk_overlap"
    )
    length_function: Callable = Field(default=len, alias="text_length_function")
    subdivide_strategy: str = Field(default=DEFAULT_SUBDIVIDE_STRATEGY)

    _document_id: Optional[UUID4] = PrivateAttr()
    _page_id: Optional[UUID4] = PrivateAttr()
    _chunk_count: int = PrivateAttr()
    _chunks: DocList[TextChunk] = PrivateAttr()

    def __init__(self, document_id=None, page_id=None):
        # Set the document and page ids
        self._document_id = document_id
        self._page_id = page_id
        self._chunks = DocList[TextChunk]()
        self._chunk_count = 0
        super().__init__()
    @classmethod
    def class_name(cls) -> str:
        """Return object class name."""
        return "TextChunker"

    def create_chunks(self, text: Union[List[str], str],
                      document_id: Optional[UUID4] = "None",
                      page_id: Optional[UUID4]= None) -> DocList[TextChunk]:

        if self.chunk_overlap > self.chunk_size:
            raise ValueError(
                f"Got a larger chunk overlap ({self.chunk_overlap}) than chunk size "
                f"({self.chunk_size}), should be smaller.")

        if not isinstance(text, List) and not isinstance(text, str):
            raise ValueError(f"Cannot create chunks from {type(text)} type of input | Expected List[str] or str")


        if isinstance(text, str):

            if self.length_function(text) <= self.chunk_size:
                self._chunks.append(TextChunk(content=text, document_id=self._document_id, page_id=self._page_id))
                return self._chunks
            else:
                return self._chunkify(text)

        if isinstance(text, List):
            for item in text:
                if not isinstance(item, str):
                    raise ValueError(f"List of text can only contain strings and not: {type(item)}")

                self.create_chunks(item)

    def _chunkify(self, text: str) ->DocList[TextChunk]:
        # Equally split the text
        if self.subdivide_strategy == "character":

            i = 0
            while i < self.length_function(text):
                # here 'i' cannot be less than 0 and we consider overlap size everytime
                i = max(0, i - self.chunk_overlap)
                chunk_text = text[i : min(i + self.chunk_size, self.length_function(text))]
                self._chunks.append(TextChunk(content=chunk_text, document_id=self._document_id, page_id=self._page_id))
                # Step i by chunk size
                i += self.chunk_size

            return self._chunks

        elif self.subdivide_strategy == "words":

            # try:
            #     # Specify the language model you want to download (e.g., "en_core_web_sm")
            #     model_name = "en_core_web_sm"
            #     # Download the spaCy language model
            #     spacy.cli.download(model_name)
            # except:
            #     raise ValueError("Could not download the spaCy language model, check your internet conenction")
            #
            # nlp = spacy.load(model_name)
            #
            # doc = nlp(text)
            # # Access tokens
            # words = [token.text for token in doc]
            words = text.split()
            num_words = len(words)


            end=1
            chunk_text = words[0]
            last_word_added = words[0]  # Initialize a variable to keep track of the last word added

            while end < num_words:
                # Keep track of last word added so that we can remove it later
                last_word_added= words[end]
                chunk_text += words[end] + " " #" ".join(words[start:end])

                if self.length_function(chunk_text) >= self.chunk_size:
                    chunk_text = chunk_text[:-len(last_word_added)].strip()
                    self._chunks.append(TextChunk(content=chunk_text, document_id=self._document_id, page_id=self._page_id))
                    chunk_text = chunk_text[-self.chunk_overlap:] + " "
                    continue
                end += 1

            return self._chunks

# class TokenChunker(Chunker, BaseModel):
#     """Create chunks based on MAX_TOKEN_SIZE."""
#
#     chunk_size: int = Field(
#         default=DEFAULT_TOKEN_CHUNK_SIZE, alias="token_chunk_size"
#     )
#     chunk_overlap: int = Field(
#         default=DEFAULT_TOKEN_CHUNK_OVERLAP_SIZE, alias="token_chunk_overlap"
#     )
#     length_function: Callable = Field(
#         default=num_tokens_from_string, alias="text_length_function"
#     )
#     document_id: Optional[UUID4]
#     page_id: Optional[UUID4]
#
#     # _chunk_count: int = Field(default=0)
#     _chunks: DocList = Field(default=DocList[TextChunk]())
#
#     def create_chunks(self, text: Union[List[str], str])-> DocList[TextChunk]:
#         """Initialize with parameters."""
#         if self.chunk_overlap > self.chunk_size:
#             raise ValueError(
#                 f"Got a larger chunk overlap ({self.chunk_overlap}) than chunk size "
#                 f"({self.chunk_size}), should be smaller."
#             )
#
#         return self._chunk_by_token_limit()
#
#     @classmethod
#     def class_name(cls) -> str:
#         """Get class name."""
#         return "TokenChunker"
#
#     def _chunk_by_token_limit(
#         self, text, token_limit, *, overlap=20, model="gpt-3.5-turbo"
#     ) -> List[str]:
#         # Count number of tokens
#         num_tokens = num_tokens_from_string(text, model)
#
#         # Check if the text fits within the token limit
#         if num_tokens <= token_limit:
#             return [text]
#
#         # Calculate the number of chunks needed
#         num_chunks = (num_tokens - overlap) // (token_limit - overlap) + 1
#
#         # Calculate the target tokens per chunk
#         tokens_per_chunk = math.ceil(num_tokens / num_chunks)
#
#         # Initialize variables
#         text_chunks = []
#         current_chunk = ""
#         current_chunk_tokens = 0
#
#         # Split the text into words
#         all_words = text.split()
#
#         # Iterate over the words
#         for word in all_words:
#             # Count the tokens in the current word
#             word_tokens = num_tokens_from_string(word, model)
#
#             # Check if adding the current word would exceed the token limit
#             if current_chunk_tokens + word_tokens <= tokens_per_chunk:
#                 # Add the word to the current chunk
#                 current_chunk += " " + word
#                 current_chunk_tokens += word_tokens
#             else:
#                 # Start a new chunk
#                 text_chunks.append(current_chunk.strip())
#                 current_chunk = word
#                 current_chunk_tokens = word_tokens
#
#                 # Add overlap
#                 if len(text_chunks) > 0 and overlap > 0:
#                     overlap_text = " ".join(text_chunks[-1].split()[-overlap:])
#                     current_chunk = overlap_text + " " + current_chunk
#                     current_chunk_tokens += num_tokens_from_string(
#                         overlap_text, model
#                     )
#
#         # Add the last chunk
#         if current_chunk:
#             text_chunks.append(current_chunk.strip())
#
#         return text_chunks
#
#
#     def _merge_into_chunks(
#         self,
#         words: List[str],
#         chunk_size: int = DEFAULT_CHUNK_SIZE,
#         overlap_size: int = DEFAULT_CHUNK_OVERLAP_SIZE,
#     ):
#         pass
#
#     def _split_text(self, text: str, chunk_size: int) -> List[str]:
#         """
#         _Split incoming text and return chunks with overlap size.
#
#         Has a preference for complete sentences, phrases, and minimal overlap.
#         """
#         if text == "":
#             return []
#
#         with self.callback_manager.event(
#             CBEventType.CHUNKING, payload={EventPayload.CHUNKS: [text]}
#         ) as event:
#             splits = self._split(text, chunk_size)
#             chunks = self._merge(splits, chunk_size)
#
#             event.on_end(payload={EventPayload.CHUNKS: chunks})
#
#         return chunks
#
#     def _split(self, text: str, chunk_size: int) -> List[_Split]:
#         """Break text into splits that are smaller than chunk size.
#
#         The order of splitting is:
#         1. split by paragraph separator
#         2. split by chunking tokenizer (default is nltk sentence tokenizer)
#         3. split by second chunking regex (default is "[^,\.;]+[,\.;]?")
#         4. split by default separator (" ")
#
#         """
#         if len(self.tokenizer(text)) <= chunk_size:
#             return [Chunk(text, is_sentence=True)]
#
#         for split_fn in self._split_fns:
#             splits = split_fn(text)
#             if len(splits) > 1:
#                 break
#
#         if len(splits) > 1:
#             is_sentence = True
#         else:
#             for split_fn in self._sub_sentence_split_fns:
#                 splits = split_fn(text)
#                 if len(splits) > 1:
#                     break
#             is_sentence = False
#
#         new_splits = []
#         for split in splits:
#             split_len = len(self.tokenizer(split))
#             if split_len <= chunk_size:
#                 new_splits.append(_Split(split, is_sentence=is_sentence))
#             else:
#                 ns = self._split(split, chunk_size=chunk_size)
#                 if len(ns) == 0:
#                     print("0 length split")
#                 # recursively split
#                 new_splits.extend(ns)
#         return new_splits
#
#     def _merge(self, splits: List[_Split], chunk_size: int) -> List[str]:
#         """Merge splits into chunks."""
#         chunks: List[str] = []
#         cur_chunk: List[str] = []
#         cur_chunk_len = 0
#         while len(splits) > 0:
#             cur_split = splits[0]
#             cur_split_len = len(self.tokenizer(cur_split.text))
#             if cur_split_len > chunk_size:
#                 raise ValueError("Single token exceed chunk size")
#             if (
#                 cur_chunk_len + cur_split_len > chunk_size
#                 and len(cur_chunk) > 0
#             ):
#                 # if adding split to current chunk exceed chunk size: close out chunk
#                 chunks.append("".join(cur_chunk).strip())
#                 cur_chunk = []
#                 cur_chunk_len = 0
#             else:
#                 if (
#                     cur_split.is_sentence
#                     or cur_chunk_len + cur_split_len
#                     < chunk_size - self.chunk_overlap
#                     or len(cur_chunk) == 0
#                 ):
#                     # add split to chunk
#                     cur_chunk_len += cur_split_len
#                     cur_chunk.append(cur_split.text)
#                     splits.pop(0)
#                 else:
#                     # close out chunk
#                     chunks.append("".join(cur_chunk).strip())
#                     cur_chunk = []
#                     cur_chunk_len = 0
#
#         # handle the last chunk
#         chunk = "".join(cur_chunk).strip()
#         if chunk:
#             chunks.append(chunk)
#
#         # run postprocessing to remove blank spaces
#         chunks = self._postprocess_chunks(chunks)
#
#         return chunks


class SentenceChunker(Chunker, BaseModel):
    """Create chunks by dividing text into sentences."""

    num_sentences: int = Field(
        default=DEFAULT_NUM_SENTANCES, alias="num_sentences"
    )
    tokenizer: str = Field(default="spacy", alias="tokenizer")
    length_function: Callable = Field(default=len, alias="text_length_function")
    overlap_size: int = Field(default=DEFAULT_SENTENCE_OVERLAP_SIZE)

    def create_chunks(self, text: str) -> DocList[TextChunk]:
        ...


class ContextAwareTextChunker(TextChunker, BaseModel):
    """Generate context aware text chunks given any text input"""
