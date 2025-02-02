from __future__ import annotations

import os
from typing import List, Dict, Union, Optional, Type, Any
import uuid
from pydantic import Field, create_model
from docarray import BaseDoc
from docarray.typing import NdArray, NdArrayEmbedding
from uuid import UUID


# DEFAULT_EMB_SIZE = os.environ.get('DEFAULT_EMB_SIZE')
# Chunk = create_model('Chunk', _id= (UUID, Field(
#         default_factory=lambda: uuid.uuid4(),
#         description="Unique ID of the chunk.",
#         alias="chunk_id",
#     )),
#     document_id= (Optional[UUID],...),
#     page_id=(Optional[UUID], ...),
#     EMBEDDING_SIZE=(Optional[int], DEFAULT_EMB_SIZE),
#     embedding=(Optional[NdArrayEmbedding[DEFAULT_EMB_SIZE]], Field(
#         is_embedding=True
#     )),
#     content_type= (str,"text"),
#     # Refer this to know why this is set to any https://docs.docarray.org/user_guide/storing/index_weaviate/#notes
#     content=(Any, ""),
#     coordinates= (Optional[tuple],...),
#     _previous=(Union[Type[Chunk], None],  None),
#     _next= (Union[Type[Chunk], None],  None),
#     __base__=(BaseDoc,...))

class Chunk(BaseDoc):
    _id: UUID = Field(
        default_factory=lambda: uuid.uuid4(),
        description="Unique ID of the chunk.",
        alias="chunk_id",
    )
    document_id: Optional[UUID]
    page_id: Optional[UUID]
    EMBEDDING_SIZE: Optional[int]
    embedding: Optional[NdArrayEmbedding[EMBEDDING_SIZE]] = Field(
        is_embedding=True
    )
    content_type: str = "text"
    # Refer this to know why this is set to any https://docs.docarray.org/user_guide/storing/index_weaviate/#notes
    content: Any = ""
    coordinates: Optional[tuple]
    _previous: Union[Type[Chunk], None] = None
    _next: Union[Type[Chunk], None] = None


    @classmethod
    def __set_embedding_size(cls, model_name):
        ...
