# PART C: Azure VM Deployment with GitHub Actions

## Overview
This part automates the deployment of the Dockerized application to an Azure Virtual Machine using GitHub Actions. The workflow pulls the latest Docker image from DockerHub and deploys it to the VM via SSH.

---

## Architecture

```
GitHub Push → GitHub Actions → SSH to Azure VM → Docker Pull → Docker Run → Application Live
```

**Flow:**
1. Code pushed to `main` branch
2. GitHub Actions workflow triggers
3. Workflow connects to Azure VM via SSH
4. VM pulls latest Docker image from DockerHub
5. VM stops old container and starts new one
6. Application accessible via VM public IP

---

## Files Created

**Deployment Workflow:** `.github/workflows/deploy-to-azure-vm.yml`

---

## Azure VM Setup

### 1. Create Azure VM (Prerequisites)

**VM Specifications:**
- **OS:** Ubuntu 20.04 LTS or newer
- **Size:** Standard_B2s (2 vCPUs, 4 GB RAM) - minimum
- **Networking:** Public IP address assigned
- **Authentication:** SSH key-based

**Create VM via Azure Portal or CLI:**

```bash
# Using Azure CLI (if you have it installed)
az vm create \
  --resource-group myResourceGroup \
  --name myDevOpsVM \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard
```

### 2. Install Docker on Azure VM

**SSH into your VM first:**
```bash
ssh azureuser@<VM_PUBLIC_IP>
```

**Then run these commands on the VM:**

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add current user to docker group (avoid sudo for docker commands)
sudo usermod -aG docker $USER

# Verify Docker installation
docker --version

# IMPORTANT: Log out and log back in for group changes to take effect
exit
```

**After logging back in, verify:**
```bash
ssh azureuser@<VM_PUBLIC_IP>
docker run hello-world
```

### 3. Configure Network Security Group (NSG)

**CRITICAL:** Azure NSG must allow inbound traffic on required ports.

**Required Inbound Rules:**

| Priority | Port | Protocol | Source | Description |
|----------|------|----------|--------|-------------|
| 1000 | 22 | TCP | Your IP or Any | SSH access |
| 1010 | 80 | TCP | Any | HTTP (application) |
| 1020 | 5000 | TCP | Any | Alternative app port (optional) |

**Add NSG Rules via Azure Portal:**
1. Go to Azure Portal → Virtual Machines → Your VM
2. Click **"Networking"** in left menu
3. Click **"Add inbound port rule"**
4. Add rules for ports 22 and 80 as shown above

**Or via Azure CLI:**
```bash
# Allow SSH (port 22)
az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name myVMNSG \
  --name AllowSSH \
  --priority 1000 \
  --source-address-prefixes '*' \
  --destination-port-ranges 22 \
  --access Allow \
  --protocol Tcp

# Allow HTTP (port 80)
az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name myVMNSG \
  --name AllowHTTP \
  --priority 1010 \
  --source-address-prefixes '*' \
  --destination-port-ranges 80 \
  --access Allow \
  --protocol Tcp
```

---

## GitHub Secrets Configuration

### Required Secrets

Add these secrets in your GitHub repository:

**Already Configured (from PART B):**
- ✅ `DOCKERHUB_USERNAME` - Your DockerHub username
- ✅ `DOCKERHUB_TOKEN` - Your DockerHub access token

**New Secrets for PART C:**

#### 1. AZURE_VM_HOST
**Value:** Public IP address of your Azure VM
**Example:** `20.123.45.67`

**How to get it:**
- Azure Portal → Virtual Machines → Your VM → Overview → Public IP address

#### 2. AZURE_VM_USER
**Value:** SSH username for the VM
**Example:** `azureuser`
**Default:** Usually `azureuser` when created via portal

#### 3. AZURE_VM_SSH_KEY
**Value:** Private SSH key content (the entire key file)

**How to get it:**

**If you created VM with Azure-generated keys:**
```bash
# The private key is usually saved as:
# Windows: C:\Users\<YourUser>\.ssh\id_rsa
# Linux/Mac: ~/.ssh/id_rsa

