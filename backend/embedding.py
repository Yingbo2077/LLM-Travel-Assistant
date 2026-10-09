from sentence_transformers import SentenceTransformer


# 加载embedding模型
model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)


def create_embedding(texts):

    vectors = model.encode(
        texts
    )

    return vectors



if __name__ == "__main__":


    texts = [
        "米兰大教堂是著名旅游景点",
        "布雷拉美术馆收藏大量艺术作品"
    ]


    vectors = create_embedding(
        texts
    )


    print(vectors)

    print(
        vectors.shape
    )