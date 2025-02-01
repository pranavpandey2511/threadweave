import chromadb
from typing import Union
from docarray import DocList
from fastchain.chunker.schema import Chunk
from fastchain.vector_stores.base import VectorStore



collection.add(
    embeddings=[[1.2, 2.3, 4.5], [6.7, 8.2, 9.2]],
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id1", "id2"]
)


# query
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2
)

class ChromaStore(VectorStore):

    def __init__(self, *args, **kwargs):

        # Persistent local storage
        if kwargs.get("persist", False):
            assert kwargs.get("path", None), "No path provided for persistent storage"
            self.chroma_client = chromadb.PersistentClient(path=kwargs["path"])
        # In-memory client
        else:
            self.chroma_client = chromadb.Client()


    def _connect_to_store(self, connection_params: dict):
        if connection_params.in_memory == True:
            self.collection = self.chroma_client.create_collection(name="my_collection")
        if connection_params.local_storage == True:
            assert connection_params.dir is not False, "No path provided for local storage"
            self.collection = self.chroma_client.create_collection(name="my_collection")


    def index(self, data: Union[DocList, Chunk]):
        ...

    def query_db(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...
