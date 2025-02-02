Vector Stores are data structures that are used to store vectors. They are optimized for operations that are commonly performed on vectors, such as dot product, cosine similarity, and nearest neighbor search.

Currently we support these vector store: (You can easily extend and add your own vector store)

1. **Weaviate** (default): This is the base class for all vector stores. It provides the basic functionality that all vector stores need.
2. **Pinecone**: This is a vector store that uses the Pinecone service. It is designed to be highly scalable and efficient.
   1. PineconeStore
3. **Qdrant**: This vector store uses the Qdrant service. It is designed to be easy to use and integrate with other services.
4. **Chroma**:
5. **VectorDB** from JinaAI :
   If you want to implement your own vector store, you can extend the Base Vector Store class. Here is a basic example:
