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
