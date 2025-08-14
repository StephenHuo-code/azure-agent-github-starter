import sys
import os
import logging
import traceback
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from app.agent import SimpleAgent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agent Service", version="1.2.0")

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    logger.error(f"Exception type: {type(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error", 
            "detail": str(exc),
            "type": str(type(exc).__name__)
        }
    )

# 初始化代理
agent = None
try:
    logger.info("Initializing SimpleAgent...")
    agent = SimpleAgent()
    logger.info("SimpleAgent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize SimpleAgent: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")

class ChatReq(BaseModel):
    message: str
    thread_id: str | None = None

@app.get("/healthz")
async def healthz():
    try:
        if agent is None:
            logger.warning("Health check failed: Agent not initialized")
            return {"ok": False, "error": "Agent not initialized"}
        
        # 测试代理是否正常工作
        test_message = "test"
        try:
            result = await agent.run(test_message)
            logger.info("Health check passed: Agent is working")
            return {"ok": True, "agent_status": "working"}
        except Exception as e:
            logger.error(f"Health check failed: Agent test failed - {e}")
            return {"ok": False, "error": f"Agent test failed: {str(e)}"}
            
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {"ok": False, "error": str(e)}

@app.get("/debug")
async def debug():
    """调试信息端点"""
    return {
        "agent_initialized": agent is not None,
        "openai_api_key_set": bool(os.getenv("OPENAI_API_KEY")),
        "openai_api_key_length": len(os.getenv("OPENAI_API_KEY", "")),
        "openai_model": os.getenv("OPENAI_MODEL"),
        "temperature": os.getenv("MODEL_TEMPERATURE"),
        "python_version": sys.version,
        "working_directory": os.getcwd()
    }

@app.post("/chat")
async def chat(req: ChatReq):
    try:
        if agent is None:
            logger.error("Chat request failed: Agent not available")
            raise HTTPException(status_code=500, detail="Agent service not available")
        
        logger.info(f"Chat request received: {req.message[:100]}...")
        logger.info(f"Thread ID: {req.thread_id}")
        
        text = await agent.run(req.message, memory={"thread_id": req.thread_id})
        
        logger.info(f"Chat response generated, length: {len(text)}")
        return {"reply": text}
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
