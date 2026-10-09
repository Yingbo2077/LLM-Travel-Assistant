import chromadb
from backend.embedding import create_embedding



client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_collection(
    name="travel"
)



def search_knowledge(query, top_k=3):


    query_vector = create_embedding(
        [query]
    )


    result = collection.query(

        query_embeddings=query_vector.tolist(),

        n_results=top_k

    )


    documents = result["documents"][0]

    metadatas = result["metadatas"][0]


    results = []


    for doc, meta in zip(
        documents,
        metadatas
    ):

        results.append({

            "content": doc,

            "metadata": meta

        })


    return results



# ============================
# 测试入口
# ============================

if __name__ == "__main__":


    query = "米兰有什么适合情侣晚上拍照的地方"


    results = search_knowledge(
        query,
        top_k=3
    )


    print("\n搜索问题:")
    print(query)


    print("\n检索结果:")


    for i, item in enumerate(results):

        print("====================")

        print(
            "结果:",
            i+1
        )


        print(
            "内容:"
        )

        print(
            item["content"]
        )


        print(
            "metadata:"
        )

        print(
            item["metadata"]
        )