from abc import ABC, abstractmethod
from typing import Union

from docarray import DocList

from threadweave.chunker.schema import Chunk


class VectorStore(ABC):
    @abstractmethod
    def _connect_to_store(self, connection_params: dict):
        ...

    @abstractmethod
    def index(self, data: Union[DocList, Chunk]):
        ...

    @abstractmethod
    def query_db(self):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def delete(self):
        ...
