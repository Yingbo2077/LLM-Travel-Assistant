import os

from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter



def load_documents(folder_path):

    """
    从文件夹读取原始文档
    返回 LangChain Document列表
    """

    documents = []


    for filename in os.listdir(folder_path):

        if filename.endswith(".txt"):


            file_path = os.path.join(
                folder_path,
                filename
            )


            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()



            document = Document(

                page_content=content,

                metadata={
                    "source": filename
                }

            )


            documents.append(
                document
            )


    return documents



def split_documents(documents):

    """
    文本切片
    """

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=300,

        chunk_overlap=50

    )


    chunks = splitter.split_documents(
        documents
    )


    return chunks



if __name__ == "__main__":


    docs = load_documents(
        "data/travel_docs"
    )


    print(
        "原始文档数量:",
        len(docs)
    )


    chunks = split_documents(
        docs
    )


    print(
        "切片数量:",
        len(chunks)
    )


    for chunk in chunks:

        print("================")

        print(
            chunk.page_content
        )


        print(
            chunk.metadata
        )