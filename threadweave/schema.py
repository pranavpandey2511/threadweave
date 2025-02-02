from __future__ import annotations

from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError, validator, Field
from typing import List, Dict, Union, Optional, Type
from uuid import uuid4
from docarray import BaseDoc
import uuid


class Document(BaseDoc):
    id_: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique ID of the node.",
        alias="doc_id",
    )
    content: str
    element_ids: List[str] = Field(default_factory=list)
    metadata: Dict


class BaseElement(BaseDoc):
    _id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique ID of the node.",
        alias="doc_id",
    )
    document_id: str
    content: str
    prev: Type[BaseElement] = None
    next: Type[BaseElement] = None
