from embedding import create_embedding
from rag import load_documents, split_documents

import chromadb



client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="travel"
)



# 1. 加载原始文档

docs = load_documents(
    "data/travel_docs"
)


# 2. 文本切片

chunks = split_documents(
    docs
)



texts = []

metadatas = []

ids = []



for i, doc in enumerate(chunks):


    # Document正文

    texts.append(
        doc.page_content
    )


    # Document metadata

    metadatas.append(
        doc.metadata
    )


    ids.append(
        str(i)
    )



# 3. embedding

vectors = create_embedding(
    texts
)



# 4. 写入ChromaDB

collection.add(

    documents=texts,

    embeddings=vectors.tolist(),

    metadatas=metadatas,

    ids=ids

)



print(
    "写入数量:",
    len(texts)
)