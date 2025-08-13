
# Azure Agent (GitHub Actions + GHCR + Azure Container Apps)

A minimal, production-ready template to deploy an AI Agent API to **Azure Container Apps** using **GitHub Actions** and **GitHub Container Registry (GHCR)**.
- Language: **Python + FastAPI**
- LLM: `langchain-openai` (supports **OpenAI** and **Azure OpenAI**)
- CI/CD: **GitHub Actions** → build Docker image → push to **GHCR** → deploy to **Azure Container Apps**

> ✅ No LangChain Platform required. Pure GitHub + Azure.

---

## Directory Structure
```
.
├─ app/
│  ├─ main.py          # FastAPI entry
│  └─ agent.py         # Agent logic (OpenAI or Azure OpenAI)
├─ tests/
│  └─ test_health.py
├─ .github/workflows/
│  └─ deploy.yml       # CI/CD pipeline
├─ .env.example
├─ requirements.txt
├─ Dockerfile
├─ .gitignore
└─ README.md
```

## Quick Start (Local)

1. Python 3.11+
2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables:
   - **Option A: OpenAI**
     ```bash
     export OPENAI_API_KEY=...
     export OPENAI_MODEL=gpt-4o-mini
     ```
   - **Option B: Azure OpenAI**
     ```bash
     export AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com
     export AZURE_OPENAI_API_VERSION=2024-08-01-preview
     export AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
     # If not using Managed Identity:
     export AZURE_OPENAI_API_KEY=...
     ```
4. Run:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Test:
   ```bash
   curl -s http://localhost:8000/healthz
   curl -s -X POST http://localhost:8000/chat -H "content-type: application/json" -d '{"message":"hello"}'
   ```

---

# Azure Deployment (with GitHub)

This repo uses **GitHub Actions** to build/push a Docker image to **GHCR** and deploy to **Azure Container Apps** automatically on every push to `main`.

### A. Prepare Azure (one-time)
1. **Resource group** (replace names/region as needed):
   ```bash
   az group create -n rg-ai -l southeastasia
   ```
2. (Optional) Create a **Container Apps Environment** (can also be auto-created by the Action on first deploy):
   ```bash
   az containerapp env create -g rg-ai -n cae-agent -l southeastasia
   ```
3. Create a **Service Principal** and configure **OIDC (Federated Credentials)** for GitHub Actions.  
   - In Azure Portal → Entra ID → App registrations → New registration.  
   - Note the **Client ID** and **Tenant ID**.  
   - Add a **Federated Credential** for your GitHub repo (environment `prod`).  
   - Assign this principal the required roles on the resource group, e.g. **Contributor** (or more restrictive Container App roles).

### B. Configure GitHub Environment & Secrets
Create an **Environment** named `prod` (Settings → Environments), then add these **Secrets**:

- **Azure auth via OIDC**
  - `AZURE_CLIENT_ID`
  - `AZURE_TENANT_ID`
  - `AZURE_SUBSCRIPTION_ID`
  - `AZURE_RESOURCE_GROUP` (e.g. `rg-ai`)
  - `AZURE_CONTAINERAPP_NAME` (e.g. `agent-app`)

- **GHCR pull for Azure**
  - `GHCR_PAT` → GitHub Personal Access Token with `read:packages`/`write:packages`

- **Model keys (choose one option)**
  - Option A (OpenAI): `OPENAI_API_KEY`
  - Option B (Azure OpenAI):  
    - `AZURE_OPENAI_API_KEY` (if not using Managed Identity)  
    - `AZURE_OPENAI_ENDPOINT` (e.g. `https://YOUR-RESOURCE.openai.azure.com`)  
    - `AZURE_OPENAI_DEPLOYMENT` (e.g. `gpt-4o-mini`)

> The workflow (`.github/workflows/deploy.yml`) references these secrets and environment variables.

### C. Trigger Deployment
- Push to `main` (or click **Run workflow**):
  - GitHub builds & pushes `ghcr.io/OWNER/REPO:latest`
  - GitHub deploys to **Azure Container Apps** (region: `southeastasia` by default)
- Get the public URL:
  ```bash
  az containerapp show -g $AZURE_RESOURCE_GROUP -n $AZURE_CONTAINERAPP_NAME     --query "properties.configuration.ingress.fqdn" -o tsv
  ```

### D. Post-Deploy Checklist
- **Health**: open `https://<FQDN>/healthz` → `{"ok":true}`
- **API**: `POST /chat` with JSON: `{"message":"hello"}`
- **Scaling**: Adjust `minReplicas/maxReplicas` and add autoscaling rules if needed.
- **Observability**: Consider enabling **Azure Monitor / Application Insights**.  
- **Network**: For private access, integrate with **VNet** and configure **NAT/Firewall** outbound rules.

### E. (Optional) Use Managed Identity for Azure OpenAI
1. Enable a **Managed Identity** on the Container App (User-assigned or System-assigned).
2. Grant it `Cognitive Services OpenAI User` on your Azure OpenAI resource.
3. In your Container App, **omit** `AZURE_OPENAI_API_KEY` and keep:
   ```
   AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT
   ```
   The SDK will use the MSI token under the hood (when configured).

---

## API
- `GET /healthz` → `{"ok": true}`
- `POST /chat` → `{"reply": "<model output>"}`
  ```bash
  curl -s -X POST https://<FQDN>/chat     -H "content-type: application/json"     -d '{"message":"hi"}'
  ```

## Notes
- Image registry is **GHCR**; you can switch to **ACR** if preferred.
- Default region is `southeastasia` (Singapore); change in workflow as needed.
- For production, set `minReplicas > 0`, add probes, and consider private networking.

---

## License
Choose the license you prefer for your repo (e.g., MIT/Apache-2.0). This template does not include a license by default.
