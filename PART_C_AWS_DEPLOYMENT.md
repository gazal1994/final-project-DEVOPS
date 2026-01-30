# PART C: AWS EC2 Deployment - Complete Guide

## ✅ Deployment Status: SUCCESSFUL

**Platform:** Amazon Web Services (AWS) EC2  
**Instance Type:** t3.micro  
**OS:** Amazon Linux 2023  
**Region:** eu-north-1 (Stockholm)  
**Date Configured:** January 30, 2026

---

## 📦 What Was Deployed

### AWS EC2 Instance Details

- **Instance ID:** `i-04943a1f391046041`
- **Public IP:** `13.60.8.113`
- **Instance Type:** t3.micro (2 vCPU, 1 GB RAM)
- **Platform:** Linux/UNIX (Amazon Linux 2023)
- **Instance State:** Running
- **Docker Version:** 25.0.13

### Application Access

**Public URL:** http://13.60.8.113/api/doc

---

## 🚀 Deployment Workflow

### GitHub Actions Workflow Created

**File:** `.github/workflows/deploy-to-aws-ec2.yml`

**Features:**
- ✅ Triggers automatically on push to `main` branch
- ✅ Manual trigger option (`workflow_dispatch`)
- ✅ SSH-based deployment to AWS EC2
- ✅ DockerHub authentication
- ✅ Container lifecycle management (pull, stop, remove, run)
- ✅ Auto-restart configuration
- ✅ Image cleanup
- ✅ Deployment verification

---

## 🔐 GitHub Secrets Configuration

### Required Secrets

Add these secrets in your GitHub repository:  
https://github.com/gazal1994/final-project-DEVOPS/settings/secrets/actions

#### 1. AWS_EC2_HOST
- **Name:** `AWS_EC2_HOST`
- **Value:** `13.60.8.113`
- **Description:** Public IP address of AWS EC2 instance

#### 2. AWS_EC2_USER
- **Name:** `AWS_EC2_USER`
- **Value:** `ec2-user`
- **Description:** SSH username for Amazon Linux

#### 3. AWS_EC2_SSH_KEY
- **Name:** `AWS_EC2_SSH_KEY`
- **Value:** Contents of `KEY.pem` file
- **Description:** Private SSH key for EC2 access
- **Format:** 
  ```
  -----BEGIN RSA PRIVATE KEY-----
  [key content]
  -----END RSA PRIVATE KEY-----
  ```

#### 4. DOCKERHUB_USERNAME (Already configured)
- **Name:** `DOCKERHUB_USERNAME`
- **Value:** Your DockerHub username

#### 5. DOCKERHUB_TOKEN (Already configured)
- **Name:** `DOCKERHUB_TOKEN`
- **Value:** Your DockerHub access token

---

## 🔧 EC2 Instance Configuration

### Docker Installation

Docker was installed and configured on the EC2 instance:

```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add ec2-user to docker group
sudo usermod -aG docker ec2-user

# Verify installation
docker --version
# Output: Docker version 25.0.13, build 0bab007
```

### Security Group Configuration

**Required Inbound Rules:**

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| SSH | TCP | 22 | Your IP / 0.0.0.0/0 | SSH access |
| HTTP | TCP | 80 | 0.0.0.0/0 | Application access |
| Custom TCP | TCP | 5000 | 0.0.0.0/0 | Flask app (optional) |

**Verify in AWS Console:**
1. Go to EC2 → Instances
2. Select your instance
3. Click "Security" tab
4. Check "Security groups"
5. Ensure ports 22 and 80 are open

---

## 📋 Deployment Process

### Automated Deployment Flow

1. **Developer pushes code to GitHub**
   ```bash
   git push origin main
   ```

2. **GitHub Actions triggers workflow**
   - Workflow: `deploy-to-aws-ec2.yml`
   - Runner: ubuntu-latest

3. **SSH connection to EC2**
   - Uses SSH key from GitHub Secrets
   - Connects as `ec2-user`

4. **Docker operations on EC2**
   ```bash
   # Login to DockerHub
   docker login
   
   # Pull latest image
   docker pull gazal94/final-python-app:latest
   
   # Stop old container
   docker stop final-python-app
   
   # Remove old container
   docker rm final-python-app
   
   # Run new container
   docker run -d --name final-python-app \
     --restart unless-stopped \
     -p 80:5000 \
     gazal94/final-python-app:latest
   
   # Cleanup
   docker image prune -af
   ```

5. **Verification**
   - Check container is running
   - Application accessible at http://13.60.8.113/api/doc

---

## ✅ Testing the Deployment

### Manual Testing Steps

1. **Access the Application**
   ```
   http://13.60.8.113/api/doc
   ```
   Should display Swagger UI interface

2. **Test API Endpoints**
   - **GET /api/stores** - List all stores
   - **POST /api/stores** - Create a store
   - **GET /api/items** - List all items
   - **POST /api/items** - Create an item

3. **Verify Container Status**
   ```bash
   ssh -i KEY.pem ec2-user@13.60.8.113 'docker ps'
   ```
   Should show `final-python-app` container running

4. **Check Container Logs**
   ```bash
   ssh -i KEY.pem ec2-user@13.60.8.113 'docker logs final-python-app'
   ```

---

## 🔄 Continuous Deployment

### Triggering Deployments

**Automatic Trigger:**
```bash
# Any push to main branch triggers deployment
git add .
git commit -m "Update application"
git push origin main
```

