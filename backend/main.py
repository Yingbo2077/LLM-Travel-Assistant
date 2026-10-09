from fastapi import FastAPI
from backend.llm import ask_llm


app = FastAPI()


@app.get("/")
def home():

    return {
        "message":
        "LLM Travel Assistant Running"
    }



@app.get("/chat")
def chat(query:str):

    answer = ask_llm(query)

    return {
        "question":query,
        "answer":answer
    }