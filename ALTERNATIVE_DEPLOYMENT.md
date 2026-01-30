# Alternative Deployment Solutions

## Overview

This document provides alternative deployment methods for the Flask API application when Azure VM deployment is not available.

---

## Option 1: Railway.app (Recommended) 🚂

**Platform:** https://railway.app

### Advantages
- ✅ Free tier available (500 hours/month)
- ✅ Automatic Docker deployment
- ✅ Direct GitHub integration
- ✅ Public HTTPS URL provided
- ✅ Automatic SSL certificates
- ✅ Environment variables support
- ✅ Automatic deployments on git push

### Setup Steps

1. **Sign Up**
   - Go to: https://railway.app
   - Click "Login with GitHub"
   - Authorize Railway

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `gazal1994/final-project-DEVOPS`

3. **Configure Deployment**
   - Railway automatically detects Dockerfile
   - No additional configuration needed
   - Click "Deploy"

4. **Access Application**
   - Railway provides a public URL
   - Click "Settings" → "Generate Domain"
   - Access at: `https://your-app.up.railway.app/api/doc`

### Cost
- **Free Tier:** 500 hours/month
- **Paid Tier:** $5/month for unlimited hours

---

## Option 2: Render.com 🎨

**Platform:** https://render.com

### Advantages
- ✅ Free tier for web services
- ✅ Docker support
- ✅ Automatic deployments
- ✅ Free SSL certificates
- ✅ Good performance

### Setup Steps

1. **Sign Up**
   - Go to: https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `final-project-DEVOPS`

3. **Configure Service**
   - **Name:** `final-python-app`
   - **Environment:** Docker
   - **Plan:** Free
   - **Dockerfile Path:** `./Dockerfile`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (3-5 minutes)
   - Access at: `https://final-python-app.onrender.com/api/doc`

### Limitations (Free Tier)
- Spins down after 15 minutes of inactivity
- Cold start takes ~30 seconds

---

## Option 3: Fly.io ✈️

**Platform:** https://fly.io

### Advantages
- ✅ Free tier includes 3 VMs
- ✅ Excellent Docker support
- ✅ Global deployment
- ✅ Fast cold starts

### Setup Steps

1. **Install Fly CLI**

   **Windows (PowerShell):**
   ```powershell
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login**
   ```powershell
   flyctl auth login
   ```

3. **Initialize App**
   ```powershell
   cd "C:\Users\windows11\Desktop\Final Project DEVOPS\final-project-DEVOPS"
   flyctl launch
   ```

4. **Configure**
   - App name: `final-python-app`
   - Region: Choose closest
   - PostgreSQL: No
   - Redis: No

5. **Deploy**
   ```powershell
   flyctl deploy
   ```

6. **Access**
   ```powershell
   flyctl open /api/doc
   ```

---

## Option 4: Docker Hub + Local Testing 🐳

**For demonstration/testing purposes**

### Pull and Run from DockerHub

```powershell
# Pull the latest image
docker pull gazal94/final-python-app:latest

# Run the container
docker run -d -p 5000:5000 --name final-python-app gazal94/final-python-app:latest

# Access application
Start-Process "http://localhost:5000/api/doc"
```

### Expose Locally with ngrok

**What is ngrok?**
Provides a public URL for local applications.

**Steps:**

1. **Download ngrok**
   - Go to: https://ngrok.com/download
   - Download Windows version
   - Extract to `C:\ngrok`

2. **Sign up** (Free account)
   - https://dashboard.ngrok.com/signup

3. **Get Auth Token**
   - Copy your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken

4. **Configure**
   ```powershell
   C:\ngrok\ngrok.exe config add-authtoken YOUR_TOKEN
   ```

5. **Start Tunnel**
   ```powershell
   # Make sure app is running on port 5000
   C:\ngrok\ngrok.exe http 5000
   ```

6. **Access Public URL**
   - ngrok displays a public URL like: `https://abc123.ngrok.io`
   - Access at: `https://abc123.ngrok.io/api/doc`

**Limitations:**
- Free tier has session time limits
- URL changes each time you restart
- Not suitable for production

---

## Option 5: Heroku 💜

**Platform:** https://heroku.com

### Note
Heroku no longer offers free tier, but provides $5/month hobby tier.

### Setup Steps

1. **Install Heroku CLI**
   ```powershell
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login**
   ```powershell
   heroku login
   ```

3. **Create App**
   ```powershell
   cd "C:\Users\windows11\Desktop\Final Project DEVOPS\final-project-DEVOPS"
   heroku create final-python-app-gazal
   ```

4. **Deploy**
   ```powershell
   git push heroku main
   ```

5. **Access**
   ```powershell
   heroku open /api/doc
   ```

---

## Option 6: Google Cloud Run ☁️

**Platform:** https://cloud.google.com/run

### Advantages
- ✅ Free tier: 2 million requests/month
- ✅ Automatic scaling
- ✅ Pay only when running

### Setup Steps

1. **Install gcloud CLI**
   - Download from: https://cloud.google.com/sdk/docs/install

2. **Initialize**
   ```powershell
   gcloud init
   ```

3. **Enable Cloud Run API**
   ```powershell
   gcloud services enable run.googleapis.com
   ```

4. **Deploy**
   ```powershell
   cd "C:\Users\windows11\Desktop\Final Project DEVOPS\final-project-DEVOPS"
   
   gcloud run deploy final-python-app `
     --source . `
     --platform managed `
     --region us-central1 `
     --allow-unauthenticated
   ```

---

## Comparison Table

| Platform | Free Tier | Docker Support | Auto Deploy | SSL | GitHub Integration |
|----------|-----------|----------------|-------------|-----|-------------------|
| **Railway** | ✅ 500hrs | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Render** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Fly.io** | ✅ 3 VMs | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Manual |
| **ngrok** | ✅ Limited | N/A | ❌ No | ✅ Yes | ❌ No |
| **Heroku** | ❌ $5/mo | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Cloud Run** | ✅ 2M req | ✅ Yes | ⚠️ Manual | ✅ Yes | ⚠️ Manual |

---

## Recommendation

### For Project Submission
**Railway.app** or **Render.com**
- Easy setup
- Free tier
- Professional public URL
- Automatic deployments

### For Quick Demo
**ngrok** with local Docker
- Instant setup
- No account needed initially
- Good for testing

### For Learning
**Fly.io** or **Google Cloud Run**
- More cloud-native
- Better for resume/portfolio
- Industry-standard tools

---

## Next Steps

Choose one option above and follow the setup steps. All options work with the existing Dockerfile and don't require code changes.

**Need help?** All platforms have excellent documentation and support.
