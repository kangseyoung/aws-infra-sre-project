#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Updating package index"
sudo apt-get update -y

echo "[INFO] Installing Docker"
sudo apt-get install -y docker.io

echo "[INFO] Enabling Docker service"
sudo systemctl enable docker
sudo systemctl start docker

echo "[INFO] Adding current user to docker group"
sudo usermod -aG docker "$USER" || true

echo "[INFO] Docker installation completed"
docker --version || true

