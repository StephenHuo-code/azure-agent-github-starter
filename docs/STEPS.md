# 执行步骤（使用 OPENAI_API_KEY 环境变量，不使用 Azure OpenAI 服务）

1. Azure 登录与订阅设置
```bash
az login
az account set --subscription "6376398c-bc02-4da5-a8c1-fc3e76b57990"
```

2. 创建资源组
```bash
az group create --name rg-ai --location southeastasia
```

3. 创建 Container Apps 环境
```bash
az containerapp env create --name cae-agent --resource-group rg-ai --location southeastasia
```

4. 在 Azure Entra ID 创建应用注册 (App Registration)
   - 记录 AZURE_CLIENT_ID = fdf7b6b2-52c6-4ed5-839b-ee27c6e69351
   - 记录 AZURE_TENANT_ID = 4fcc0957-8514-4a11-ab10-5c7c7e0af57c
   - 添加 Federated Credential：
     - Issuer: https://token.actions.githubusercontent.com
     - Subject: repo:StephenHuo-code/azure-agent-github-starter:environment:prod
   - 赋予 Contributor 权限到资源组 rg-ai

5. GitHub 仓库准备
   - 创建仓库 azure-agent-github-starter 在账户 StephenHuo-code
   - Push 代码到 main 分支
   - Settings → Actions → General → Workflow permissions = Read and write
   - Settings → Environments → Add environment prod
   - 在 prod 环境添加 Secrets：
     - AZURE_CLIENT_ID = fdf7b6b2-52c6-4ed5-839b-ee27c6e69351
     - AZURE_TENANT_ID = 4fcc0957-8514-4a11-ab10-5c7c7e0af57c
     - AZURE_SUBSCRIPTION_ID = 6376398c-bc02-4da5-a8c1-fc3e76b57990
     - AZURE_RESOURCE_GROUP = rg-ai
     - AZURE_CONTAINERAPP_NAME = agent
     - GHCR_PAT = <你的 GHCR token>
     - OPENAI_API_KEY = <你的 OpenAI API Key>

6. 触发部署
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

7. 验证部署
```bash
az containerapp show -g rg-ai -n agent --query "properties.configuration.ingress.fqdn" -o tsv
curl -s https://<FQDN>/healthz
```