**Manual Trigger:**
1. Go to: https://github.com/gazal1994/final-project-DEVOPS/actions
2. Select "Deploy to AWS EC2" workflow
3. Click "Run workflow"
4. Select branch: main
5. Click "Run workflow"

---

## 🛠️ Manual Deployment (Without GitHub Actions)

### Direct SSH Deployment

```bash
# SSH into EC2
ssh -i C:\Users\windows11\Desktop\keys\KEY.pem ec2-user@13.60.8.113

# Pull and run
docker pull gazal94/final-python-app:latest
docker stop final-python-app || true
docker rm final-python-app || true
docker run -d \
  --name final-python-app \
  --restart unless-stopped \
  -p 80:5000 \
  gazal94/final-python-app:latest

# Exit
exit
```

---

## 📊 Comparison: AWS vs Azure

| Feature | AWS EC2 | Azure VM |
|---------|---------|----------|
| **Status** | ✅ Working | ❌ Blocked by policy |
| **Setup Time** | 5 minutes | N/A |
| **Cost** | Free tier (12 months) | N/A |
| **Instance Type** | t3.micro | Blocked |
| **Region** | eu-north-1 | All blocked |
| **Docker Support** | ✅ Yes | N/A |
| **Public IP** | ✅ Yes | N/A |
| **Deployment** | ✅ Successful | ❌ Failed |

---

## 🎯 Project Completion Status

| Part | Status | Platform | Notes |
|------|--------|----------|-------|
| **PART A** | ✅ Complete | Docker | Dockerfile created and tested |
| **PART B** | ✅ Complete | DockerHub | CI/CD pipeline working |
| **PART C** | ✅ Complete | AWS EC2 | Deployed successfully |

---

## 📝 Documentation Files

1. **PART_C_DOCUMENTATION.md** - Original Azure guide (600+ lines)
2. **PART_C_AWS_DEPLOYMENT.md** - This file (AWS-specific guide)
3. **PART_C_AZURE_LIMITATION.md** - Azure policy issue documentation
4. **ALTERNATIVE_DEPLOYMENT.md** - Other deployment options
5. **README.md** - Project overview

---

## 🔍 Troubleshooting

### Issue: Cannot access application

**Check Security Group:**
```bash
# In AWS Console: EC2 → Security Groups
# Ensure port 80 is open to 0.0.0.0/0
```

### Issue: Container not running

**Check Docker status:**
```bash
ssh -i KEY.pem ec2-user@13.60.8.113
docker ps -a
docker logs final-python-app
```

### Issue: SSH connection failed

**Check permissions:**
```powershell
# Windows - Fix key permissions
icacls "C:\Users\windows11\Desktop\keys\KEY.pem" /inheritance:r
icacls "C:\Users\windows11\Desktop\keys\KEY.pem" /grant:r "$($env:USERNAME):(R)"
```

### Issue: Workflow fails

**Verify GitHub Secrets:**
1. All 5 secrets are added
2. SSH key includes BEGIN/END lines
3. No extra spaces or newlines

---

## 💰 Cost Considerations

### AWS Free Tier (12 months)

- **EC2:** 750 hours/month of t2.micro or t3.micro
- **Data Transfer:** 15 GB outbound per month
- **Storage:** 30 GB EBS

**Current Usage:**
- Instance: t3.micro ✅ (covered by free tier)
- Running time: ~720 hours/month ✅ (within limits)
- Traffic: Minimal ✅ (well under 15 GB)

**Estimated Cost:** $0.00/month (within free tier)

---

## 🚀 Next Steps

### 1. Add HTTPS (Optional)

Use Let's Encrypt for free SSL:

```bash
ssh -i KEY.pem ec2-user@13.60.8.113
sudo yum install -y certbot
# Follow certbot instructions
```

### 2. Set up Custom Domain (Optional)

1. Purchase domain (e.g., from Route 53)
2. Create A record pointing to 13.60.8.113
3. Access via custom domain

### 3. Monitoring (Optional)

```bash
# Install CloudWatch agent
# Set up alarms for CPU, memory, disk usage
```

---

## ✅ Verification Checklist

- [x] EC2 instance running
- [x] Docker installed and configured
- [x] Security group allows ports 22 and 80
- [x] GitHub Actions workflow created
- [x] GitHub Secrets configured
- [x] Container deployed successfully
- [x] Application accessible via public IP
- [x] Swagger UI working
- [x] Auto-restart configured
- [x] Deployment documentation complete

---

## 🎓 Learning Outcomes

### Skills Demonstrated

1. **AWS EC2 Management**
   - Instance creation and configuration
   - Security group management
   - SSH key management

2. **Linux System Administration**
   - Package installation (yum)
   - Service management (systemctl)
   - User permissions

3. **Docker Operations**
   - Installation and configuration
   - Container lifecycle management
   - Image registry (DockerHub) integration

4. **CI/CD with GitHub Actions**
   - Workflow creation
   - SSH-based deployment
   - Secret management

5. **DevOps Best Practices**
   - Infrastructure automation
   - Continuous deployment
   - Security considerations

---

## 📞 Support & Resources

### AWS Documentation
- EC2 User Guide: https://docs.aws.amazon.com/ec2/
- Security Groups: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html

### Project Links
- **GitHub Repository:** https://github.com/gazal1994/final-project-DEVOPS
- **DockerHub Image:** https://hub.docker.com/r/gazal94/final-python-app
- **Application URL:** http://13.60.8.113/api/doc

---

**Deployment Date:** January 30, 2026  
**Status:** ✅ PRODUCTION READY  
**Platform:** AWS EC2  
**Maintainer:** Gazal