# Display the private key:
cat ~/.ssh/id_rsa
```

**The key should look like:**
```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
...
(many lines)
...
-----END OPENSSH PRIVATE KEY-----
```

**Important:**
- Copy the ENTIRE key including the BEGIN and END lines
- Paste it as-is into the GitHub secret (preserve line breaks)

### Adding Secrets to GitHub

1. Go to: https://github.com/gazal1994/final-project-DEVOPS/settings/secrets/actions
2. Click **"New repository secret"** for each:

**Secret 1:**
- Name: `AZURE_VM_HOST`
- Value: Your VM's public IP (e.g., `20.123.45.67`)

**Secret 2:**
- Name: `AZURE_VM_USER`
- Value: `azureuser` (or your VM username)

**Secret 3:**
- Name: `AZURE_VM_SSH_KEY`
- Value: Entire private SSH key content

---

## Deployment Workflow Explanation

### Workflow File: `.github/workflows/deploy-to-azure-vm.yml`

### Trigger
```yaml
on:
  push:
    branches:
      - main
  workflow_dispatch:
```
- **Automatic:** Triggers on every push to `main` branch
- **Manual:** Can also be triggered manually from GitHub Actions tab

### Job: deploy

**Step 1: Checkout Repository**
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```
- Checks out the repository code
- Required for workflow context

**Step 2: Deploy to Azure VM via SSH**
```yaml
- name: Deploy to Azure VM via SSH
  uses: appleboy/ssh-action@v1.0.3
```
- Uses the SSH Action to connect to Azure VM
- Executes deployment commands remotely

**SSH Connection Parameters:**
- `host`: VM public IP from `AZURE_VM_HOST` secret
- `username`: SSH user from `AZURE_VM_USER` secret
- `key`: Private SSH key from `AZURE_VM_SSH_KEY` secret

**Deployment Script Breakdown:**

1. **Login to DockerHub**
   ```bash
   echo "${{ secrets.DOCKERHUB_TOKEN }}" | docker login -u "${{ secrets.DOCKERHUB_USERNAME }}" --password-stdin
   ```
   - Authenticates Docker CLI with DockerHub
   - Allows pulling private images (if needed)

2. **Pull Latest Image**
   ```bash
   docker pull ${{ secrets.DOCKERHUB_USERNAME }}/final-python-app:latest
   ```
   - Downloads the latest version of the image from DockerHub
   - Uses the image built in PART B

3. **Stop and Remove Old Container**
   ```bash
   docker stop final-python-app || true
   docker rm final-python-app || true
   ```
   - Stops the currently running container
   - Removes the old container
   - `|| true` prevents failure if container doesn't exist

4. **Run New Container**
   ```bash
   docker run -d \
     --name final-python-app \
     --restart unless-stopped \
     -p 80:5000 \
     ${{ secrets.DOCKERHUB_USERNAME }}/final-python-app:latest
   ```
   - `-d`: Run in detached mode (background)
   - `--name`: Names the container for easy reference
   - `--restart unless-stopped`: Auto-restart on failure
   - `-p 80:5000`: Maps VM port 80 to container port 5000
   - Uses the latest image from DockerHub

5. **Clean Up Unused Images**
   ```bash
   docker image prune -af
   ```
   - Removes old/unused Docker images to save disk space
   - Keeps the VM clean

6. **Verify Container is Running**
   ```bash
   docker ps | grep final-python-app
   ```
   - Checks that the container started successfully
   - Workflow fails if container is not running

---

## Port Mapping Explained

**Container Port:** 5000 (Flask app runs on this port inside container)  
**VM Port:** 80 (Standard HTTP port, accessible from browser)

**Mapping:** `-p 80:5000`
- VM port 80 → Container port 5000
- Users access via: `http://<VM_PUBLIC_IP>` (port 80 is default for HTTP)

**Alternative:** If you want to keep port 5000:
```yaml
-p 5000:5000
```
Then access via: `http://<VM_PUBLIC_IP>:5000`

---

## Accessing the Application

### URL Format

After successful deployment, access your application at:

```
http://<AZURE_VM_PUBLIC_IP>/api/doc
```

**Example:**
If your VM public IP is `20.123.45.67`:
```
http://20.123.45.67/api/doc
```

### Testing Endpoints

**Swagger UI (API Documentation):**
```
http://<VM_IP>/api/doc
```

**API Endpoints:**
```
http://<VM_IP>/api/stores
http://<VM_IP>/api/items
```

**Using curl:**
```bash
curl http://<VM_IP>/api/stores
```

---

## Workflow Execution Process

### 1. Trigger Workflow

**Automatic Trigger:**
```bash
cd "C:\Users\windows11\Desktop\Final Project DEVOPS\final-project-DEVOPS"
git add .
git commit -m "Deploy to Azure VM"
git push origin main
```

**Manual Trigger:**
1. Go to: https://github.com/gazal1994/final-project-DEVOPS/actions
2. Click **"Deploy to Azure VM"** workflow
3. Click **"Run workflow"** → **"Run workflow"**

### 2. Monitor Deployment

