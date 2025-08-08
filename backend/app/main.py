from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import QueryRequest
from app.agent import agent

app = FastAPI()

# CORS config to allow requests from frontend (like localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "It works on Fly!"}

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        response = agent.run(request.question)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}
