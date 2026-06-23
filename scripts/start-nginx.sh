#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="aws-infra-2week-nginx"
CONTAINER_NAME="aws-infra-2week-nginx"

echo "[INFO] Building Nginx image"
docker build -t "$IMAGE_NAME" ./app

echo "[INFO] Removing old container if it exists"
docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

echo "[INFO] Starting container"
docker run -d \
  --name "$CONTAINER_NAME" \
  -p 80:80 \
  --restart unless-stopped \
  "$IMAGE_NAME"

echo "[INFO] Running containers"
docker ps

