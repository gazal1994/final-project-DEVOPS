# PART C - Quick Reference

## ✅ Azure VM Deployment with GitHub Actions

### 📁 Workflow File
```
.github/workflows/deploy-to-azure-vm.yml
```

---

## 🔐 Required GitHub Secrets

### From PART B (Already Configured):
- ✅ `DOCKERHUB_USERNAME`
- ✅ `DOCKERHUB_TOKEN`

### New for PART C:
- `AZURE_VM_HOST` - VM public IP (e.g., `20.123.45.67`)
- `AZURE_VM_USER` - SSH username (e.g., `azureuser`)
- `AZURE_VM_SSH_KEY` - Complete private SSH key

---

## 🖥️ Azure VM Setup

### 1. Install Docker on VM
```bash
# SSH into VM
ssh azureuser@<VM_IP>

# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER

# Log out and back in
exit
ssh azureuser@<VM_IP>

# Verify
docker --version
```

### 2. Configure NSG (Network Security Group)
**Required Inbound Rules:**
- Port 22 (SSH)
- Port 80 (HTTP - Application)

---

## 🚀 Deployment Flow

```
Push to main → GitHub Actions → SSH to VM → Pull Image → Run Container
```

### Workflow Steps:
1. ✅ Checkout code
2. ✅ SSH into Azure VM
3. ✅ Login to DockerHub
4. ✅ Pull latest image
5. ✅ Stop old container
6. ✅ Run new container on port 80
7. ✅ Verify deployment

---

## 🌐 Access Application

### URL Format:
```
http://<AZURE_VM_PUBLIC_IP>/api/doc
```

**Example:**
```
http://20.123.45.67/api/doc
```

### Test Endpoints:
```
http://<VM_IP>/api/stores
http://<VM_IP>/api/items
```

---

## 📋 Deployment Checklist

### Azure Setup:
- [ ] VM created (Ubuntu 20.04+)
- [ ] Docker installed on VM
- [ ] NSG allows port 22 and 80
- [ ] Have SSH private key

### GitHub Setup:
- [ ] Add `AZURE_VM_HOST` secret
- [ ] Add `AZURE_VM_USER` secret
- [ ] Add `AZURE_VM_SSH_KEY` secret

### Deploy:
- [ ] Push workflow file to GitHub
- [ ] Workflow runs successfully
- [ ] Access app via `http://<VM_IP>/api/doc`

---

## 🔧 Port Mapping

**Container Port:** 5000 (Flask app)  
**VM Port:** 80 (Public HTTP)  
**Mapping:** `-p 80:5000`

Access without port number: `http://<VM_IP>/`

---

## 📖 Full Documentation

See **PART_C_DOCUMENTATION.md** for:
- Complete Azure VM setup guide
- Docker installation steps
- NSG configuration details
- Troubleshooting guide
- Security best practices
