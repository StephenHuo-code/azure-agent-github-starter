#!/usr/bin/env bash
set -euo pipefail
AZ_RG="rg-ai"
AZ_ENV="cae-agent"
APP_NAME="agent"
IMAGE="ghcr.io/StephenHuo-code/azure-agent-github-starter:latest"
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
set +e
az containerapp create -g "$AZ_RG" -n "$APP_NAME"   --environment "$AZ_ENV"   --image "$IMAGE"   --target-port 8000   --ingress external   --env-vars     OPENAI_API_KEY="$OPENAI_API_KEY"     OPENAI_MODEL="gpt-4o-mini"     MODEL_TEMPERATURE="0.2"
ret=$?
set -e
if [ $ret -ne 0 ]; then
  az containerapp update -g "$AZ_RG" -n "$APP_NAME" --image "$IMAGE"
fi
az containerapp show -g "$AZ_RG" -n "$APP_NAME" --query "properties.configuration.ingress.fqdn" -o tsv
