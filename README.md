# Final Project DEVOPS

## Overview

This repository contains the complete DevOps final assignment implementation.

**Source Application:** https://github.com/lidorg-dev/final-python

---

## PART A: Docker Implementation ✅

**Objective:** Dockerize a Python Flask REST API application

**Solution:** Option 1 - Dockerfile

### Deliverables

1. **Dockerfile** - Production-ready Docker configuration
2. **PART_A_DOCUMENTATION.md** - Complete implementation guide

### Implementation Details

- **Base Image:** python:3.9-slim
- **Entry Point:** app.py
- **Framework:** Flask REST API with Flask-RESTPlus
- **Database:** SQLite
- **Port:** 5000

### Quick Start (PART A)

```bash
# Clone the source repository
git clone https://github.com/lidorg-dev/final-python.git
cd final-python

# Copy the Dockerfile from this repo to the source repo
# Then build and run:

docker build -t final-python-app .
docker run -d -p 5000:5000 --name final-python-container final-python-app
```

**Access:** http://localhost:5000/api/doc

---

## PART B: CI/CD Pipeline with GitHub Actions ✅

**Objective:** Automate Docker image build and push to DockerHub using GitHub Actions

### Deliverables

1. **`.github/workflows/docker-build-push.yml`** - GitHub Actions workflow
2. **PART_B_DOCUMENTATION.md** - Complete CI/CD setup guide

### Workflow Features

- **Trigger:** Automatic on push to `main` branch
- **Actions Used:**
  - `actions/checkout@v4` - Checkout repository
  - `docker/login-action@v3` - Login to DockerHub
  - `docker/build-push-action@v5` - Build and push image
- **Security:** Uses GitHub Secrets for DockerHub credentials
- **Image Tag:** `<DOCKERHUB_USERNAME>/final-python-app:latest`

### Required GitHub Secrets

Add these secrets in your GitHub repository settings:

1. `DOCKERHUB_USERNAME` - Your DockerHub username
2. `DOCKERHUB_TOKEN` - Your DockerHub access token

**See PART_B_DOCUMENTATION.md for detailed setup instructions.**

### Pull from DockerHub

Once the workflow runs successfully:

```bash
docker pull <your-dockerhub-username>/final-python-app:latest
docker run -d -p 5000:5000 <your-dockerhub-username>/final-python-app:latest
```

---

## Repository Structure

```
final-project-DEVOPS/
├── .github/
│   └── workflows/
│       └── docker-build-push.yml    # PART B: CI/CD Workflow
├── Dockerfile                        # PART A: Docker config
├── PART_A_DOCUMENTATION.md          # PART A: Full guide
├── PART_B_DOCUMENTATION.md          # PART B: Full guide
└── README.md                         # This file
```

---

## Documentation

- **[PART_A_DOCUMENTATION.md](PART_A_DOCUMENTATION.md)** - Docker implementation with commands, testing, and troubleshooting
- **[PART_B_DOCUMENTATION.md](PART_B_DOCUMENTATION.md)** - GitHub Actions workflow setup, secrets configuration, and validation

---

## Validation Status

## Validation Status

### PART A
✅ Docker build successful  
✅ Container running on port 5000  
✅ API responding (HTTP 200)  
✅ Swagger UI accessible  

### PART B
✅ GitHub Actions workflow created  
✅ Workflow file in `.github/workflows/`  
✅ Uses official Docker actions  
✅ Secrets-based authentication  
✅ Auto-trigger on push to main  

---

## Next Steps

1. **Add GitHub Secrets** (for PART B):
   - Go to repository Settings → Secrets and variables → Actions
   - Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`

2. **Trigger Workflow**:
   ```bash
   git add .
   git commit -m "Add PART B: GitHub Actions CI/CD workflow"
   git push origin main
   ```

3. **Monitor Workflow**:
   - Check GitHub Actions tab for workflow execution
   - Verify image appears in DockerHub

---

## Contact & Submission

**Repository:** https://github.com/gazal1994/final-project-DEVOPS  
**Student:** Gazal  
**Assignment:** DevOps Final Project - Parts A & B
