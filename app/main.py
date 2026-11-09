from fastapi import FastAPI
from app.graph import metro_graph
from pydantic import BaseModel

app = FastAPI(
    title="AI METRO ASSISTANT"
)

class ChatRequest(BaseModel):
    question:str



@app.post("/ask_agent")
def ask_metro_agent(request:ChatRequest):
    
    response = metro_graph.invoke({
        "messages":[
            {
                "role":"user",
                "content":request.question
            }
        ]
    })
    
    final_message = response["messages"][-1]
    
    return {
        "question":request.question,
        "answer":final_message.content
    }