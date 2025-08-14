from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from app.agent import SimpleAgent

app = FastAPI(title="Agent Service", version="1.2.0")
agent = SimpleAgent()

class ChatReq(BaseModel):
    message: str
    thread_id: str | None = None

@app.get("/healthz")
async def healthz():
    return {"ok": True}

@app.post("/chat")
async def chat(req: ChatReq):
    text = await agent.run(req.message, memory={"thread_id": req.thread_id})
    return {"reply": text}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
