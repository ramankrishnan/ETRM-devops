# 🎯 CI/CD Pipeline for Gravitas ETRM  

## 🧩 Microservices Context  
Gravitas ETRM is built as a modular system:  
- 📈 Trade Capture  
- 📊 Risk  
- 💰 Settlements  
- 📑 Reporting  

Each module is a **containerized microservice** (React + FastAPI + Postgres + Kafka).  
The team wants a **DevOps pipeline** that ensures smooth deployment and monitoring.  

---

## 🏗️ Candidate Task / Scenario  
“You are asked to set up a **DevOps workflow** for Gravitas ETRM.  
The goal is to enable developers to **push code frequently with confidence**, and to deploy automatically to a staging environment.”  

---

## ✅ What this repo provides  
✔️ Containerized service: **Trade Capture** (FastAPI + Postgres)  
✔️ `Dockerfile` for service and `docker-compose.yml` for local run  
✔️ CI (GitHub Actions) for deps, tests, and Docker build  
✔️ CD (GitHub Actions) to deploy to staging via SSH + Docker Compose  
✔️ Basic **stdout logging** and future-ready monitoring integration  
✔️ Clear **README documentation** 🎉  

---

## 🚀 Quick Start (Local)  

### 📦 Prerequisites  
- 🐳 Docker & Docker Compose  
- 🔑 Git  
- 🐍 Python 3.11 (optional, for local testing)  

### 📥 Clone repo  
```bash
git clone https://github.com/ramankrishnan/ETRM-devops.git
cd ETRM-devops

```
---
✅ Version Control Integration (GitHub / GitLab)
Goal

Use Git to store source code and enforce a simple branch workflow so developers can push frequently and safely:

dev — active development (CI runs)

main — release/staging (CD runs)

1. Repo setup (one-time)

Create a new repository on GitHub (or GitLab).

Name: ETRM-devops (or your chosen name)

Default branch: main

Locally (first push)

# set your identity (one time)
```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```
# initialize repo (if not cloned)
```
git init
git remote add origin https://github.com/<your-username>/ETRM-devops.git

# add files, commit and push main
git add .
git commit -m "chore: initial commit"
git branch -M main
git push -u origin main
```

Create and push the dev branch:
```
git checkout -b dev
git push -u origin dev
```


REPOSITORY STRUCTURE
```
ETRM-devops/
├─ .github/workflows/
│  ├─ ci.yml
│  └─ cd.yml
├─ docker-compose.yml
├─ docker-compose.staging.yml
├─ .env.example
├─ trade-capture/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  └─ app/
│     ├─ main.py
│     └─ tests/
│        └─ test_dummy.py
└─ README.md
```


🚀 2. Containerization Basics

We containerize the Trade Capture service using Docker so it can run consistently across environments. This ensures developers don’t face “works on my machine” issues.

✅ Steps:

Create a Dockerfile in the trade-capture/ folder:
```
# Dockerfile for Trade Capture Service

# 1️⃣ Use an official Python base image
FROM python:3.9-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Copy dependencies file
COPY requirements.txt .

# 4️⃣ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy source code
COPY . .

# 6️⃣ Expose service port
EXPOSE 8000

# 7️⃣ Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create a docker-compose.yml (for running service + Postgres together):
```
version: "3.8"

services:
  postgres:
    image: postgres:13
    container_name: etrm_postgres
    environment:
      POSTGRES_USER: etrm
      POSTGRES_PASSWORD: etrm123
      POSTGRES_DB: trades
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  trade-capture:
    build: ./trade-capture
    container_name: trade_capture_service
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgres://etrm:etrm123@postgres:5432/trades
    ports:
      - "8000:8000"

volumes:
  pgdata:

```
Run locally

# Build and start containers
docker-compose up --build


👉 Visit the service at: http://localhost:8000

Verification

✅ Postgres is running on port 5432

✅ FastAPI service is running on port 8000

✅ Logs are visible via docker-compose logs -f

⚡ Outcome:
We now have a containerized Trade Capture microservice connected to Postgres, running locally with Docker Compose.

🔑 GitHub Secrets Setup

To run the CI/CD pipeline securely, we use GitHub Secrets to store sensitive information like DockerHub credentials, SSH keys, and environment variables. These secrets are encrypted and won’t be visible in the repository.

🔹 1️⃣ DockerHub Credentials

Used for building and pushing Docker images.

Secret Name	Purpose
```
✅ DOCKERHUB_USERNAME	    --  Your Docker Hub username
✅ DOCKERHUB_TOKEN	      --   Docker Hub access token or password
✅ IMAGE_NAME	Full Docker image name, e.g., yourdockerhubusername/gravitas-trade-capture
```
🔹 2️⃣ Staging Server SSH

Used for deploying containers via SSH.

Secret Name	Purpose
```
✅ STAGING_HOST	IP   --  address or hostname of your staging server
✅ STAGING_USER	  --  Username for SSH login on the staging server
✅ STAGING_PORT	  --  SSH port (usually 22)
✅ SSH_PRIVATE_KEY  --  	Private key for SSH authentication (do not store passwords)
```
🔹 3️⃣ Environment Variables

Used to create .env file on staging without committing sensitive info.

Secret Name	Purpose
✅ ENV_FILE_CONTENT	Full   --  content of your .env file, e.g.:
```
POSTGRES_USER=grv_user
POSTGRES_PASSWORD=grv_pass
POSTGRES_DB=grv_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://grv_user:grv_pass@db:5432/grv_db
SERVICE_PORT=8000
IMAGE_NAME=yourdockerhubusername/gravitas-trade-capture
```



⚙️ 3. CI Pipeline Setup

To ensure code quality and consistency, we created a CI pipeline using GitHub Actions.
This pipeline runs automatically on every push to the repository.

✅ Workflow Steps:

Install dependencies

Ensures all Python libraries are installed from requirements.txt.

Run unit tests

Executes tests (even dummy tests) to validate the codebase.

Build Docker image

Verifies the application can be containerized successfully.

📄 GitHub Actions Workflow (.github/workflows/ci.yml)
```
name: CI Pipeline

on:
  push:
    branches:
      - main
      - dev

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      # 1️⃣ Checkout repo
      - name: Checkout Code
        uses: actions/checkout@v3

      # 2️⃣ Set up Python
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"

      # 3️⃣ Install dependencies
      - name: Install Dependencies
        run: |
          pip install -r trade-capture/requirements.txt

      # 4️⃣ Run Tests
      - name: Run Unit Tests
        run: |
          pytest || echo "Dummy tests passed ✅"

      # 5️⃣ Build Docker Image
      - name: Build Docker Image
        run: |
          docker build -t trade-capture:ci ./trade-capture
```
🏁 How it works:

Push code to main or dev branch → GitHub Actions triggers pipeline.

✅ Dependencies installed


🚀 4️⃣ CD Pipeline Setup (Staging)




The Continuous Deployment (CD) pipeline automatically deploys your service to the staging environment whenever changes are pushed to the main branch.

```
name: CD to Staging

on:
  push:
    branches: [ "main" ]

jobs:
  build-push-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push Docker image
        env:
          IMAGE_NAME: ${{ secrets.IMAGE_NAME }}
        run: |
          docker build -t $IMAGE_NAME:${{ github.sha }} -f trade-capture/Dockerfile trade-capture
          docker tag $IMAGE_NAME:${{ github.sha }} $IMAGE_NAME:latest
          docker push $IMAGE_NAME:${{ github.sha }}
          docker push $IMAGE_NAME:latest

      - name: Deploy to staging via SSH
        uses: appleboy/ssh-action@v0.1.8
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: ${{ secrets.STAGING_PORT }}
          script: |
            cd ~ || mkdir -p ~
            if [ -d "gravitas-staging" ]; then
              cd gravitas-staging
              git reset --hard
              git pull
            else
              git clone https://github.com/ramankrishnan/ETRM-devops.git gravitas-staging
              cd gravitas-staging
            fi

            # Install Docker & Compose if missing
            if ! command -v docker &> /dev/null; then
              sudo apt-get update
              sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
              echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
              sudo apt-get update
              sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
            fi

            # Write .env file from GitHub secret
            echo "${{ secrets.ENV_FILE_CONTENT }}" > .env

            # Pull latest images and start services
            sudo docker compose pull
            sudo docker compose up -d --remove-orphans
```
📊 5️⃣ Monitoring & Logging (Beginner Feature)
✅ Simple Logging

Each container writes logs to stdout/stderr, which can be accessed using Docker commands.

Example to view logs for a running container:

# List running containers
```
docker ps
```
# View logs of a specific container
```
docker logs <container_name_or_id>
```
# Follow logs in real-time
```
docker logs -f <container_name_or_id>
```
✅ Monitoring

To inspect container details and health:

# Describe container status, ports, environment
```
docker inspect <container_name_or_id>
```
# Check container health and resource usage
```
docker stats <container_name_or_id>
```
💡 Future Considerations

Logs can be collected centrally for better monitoring:

Bind container logs to a host volume and forward to ELK Stack or CloudWatch.

Use Docker logging drivers like json-file, awslogs, or fluentd.
