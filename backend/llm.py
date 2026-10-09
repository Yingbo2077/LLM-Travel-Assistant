from openai import OpenAI
import os
from dotenv import load_dotenv

from backend.retriever import search_knowledge


load_dotenv()


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)



def ask_llm(user_query):


    # 1. 从知识库检索资料

    documents = search_knowledge(
        user_query
    )


    # 2. 拼接知识上下文

    context = "\n\n".join(
    doc["content"] for doc in documents
)


    # 3. 构造增强Prompt

    prompt = f"""

你是一名专业旅游规划助手。

请根据下面提供的旅游知识库内容回答用户问题。

【知识库资料】

{context}


【用户问题】

{user_query}


要求：

1. 优先使用知识库信息
2. 不确定的信息不要编造
3. 给出具体旅游建议

"""


    # 4. 调用DeepSeek

    response = client.chat.completions.create(

        model="deepseek-chat",

        messages=[

            {
                "role":"system",
                "content":
                "你是一个专业旅行规划助手"
            },

            {
                "role":"user",
                "content":prompt
            }

        ]

    )


    return response.choices[0].message.content