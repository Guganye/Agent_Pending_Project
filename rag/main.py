import chromadb
import uuid
"""
Chroma gives you everything you need for retrieval: store 
embeddings with metadata, search with dense and 
sparse vectors, filter by metadata, and retrieve across 
text, images, and more.
VectorDB 检索+增强+生成
"""


chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection") # 本地连接
with open("my_collection.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

collection.add(
    ids = [str(uuid.uuid4()) for _ in range(len(lines))],
    documents=lines,
    metadatas=[{"line": i} for i in range(len(lines))],
)

# print(collection.peek()) # ids, vectors, documents, metadatas

results = collection.query(
    query_texts=[
        "什么是python",
        "rag"
    ],
    n_results=5 # TopK
)
for i, query_results in enumerate(results["documents"]):
    print(f"\nQuery {i}")
    print("\n".join(query_results))


