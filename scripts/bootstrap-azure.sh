#!/usr/bin/env bash
set -euo pipefail
AZ_SUB="6376398c-bc02-4da5-a8c1-fc3e76b57990"
AZ_RG="rg-ai"
AZ_LOC="southeastasia"
AZ_ENV="cae-agent"
az account show >/dev/null 2>&1 || az login
az account set --subscription "$AZ_SUB"
az group create -n "$AZ_RG" -l "$AZ_LOC"
az containerapp env create -g "$AZ_RG" -n "$AZ_ENV" -l "$AZ_LOC" || true
echo "Bootstrap done."
