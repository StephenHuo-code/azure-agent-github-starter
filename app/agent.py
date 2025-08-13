
from typing import Dict, Optional
import os

# LangChain model clients
from langchain_openai import ChatOpenAI
try:
    from langchain_openai import AzureChatOpenAI  # available in langchain-openai
except ImportError:
    AzureChatOpenAI = None


class SimpleAgent:
    """A minimal async agent wrapper using LangChain's Chat* clients.
    It supports either OpenAI (default) or Azure OpenAI when env vars are set.
    """

    def __init__(self):
        # If Azure OpenAI envs are present, prefer Azure
        use_azure = all([
            os.getenv("AZURE_OPENAI_ENDPOINT"),
            os.getenv("AZURE_OPENAI_API_VERSION"),
            os.getenv("AZURE_OPENAI_DEPLOYMENT")
        ])

        temperature = float(os.getenv("MODEL_TEMPERATURE", "0.2"))
        if use_azure and AzureChatOpenAI is not None:
            self.llm = AzureChatOpenAI(
                azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
                api_version=os.environ["AZURE_OPENAI_API_VERSION"],
                temperature=temperature,
            )
        else:
            # Fallback to public OpenAI (requires OPENAI_API_KEY)
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            self.llm = ChatOpenAI(model=model, temperature=temperature)

    async def run(self, message: str, memory: Optional[Dict] = None) -> str:
        prompt = f"You're a concise, helpful assistant. User says: {message}"
        resp = await self.llm.ainvoke(prompt)
        return resp.content
