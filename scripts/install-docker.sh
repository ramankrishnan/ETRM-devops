#!/bin/bash
# Update package lists
sudo apt update -y

# Install Docker
sudo apt install -y docker.io

# Enable and start Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Install Docker Compose
sudo apt install -y docker-compose

# Add current user to docker group
sudo usermod -aG docker $USER