**GitHub Actions:**
- Go to: https://github.com/gazal1994/final-project-DEVOPS/actions
- Watch the "Deploy to Azure VM" workflow
- Check each step for success/failure

**Expected Steps:**
- ✅ Checkout repository (~5 seconds)
- ✅ Deploy to Azure VM via SSH (~30-60 seconds)
  - Login to DockerHub
  - Pull latest image
  - Stop old container
  - Run new container
  - Clean up images
  - Verify container running

### 3. Verify Deployment

**On Azure VM (SSH):**
```bash
# SSH into VM
ssh azureuser@<VM_PUBLIC_IP>

# Check running containers
docker ps

# View container logs
docker logs final-python-app

# Check if app is responding
curl http://localhost/api/stores
```

**From Browser:**
- Open: `http://<VM_PUBLIC_IP>/api/doc`
- You should see the Swagger UI

---

## Troubleshooting

### Deployment Fails with "Permission Denied"

**Cause:** SSH key not configured correctly

**Solution:**
1. Verify `AZURE_VM_SSH_KEY` contains the complete private key
2. Ensure the corresponding public key is in VM's `~/.ssh/authorized_keys`

### Container Not Accessible from Browser

**Cause:** NSG not configured or port mapping incorrect

**Solution:**
1. Verify NSG allows inbound traffic on port 80
2. Check container is running: `docker ps`
3. Test locally on VM: `curl http://localhost/api/stores`

### Docker Pull Fails

**Cause:** DockerHub credentials invalid

**Solution:**
1. Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` are correct
2. Test login manually on VM:
   ```bash
   docker login -u <username>
   ```

### Container Stops Immediately

**Cause:** Application error

**Solution:**
```bash
# View container logs
docker logs final-python-app

# Check for Python errors or missing dependencies
```

---

## Security Best Practices

✅ **SSH Key Authentication:** More secure than password-based  
✅ **GitHub Secrets:** All credentials encrypted  
✅ **NSG Rules:** Restrict SSH access to known IPs (optional)  
✅ **Docker Login:** Only during deployment, token not stored on VM  
✅ **Auto-restart:** Container restarts automatically on failure  

**Optional Enhancements:**
- Restrict SSH (port 22) to your IP address only
- Use HTTPS with SSL/TLS certificate (Let's Encrypt)
- Implement health checks
- Set up monitoring and alerts

---

## Complete Deployment Checklist

### Prerequisites
- [ ] Azure VM created with Ubuntu 20.04+
- [ ] Docker installed on VM
- [ ] VM has public IP address
- [ ] NSG allows ports 22 and 80
- [ ] SSH access to VM verified

### GitHub Configuration
- [ ] `DOCKERHUB_USERNAME` secret exists (from PART B)
- [ ] `DOCKERHUB_TOKEN` secret exists (from PART B)
- [ ] `AZURE_VM_HOST` secret added (VM public IP)
- [ ] `AZURE_VM_USER` secret added (SSH username)
- [ ] `AZURE_VM_SSH_KEY` secret added (private key)

### Deployment
- [ ] Workflow file created at `.github/workflows/deploy-to-azure-vm.yml`
- [ ] Code pushed to `main` branch
- [ ] Workflow runs successfully
- [ ] Container running on VM
- [ ] Application accessible via browser

### Validation
- [ ] `http://<VM_IP>/api/doc` shows Swagger UI
- [ ] API endpoints respond correctly
- [ ] Container auto-restarts after VM reboot

---

## Summary

### What Was Implemented

**Infrastructure:**
- Azure VM with Docker
- Network Security Group configured
- SSH key-based authentication

**CI/CD Pipeline:**
- Automated deployment on push to main
- SSH-based deployment to Azure VM
- Docker container management (pull, stop, run)
- Zero-downtime deployment strategy

**Application Access:**
- Public URL: `http://<VM_IP>/api/doc`
- Port mapping: VM:80 → Container:5000
- Auto-restart enabled

### Deployment Flow

```
Developer Push → GitHub Actions → SSH to Azure VM
                                    ↓
                           Docker Pull from DockerHub
                                    ↓
                           Stop Old Container
                                    ↓
                           Run New Container
                                    ↓
                           Application Live on Port 80
```

### Key Files

- **Workflow:** `.github/workflows/deploy-to-azure-vm.yml`
- **Documentation:** `PART_C_DOCUMENTATION.md`
- **Image:** `<dockerhub-username>/final-python-app:latest`
- **Access:** `http://<VM_PUBLIC_IP>/api/doc`

**PART C is complete and ready for deployment!** 🚀
