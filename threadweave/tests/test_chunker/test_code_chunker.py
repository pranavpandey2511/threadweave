from threadweave.chunker.code_chunker import CodeChunker


def test_code_chunker():
    chunkern = CodeChunker(
        directory_path="/Users/pranavpandey/Projects/Personal_Projects/fastchain/data/code",
        max_chunk_size=500,
        coalesce=50,
    )
    pages = chunkern.create_chunks()

    for chunk in pages[0].chunks:
        print("**************")
        print(chunk)
        print(chunk.content)
        print(chunk.doc_id)
        print("**************")
