# Troubleshooting Setup Issues

## Issue 1: Docker Command Not Found

### Problem
```bash
bash: docker: command not found
```

### Solutions

#### Solution A: Start Docker Desktop (Most Common)

1.  **Open Docker Desktop application**
    *   Look for Docker in your Applications folder
    *   Or search for "Docker" in Spotlight (Cmd + Space)
2.  **Wait for Docker to start**
    *   You'll see a whale icon in your menu bar
    *   Wait until it says "Docker Desktop is running"
3.  **Verify Docker is running**
    ```bash
    docker --version
    docker ps
    ```

#### Solution B: Add Docker to PATH

If Docker Desktop is running but command not found:

```bash
# Add Docker to your PATH
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"

# Verify
docker --version
```

#### Solution C: Install Docker Desktop

If Docker is not installed:

1.  Download from: https://www.docker.com/products/docker-desktop
2.  Install Docker Desktop for Mac
3.  Open Docker Desktop
4.  Wait for it to start
5.  Try docker commands again

---

## Issue 2: SN_ICR_NAMESPACE is Empty

### Problem
```bash
echo $SN_ICR_NAMESPACE
# Returns empty
```

### Solutions

#### Solution A: Set the Environment Variable

You need to get your IBM Container Registry namespace first:

```bash
# Login to IBM Cloud (if not already)
ibmcloud login

# Login to Container Registry
ibmcloud cr login

# List your namespaces
ibmcloud cr namespace-list
```

This will show your namespace(s). Then set it:

```bash
# Replace 'your-namespace' with actual namespace from the list
export SN_ICR_NAMESPACE=your-namespace

# Verify
echo $SN_ICR_NAMESPACE
```

#### Solution B: Create a Namespace (if you don't have one)

```bash
# Create a new namespace
ibmcloud cr namespace-add your-desired-namespace-name

# Set the environment variable
export SN_ICR_NAMESPACE=your-desired-namespace-name

# Verify
echo $SN_ICR_NAMESPACE
```

#### Solution C: Make it Permanent

To avoid setting it every time, add to your shell profile:

**For bash (~/.bash_profile or ~/.bashrc):**
```bash
echo 'export SN_ICR_NAMESPACE=your-namespace' >> ~/.bash_profile
source ~/.bash_profile
```

**For zsh (~/.zshrc):**
```bash
echo 'export SN_ICR_NAMESPACE=your-namespace' >> ~/.zshrc
source ~/.zshrc
```

---

## Complete Setup Verification

Run these commands to verify everything is ready:

```bash
# 1. Check Docker
docker --version
docker ps

# 2. Check IBM Cloud login
ibmcloud target

# 3. Check Container Registry
ibmcloud cr login
ibmcloud cr namespace-list

# 4. Check environment variable
echo $SN_ICR_NAMESPACE

# 5. Check Code Engine
ibmcloud ce project current
```

---

## Step-by-Step Setup Process

### Step 1: Start Docker Desktop
```bash
# Open Docker Desktop application
# Wait for "Docker Desktop is running" message
```

### Step 2: Login to IBM Cloud
```bash
ibmcloud login
# Follow the prompts
```

### Step 3: Setup Container Registry
```bash
# Login to registry
ibmcloud cr login

# List or create namespace
ibmcloud cr namespace-list

# If no namespace exists, create one:
# ibmcloud cr namespace-add my-namespace
```

### Step 4: Set Environment Variable
```bash
# Replace with your actual namespace
export SN_ICR_NAMESPACE=your-namespace-here

# Verify
echo $SN_ICR_NAMESPACE
```

### Step 5: Select Code Engine Project
```bash
# List projects
ibmcloud ce project list

# Select your project
ibmcloud ce project select --name your-project-name
```

### Step 6: Verify Setup
```bash
# All these should work without errors
docker --version
ibmcloud target
echo $SN_ICR_NAMESPACE
ibmcloud ce project current
```

---

## Once Setup is Complete

After fixing both issues, run the deployment commands:

```bash
# Navigate to directory
cd /Users/Salama/IBM/xrwvm-fullstack_developer_capstone/server/djangoapp/microservices

# Build Docker image
docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer

# Push to registry
docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer

# Deploy to Code Engine
ibmcloud ce application create --name sentianalyzer \
    --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer \
    --registry-secret icr-secret \
    --port 5000

# Get application URL
ibmcloud ce application get --name sentianalyzer

# Test
curl [YOUR_URL]/analyze/Fantastic%20services
```

---

## Quick Checklist

Before running deployment commands, verify:

- [ ] Docker Desktop is running (whale icon in menu bar)
- [ ] `docker --version` works
- [ ] `docker ps` works
- [ ] `ibmcloud target` shows you're logged in
- [ ] `ibmcloud cr namespace-list` shows your namespace
- [ ] `echo $SN_ICR_NAMESPACE` shows your namespace
- [ ] `ibmcloud ce project current` shows your project

---

## Common Error Messages and Fixes

### "Cannot connect to the Docker daemon"
**Fix:** Start Docker Desktop application

### "unauthorized: authentication required"
**Fix:** Run `ibmcloud cr login`

### "namespace not found"
**Fix:** Create namespace with `ibmcloud cr namespace-add your-namespace`

### "No Code Engine project selected"
**Fix:** Run `ibmcloud ce project select --name your-project`

### "registry-secret not found"
**Fix:** The secret should be created automatically. If not:
```bash
ibmcloud ce registry create --name icr-secret --server us.icr.io
```

---

## Alternative: Use IBM Cloud Web Console

If command line issues persist, you can deploy via web console:

1. Go to: https://cloud.ibm.com/codeengine
2. Select your project
3. Click "Create" → "Application"
4. Configure:
   - Name: sentianalyzer
   - Container image: us.icr.io/[namespace]/senti_analyzer
   - Port: 5000
5. Click "Create"

But you still need to build and push the Docker image first using Docker Desktop.

---

## Need More Help?

1. Check Docker Desktop is installed and running
2. Verify IBM Cloud CLI is installed: `ibmcloud --version`
3. Check you're in the right directory
4. Review error messages carefully
5. Try each command individually to isolate the issue

---

## Summary of Required Tools

| Tool | Check Command | Install/Setup |
| --- | --- | --- |
| Docker Desktop | `docker --version` | https://www.docker.com/products/docker-desktop |
| IBM Cloud CLI | `ibmcloud --version` | https://cloud.ibm.com/docs/cli |
| Code Engine Plugin | `ibmcloud plugin list` | `ibmcloud plugin install code-engine` |
| Container Registry Access | `ibmcloud cr login` | Automatic with IBM Cloud |

---

**After fixing these issues, return to MANUAL_DEPLOYMENT_STEPS.md to continue deployment.**
