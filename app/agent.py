import logging
import os
from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from openai import AuthenticationError, RateLimitError, APIError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleAgent:
    """Minimal async agent using OpenAI via langchain-openai."""
    def __init__(self):
        try:
            # 检查环境变量
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.error("OPENAI_API_KEY environment variable is not set")
                raise ValueError("OPENAI_API_KEY environment variable is required")
            
            # 记录配置信息
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            temperature = float(os.getenv("MODEL_TEMPERATURE", "0.2"))
            
            logger.info(f"Initializing agent with model: {model}, temperature: {temperature}")
            logger.info(f"API Key length: {len(api_key)} characters")
            logger.info(f"API Key prefix: {api_key[:7]}...")
            
            self.llm = ChatOpenAI(
                model=model, 
                temperature=temperature,
                api_key=api_key,
                timeout=30,  # 设置超时时间
                max_retries=3  # 设置重试次数
            )
            
            logger.info("Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise

    async def run(self, message: str, memory: Optional[Dict] = None) -> str:
        try:
            logger.info(f"Processing message: {message[:100]}...")
            logger.info(f"Memory: {memory}")
            
            prompt = f"You're a concise, helpful assistant. User says: {message}"
            logger.info(f"Generated prompt: {prompt[:100]}...")
            
            # 测试 OpenAI API 连接
            logger.info("Calling OpenAI API...")
            resp = await self.llm.ainvoke(prompt)
            
            logger.info(f"API response received, content length: {len(resp.content)}")
            return resp.content
            
        except AuthenticationError as e:
            logger.error(f"OpenAI Authentication Error: {e}")
            return "抱歉，API 认证失败，请检查 API 密钥是否正确。"
            
        except RateLimitError as e:
            logger.error(f"OpenAI Rate Limit Error: {e}")
            return "抱歉，API 调用频率超限，请稍后再试。"
            
        except APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            return f"抱歉，OpenAI API 调用失败: {str(e)}"
            
        except Exception as e:
            logger.error(f"Unexpected error in agent.run: {e}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {str(e)}")
            
            # 返回用户友好的错误信息
            return f"抱歉，处理您的请求时出现了意外错误: {str(e)}"
