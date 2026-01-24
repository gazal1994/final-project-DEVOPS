# DevOps Final Project - PART A: Dockerfile Implementation

## Project Overview
This is a Flask REST API application using Flask-RESTPlus, Flask-Marshmallow, and SQLite database.

## Files Created
- **Dockerfile**: Production-ready Docker configuration

## Prerequisites
- Docker installed on your system
- Git (if cloning from repository)

---

## Docker Build & Run Commands

### 1. Build the Docker Image
```bash
cd "C:\Users\windows11\Desktop\Final Project DEVOPS\final-python"
docker build -t final-python-app .
```

**Explanation:**
- `-t final-python-app`: Tags the image with name "final-python-app"
- `.`: Uses current directory as build context

### 2. Run the Docker Container
```bash
docker run -d -p 5000:5000 --name final-python-container final-python-app
```

**Explanation:**
- `-d`: Run in detached mode (background)
- `-p 5000:5000`: Maps host port 5000 to container port 5000
- `--name final-python-container`: Names the container for easy reference
- `final-python-app`: The image to run

---

## Application Details

### Port Information
- **Port Used**: 5000
- **Access URL**: http://localhost:5000
- **Swagger UI (API Documentation)**: http://localhost:5000/api/doc

### Environment Variables
The Dockerfile sets these defaults:
- `FLASK_ENV=production`: Runs Flask in production mode
- `PYTHONUNBUFFERED=1`: Ensures Python output is sent straight to terminal

---

## Quick Test Checklist

### 1. Test with curl (Command Line)
```bash
# Test if the API is responding
curl http://localhost:5000/api/doc

# Test stores endpoint
curl http://localhost:5000/api/stores

# Test items endpoint
curl http://localhost:5000/api/items
```

### 2. Test with Browser
1. Open browser and navigate to: **http://localhost:5000/api/doc**
2. You should see the Swagger UI interface
3. Try the following endpoints:
   - `/api/stores` - Manage stores
   - `/api/items` - Manage items

### 3. Verify Container is Running
```bash
# Check running containers
docker ps

# View container logs
docker logs final-python-container

# Check if app is listening on port 5000
docker exec final-python-container netstat -tuln | grep 5000
```

---

## Useful Docker Commands

### Stop the Container
```bash
docker stop final-python-container
```

### Start the Container Again
```bash
docker start final-python-container
```

### Remove the Container
```bash
docker rm -f final-python-container
```

### Remove the Image
```bash
docker rmi final-python-app
```

### View Container Logs (Real-time)
```bash
docker logs -f final-python-container
```

### Access Container Shell (for debugging)
```bash
docker exec -it final-python-container /bin/bash
```

---

## Dockerfile Explanation

```dockerfile
FROM python:3.11-slim          # Small base image (~50MB vs ~900MB for full python:3.11)
WORKDIR /app                    # Sets working directory inside container
COPY requirements.txt .         # Copy dependencies file first (Docker layer caching)
RUN pip install --no-cache-dir  # Install dependencies, --no-cache-dir reduces image size
COPY . .                        # Copy all application files
EXPOSE 5000                     # Document which port the app uses
ENV FLASK_ENV=production        # Set environment variables
CMD ["python", "app.py"]        # Command to run when container starts
```

### Why These Choices?
1. **python:3.11-slim**: Small, secure base image (significantly smaller than full Python image)
2. **WORKDIR /app**: Clean organization and consistent paths
3. **Copy requirements first**: Docker caches layers - dependencies change less often than code
4. **--no-cache-dir**: Prevents pip from caching downloaded packages, reducing image size
5. **EXPOSE 5000**: Documents the port (matches app.py configuration)
6. **CMD**: Uses exec form (proper signal handling)

---

## Troubleshooting

### Port Already in Use
If you see "port is already allocated" error:
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
docker run -d -p 5001:5000 --name final-python-container final-python-app
```

### Container Won't Start
Check logs:
```bash
docker logs final-python-container
```

### Permission Issues
Run PowerShell/CMD as Administrator

---

## Expected Output

### Successful Build Output
```
[+] Building 15.3s (10/10) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 456B
 => [internal] load .dockerignore
 => [1/5] FROM python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .
 => exporting to image
 => => writing image sha256:...
 => => naming to docker.io/library/final-python-app
```

### Successful Run Output (docker logs)
```
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
```

---

## Summary

✅ **Dockerfile created** at repository root  
✅ **Base image**: python:3.11-slim (production-ready, small footprint)  
✅ **Port exposed**: 5000  
✅ **Build command**: `docker build -t final-python-app .`  
✅ **Run command**: `docker run -d -p 5000:5000 --name final-python-container final-python-app`  
✅ **Test URL**: http://localhost:5000/api/doc  
✅ **Application**: Flask REST API with Swagger UI

**Status**: Ready for deployment! 🚀
