from fastapi import FastAPI
from pydantic import BaseModel
 
print("111111111")

# 👉 import your graph here
from rag_movie_suggestion import graph

app = FastAPI()

# request format
class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: QueryRequest):
    try:
        result = graph.invoke({"query": request.query})

        return {
            "response": result["response"]
        }

    except Exception as e:
        return {
            "response": f"Error: {str(e)}"
        }
    
