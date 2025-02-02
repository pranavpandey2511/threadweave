from __future__ import annotations

from pydantic import BaseModel, ValidationError, validator, Field
from typing import List, Dict, Optional, Type, Any
import uuid
from docarray import BaseDoc, DocList
from docarray.typing import (
    NdArray,
    NdArrayEmbedding,
    AudioNdArray,
    VideoNdArray,
    AnyEmbedding,
    ImageUrl,
    AudioUrl,
    TextUrl,
    Mesh3DUrl,
    PointCloud3DUrl,
    VideoUrl,
    AnyUrl,
    ID,
    AnyTensor,
    ImageTensor,
    AudioTensor,
    VideoTensor,
    ImageNdArray,
    ImageBytes,
    VideoBytes,
    AudioBytes,
)

from threadweave.document.chunk.base import Chunk

class Metadata(BaseDoc):
    """Metadata class for documents."""

    path: Optional[str] = None
    total_pages: Optional[int] = None
    version: Optional[str] = None
    record_locator: Optional[
        Dict[str, Any]
    ] = None  # Values must be JSON-serializable
    date_created: Optional[str] = None
    date_modified: Optional[str] = None
    date_processed: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            key: value
            for key, value in self.__dict__.items()
            if value is not None
        }

    def __str__(self) -> str:
        return str(self.to_dict())

class Page(BaseDoc):
    """A page is a collection of sections.
    The idea is to arrange different kind of chunks in a page in an orderly fashion.
    """

    _id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    doc_id: Optional[str]
    page_info: Optional[str]
    hash_value: Optional[str]
    chunks: Optional[DocList[Chunk]]

    class Config:
        # This will allow the model to be created from a dictionary as well
        orm_mode = True

    def __str__(self):
        return "\n\n------------\n\n".join(
            [str(chunk) for chunk in self.chunks]
        )



class Document(BaseDoc):
    _id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique ID of the document.",
        alias="doc_id",
    )
    doc_summary: Optional[str] = "NA"
    pages: Optional[DocList[Page]]
    chunks: Optional[DocList[Chunk]]
    metadata: Metadata


