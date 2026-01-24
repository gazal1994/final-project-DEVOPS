# PART B: GitHub Actions CI/CD Pipeline

## Overview
This workflow automatically builds and pushes the Docker image to DockerHub whenever code is pushed to the `main` branch.

---

## Files Created

**Workflow File:** `.github/workflows/docker-build-push.yml`

---

## GitHub Actions Workflow Explanation

### Workflow Structure

```yaml
name: Build and Push Docker Image to DockerHub

on:
  push:
    branches:
      - main
```
- **Trigger:** Runs automatically on every push to the `main` branch

### Job: build-and-push

**Step 1: Checkout Repository**
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```
- Checks out your repository code so the workflow can access the Dockerfile and source code

**Step 2: Login to DockerHub**
```yaml
- name: Login to DockerHub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```
- Authenticates to DockerHub using encrypted secrets
- Uses official Docker login action for secure authentication

**Step 3: Build and Push Docker Image**
```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    file: ./Dockerfile
    push: true
    tags: ${{ secrets.DOCKERHUB_USERNAME }}/final-python-app:latest
```
- Builds the Docker image from the Dockerfile in repository root
- Pushes the image to DockerHub
- Tags the image as `latest`

---

## Setting Up GitHub Secrets

### Step-by-Step Instructions

1. **Navigate to Repository Settings**
   - Go to: https://github.com/gazal1994/final-project-DEVOPS
   - Click **"Settings"** tab

2. **Access Secrets Section**
   - In left sidebar, click **"Secrets and variables"**
   - Click **"Actions"**

3. **Add DOCKERHUB_USERNAME Secret**
   - Click **"New repository secret"**
   - **Name:** `DOCKERHUB_USERNAME`
   - **Value:** Your DockerHub username (e.g., `gazal1994`)
   - Click **"Add secret"**

4. **Add DOCKERHUB_TOKEN Secret**
   - Click **"New repository secret"** again
   - **Name:** `DOCKERHUB_TOKEN`
   - **Value:** Your DockerHub access token
   - Click **"Add secret"**

### How to Get DockerHub Access Token

1. Go to: https://hub.docker.com/settings/security
2. Click **"New Access Token"**
3. **Description:** `GitHub Actions CI/CD`
4. **Access permissions:** `Read, Write, Delete`
5. Click **"Generate"**
6. **Copy the token** (you won't see it again!)
7. Use this token as the value for `DOCKERHUB_TOKEN` secret

---

## How to Trigger the Workflow

### Automatic Trigger
The workflow runs automatically whenever you push to the `main` branch:

```bash
cd "C:\Users\windows11\Desktop\Final Project DEVOPS\final-project-DEVOPS"
git add .
git commit -m "Add GitHub Actions workflow for Docker build and push"
git push origin main
```

### Manual Trigger (Optional Enhancement)
To enable manual workflow runs, you can add `workflow_dispatch` to the workflow:

```yaml
on:
  push:
    branches:
      - main
  workflow_dispatch:  # Add this line
```

Then trigger manually via:
- GitHub UI → Actions tab → Select workflow → "Run workflow"

---

## Expected Workflow Execution

### 1. Workflow Triggers
- A new commit is pushed to `main` branch
- GitHub Actions starts the workflow automatically

### 2. Workflow Steps Execute
```
✓ Checkout repository
✓ Login to DockerHub
✓ Build and push Docker image
```

### 3. Success Indicators
- Green checkmark ✓ in GitHub Actions tab
- Image appears in DockerHub at: `https://hub.docker.com/r/<your-username>/final-python-app`
- Image tagged as `latest`

---

## DockerHub Image Details

### Image Name Format
```
<DOCKERHUB_USERNAME>/final-python-app:latest
```

**Example:**
If your DockerHub username is `gazal1994`, the image will be:
```
gazal1994/final-python-app:latest
```

### Pulling the Image
Anyone can pull your image from DockerHub using:
```bash
docker pull <your-dockerhub-username>/final-python-app:latest
docker run -d -p 5000:5000 <your-dockerhub-username>/final-python-app:latest
```

---

## Monitoring Workflow Execution

### View Workflow Runs
1. Go to your repository: https://github.com/gazal1994/final-project-DEVOPS
2. Click **"Actions"** tab
3. View all workflow runs with status (success/failure)
4. Click on any run to see detailed logs for each step

### Troubleshooting Failed Workflows

**Common Issues:**

1. **Invalid DockerHub Credentials**
   - Error: `unauthorized: incorrect username or password`
   - Solution: Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets are correct

2. **Dockerfile Not Found**
   - Error: `unable to prepare context: unable to evaluate symlinks in Dockerfile path`
   - Solution: Ensure Dockerfile exists in repository root

3. **Permission Denied**
   - Error: `denied: requested access to the resource is denied`
   - Solution: Ensure DockerHub token has `Read, Write, Delete` permissions

---

## Validation Checklist

### Pre-Push Validation
- [ ] `.github/workflows/docker-build-push.yml` file created
- [ ] Dockerfile exists in repository root
- [ ] GitHub Secrets added:
  - [ ] `DOCKERHUB_USERNAME`
  - [ ] `DOCKERHUB_TOKEN`

### Post-Push Validation
- [ ] Workflow appears in GitHub Actions tab
- [ ] All workflow steps complete successfully (green checkmarks)
- [ ] DockerHub repository shows new image
- [ ] Image tagged as `latest`
- [ ] Can pull and run image from DockerHub

---

## Security Best Practices

✅ **Never commit credentials** - All sensitive data uses GitHub Secrets  
✅ **Use access tokens** - DockerHub token instead of password  
✅ **Minimal permissions** - Token has only required permissions  
✅ **Secrets encryption** - GitHub encrypts all secrets at rest  

---

## Workflow File Location

```
final-project-DEVOPS/
├── .github/
│   └── workflows/
│       └── docker-build-push.yml  ← Workflow file
├── Dockerfile
├── PART_A_DOCUMENTATION.md
├── PART_B_DOCUMENTATION.md
└── README.md
```

---

## Summary

✅ **Workflow created:** `.github/workflows/docker-build-push.yml`  
✅ **Trigger:** Push to `main` branch  
✅ **Actions used:**
   - `actions/checkout@v4`
   - `docker/login-action@v3`
   - `docker/build-push-action@v5`  
✅ **Secrets required:**
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`  
✅ **Image name:** `<DOCKERHUB_USERNAME>/final-python-app:latest`  
✅ **Dockerfile:** Repository root  

**Status:** Ready for CI/CD automation! 🚀
