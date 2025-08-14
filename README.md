# Azure Agent — OpenAI-only (no Azure OpenAI)

Configured for:
- Owner/Repo: **StephenHuo-code/azure-agent-github-starter**
- Resource Group: **rg-ai**
- Location: **southeastasia**
- CA Environment: **cae-agent**
- Container App: **agent**

## Local dev
```bash
pip install -r requirements.txt

# 复制环境变量配置模板
cp env.example .env

# 编辑 .env 文件，设置你的配置
# 然后设置 OpenAI API 密钥
export OPENAI_API_KEY=...

# 启动应用
uvicorn app.main:app --reload
```

## Deployment
Push to `main` triggers CI/CD (GHCR → Azure).

### Required GitHub Environment `prod` secrets
- AZURE_CLIENT_ID = fdf7b6b2-52c6-4ed5-839b-ee27c6e69351
- AZURE_TENANT_ID = 4fcc0957-8514-4a11-ab10-5c7c7e0af57c
- AZURE_SUBSCRIPTION_ID = 6376398c-bc02-4da5-a8c1-fc3e76b57990
- AZURE_RESOURCE_GROUP = rg-ai
- AZURE_CONTAINERAPP_NAME = agent
- GHCR_PAT = <your token>
- OPENAI_API_KEY = <your key>
