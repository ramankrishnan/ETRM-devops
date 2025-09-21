#!/usr/bin/env bash
set -e

sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg lsb-release

curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER

mkdir -p ~/gravitas-staging
cd ~/gravitas-staging
# Place docker-compose.staging.yml and .env here
# docker compose pull
# docker compose up -d --remove-orphans
