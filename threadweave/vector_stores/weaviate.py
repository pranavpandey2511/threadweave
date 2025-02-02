from docarray.index.backends.weaviate import (
    WeaviateDocumentIndex,
    EmbeddedOptions,
)
from typing import List, Union, Optional

from docarray import DocList
import os
from dotenv import load_dotenv

from threadweave.vector_stores.base import VectorStore
from threadweave.document.chunk.base import Chunk
import logging

logger = logging.getLogger(__name__)

class WeaviateStore(VectorStore):
    def __init__(self, host: str, auth_method: str = "none"):
        self.host = host
        self.auth_method = auth_method
        self.doc_index = self._connect_to_store(host, auth_method)


    def _connect_to_store(self, host: str, auth_method: str = "none"):
        if auth_method == "none":
            logger.warning("No auth method provided, starting a new Weaviate service")

            dbconfig = WeaviateDocumentIndex.DBConfig(
                embedded_options=EmbeddedOptions()
            )
        elif auth_method == "password":
            self.dbconfig = WeaviateDocumentIndex.DBConfig(
                username=os.environ.get("WEAVIATE_USERNAME"),
                password=os.environ.get("WEAVIATE_PASSWORD"),
                host=host,
            )
        elif auth_method == "api":
            self.dbconfig = WeaviateDocumentIndex.DBConfig(
                auth_api_key=os.environ.get(
                    "WEAVIATE_API_KEY"
                ),  # Replace with your own API key
                host="http://localhost:8080",  # Replace with your endpoint
            )

        return WeaviateDocumentIndex[Chunk](db_config=self.dbconfig)

    def _create_index(self, batch_index: int=20, dynamic: bool=False, timeout_retries: int=3, num_workers: int=1):
        self.batch_config = {
            "batch_size": batch_index,
            "dynamic": dynamic,
            "timeout_retries": timeout_retries,
            "num_workers": num_workers,
        }

        self.runtime_config = WeaviateDocumentIndex.RuntimeConfig(
            batch_config=self.batch_config
        )

        store = WeaviateDocumentIndex[Chunk]()
        store.configure(self.runtime_config)  # Batch settings being passed on

        return store

    def index(self, data: Union[DocList, Chunk]):

        # Create the actual index
        self.store = self._create_index()

        if isinstance(data, Chunk):
            self.store.index(DocList[data])
            return
        if isinstance(data, DocList) and data.__class__.__name__ == "Page":
            self.store.index(data)
            return

        if isinstance(data, DocList) and data.__class__.__name__ == "Document":
            for page in data.Pages:
                self.store.index(page)
            return
        logger.info("Indexing completed successfully")

    def query_db(self, query: Union[DocList, Chunk], top_k: int = 5):

        # find similar documents
        matches, scores = self.store.find(query, limit=top_k)

        print(f'{matches=}')
        print(f'{matches.text=}')
        print(f'{scores=}')

        return matches, scores
    def update(self):
        ...

    def delete(self, doc_ids: List[int]):
        del self.doc_index[doc_ids]
