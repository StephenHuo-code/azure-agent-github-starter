from typing import Dict, Optional
import os
from langchain_openai import ChatOpenAI

class SimpleAgent:
    """Minimal async agent using OpenAI via langchain-openai."""
    def __init__(self):
        # Requires OPENAI_API_KEY in environment
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        temperature = float(os.getenv("MODEL_TEMPERATURE", "0.2"))
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    async def run(self, message: str, memory: Optional[Dict] = None) -> str:
        prompt = f"You're a concise, helpful assistant. User says: {message}"
        resp = await self.llm.ainvoke(prompt)
        return resp.content
