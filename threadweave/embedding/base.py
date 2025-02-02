import asyncio
from abc import ABC, abstractmethod
from typing import Callable, Optional, Dict, List
import numpy as np
from threadweave.document.base import Document
from threadweave.document.chunk.base import Chunk

EMB_TYPE = np.ndarray
DEFAULT_EMBED_BATCH_SIZE = 10

# Assuming Document, Chunk, etc. are imported or defined

class BaseEmbedding(ABC):
    def __init__(self, tokenizer: Optional[Callable] = None) -> None:
        self._total_tokens_used = 0
        self._tokenizer = tokenizer
        self._document_queue: List[Document] = []

    @abstractmethod
    def _get_embedding(self, content: str) -> EMB_TYPE:
        """Retrieve the embedding for a given content."""

    async def _aget_embedding(self, content: str) -> EMB_TYPE:
        """Asynchronous version of _get_embedding."""
        return self._get_embedding(content)

    def get_chunk_embedding(self, chunk: Chunk) -> EMB_TYPE:
        if self._tokenizer:
            self._total_tokens_used += len(self._tokenizer(chunk.content))
        return self._get_embedding(chunk.content)

    async def aget_chunk_embedding(self, chunk: Chunk) -> EMB_TYPE:
        self._total_tokens_used += len(self._tokenizer(chunk.content))
        return await self._aget_embedding(chunk.content)

    def queue_document_for_embedding(self, document: Document) -> None:
        """Queue entire document for embedding."""
        self._document_queue.append(document)

    def get_queued_document_embeddings(self) -> Dict[str, Dict[str, EMB_TYPE]]:
        """Retrieve embeddings for all chunks within queued documents."""
        result = {}
        for document in self._document_queue:
            doc_embeddings = {}
            for page in document.pages or []:
                for chunk in page.chunks or []:
                    doc_embeddings[chunk._id] = self.get_chunk_embedding(chunk)
            for chunk in document.chunks or []:
                doc_embeddings[chunk._id] = self.get_chunk_embedding(chunk)
            result[document._id] = doc_embeddings
        self._document_queue.clear()
        return result

    async def aget_queued_document_embeddings(self) -> Dict[str, Dict[str, EMB_TYPE]]:
        """Asynchronous version of get_queued_document_embeddings."""
        result = {}
        for document in self._document_queue:
            doc_embeddings = {}
            for page in document.pages or []:
                for chunk in page.chunks or []:
                    doc_embeddings[chunk._id] = await self.aget_chunk_embedding(chunk)
            for chunk in document.chunks or []:
                doc_embeddings[chunk._id] = await self.aget_chunk_embedding(chunk)
            result[document._id] = doc_embeddings
        self._document_queue.clear()
        return result

    @property
    def total_tokens_used(self) -> int:
        """get total tokens."""
        return self._total_tokens_used
