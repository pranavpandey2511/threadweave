from __future__ import annotations

from pydantic import BaseModel, ValidationError, validator, Field
from typing import List, Dict, Union, Optional, Type, Any
import uuid
from docarray import BaseDoc, DocVec, DocList
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

from sections import Section


class Document(BaseDoc):
    _id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique ID of the document.",
        alias="doc_id",
    )
    summary: Optional[str]
    pages: DocList[Page]
    sections: DocList[Section]
    page_ids: List[uuid.UUID] = Field(default_factory=list)
    section_ids: List[uuid.UUID] = Field(default_factory=list)
    metadata: Metadata


class Page(BaseDoc):
    """A page is a collection of sections.
    The idea is to arrange different kind of sections in a page in an orderly fashion.
    """

    _id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        # This will allow the model to be created from a dictionary as well
        orm_mode = True

    def __init__(self, page_number: int):
        self.page_number: int = page_number
        self.sections: List[Section] = []

    def __str__(self):
        return "\n\n------------\n\n".join(
            [str(section) for section in self.sections]
        )


class Metadata(BaseDoc):
    """Metadata class for documents."""

    url: Optional[str] = None
    version: Optional[str] = None
    record_locator: Optional[
        Dict[str, Any]
    ] = None  # Values must be JSON-serializable
    date_created: Optional[str] = None
    date_modified: Optional[str] = None
    date_processed: Optional[str] = None

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if value is not None
        }
