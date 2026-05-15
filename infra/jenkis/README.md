# Jenkins Setup Guide — BloodChain

## Prerequisites
- VPS with Ubuntu 24 running
- Docker installed on the VPS
- Jenkins installed and running on port 8080
- GitHub repository created

---

## Step 1 — Install Jenkins on VPS

```bash
# Install Java
sudo apt update
sudo apt install openjdk-17-jdk -y

# Add Jenkins repo
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key \
  | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian binary/ \
  | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update && sudo apt install jenkins -y
sudo systemctl start jenkins && sudo systemctl enable jenkins
```

Access Jenkins at: http://your-vps-ip:8080

---

## Step 2 — Install Required Plugins

Jenkins Dashboard → Manage Jenkins → Plugins → Available

Install all plugins listed in plugins.txt
Restart Jenkins after installation.

---

## Step 3 — Add Credentials

Jenkins Dashboard → Manage Jenkins → Credentials → Global → Add Credential

### Docker Hub credentials
- Kind: Username with password
- ID: dockerhub-credentials
- Username: your Docker Hub username
- Password: your Docker Hub password or access token

### VPS SSH Key
- Kind: SSH Username with private key
- ID: vps-ssh-key
- Username: root
- Private Key: paste your VPS private SSH key

---

## Step 4 — Create the Pipeline Job

1. Jenkins Dashboard → New Item
2. Name: BloodChain-Pipeline
3. Type: Multibranch Pipeline → OK
4. Branch Sources → Add source → GitHub
5. Repository HTTPS URL:
   https://github.com/your-org/bloodchain.git
6. Credentials: add your GitHub token
7. Build Configuration:
   Mode: by Jenkinsfile
   Script Path: Jenkinsfile
8. Save

---

## Step 5 — Set Up GitHub Webhook

### On your VPS — open port 8080
```bash
sudo ufw allow 8080
sudo ufw reload
```

### On GitHub
1. Go to your repo → Settings → Webhooks → Add webhook
2. Payload URL:
   http://your-vps-ip:8080/github-webhook/
3. Content type: application/json
4. Events: select "Just the push event"
5. Active: checked → Add webhook

### On Jenkins
1. Open your pipeline job → Configure
2. Build Triggers → check:
   GitHub hook trigger for GITScm polling
3. Save

---

## How the Pipeline Works

| Trigger | What runs |
|---|---|
| Push to any feature/* branch | Checkout + Build + Test |
| Push / merge to dev | Checkout + Build + Test + Push to Docker Hub |
| Merge to main | All stages + Deploy to K3s |

---

## Troubleshoot

| Problem | Fix |
|---|---|
| Webhook not triggering | Check port 8080 is open on VPS firewall |
| Docker build fails | Check Dockerfile path in Jenkinsfile |
| K3s deploy fails | Check SSH key and VPS IP in credentials |
| Tests fail | Run locally first: docker compose up |