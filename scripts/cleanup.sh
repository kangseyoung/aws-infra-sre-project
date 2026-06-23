#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="aws-infra-2week-nginx"
IMAGE_NAME="aws-infra-2week-nginx"

echo "[INFO] Stopping and removing container if present"
docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

echo "[INFO] Removing image if present"
docker rmi "$IMAGE_NAME" >/dev/null 2>&1 || true

echo "[INFO] Cleanup finished"

