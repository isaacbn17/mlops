# Known Issues & Troubleshooting

This document lists common setup problems encountered by students and how to fix them.

---

## Docker Issues

### Docker command not found
- Docker Desktop or Rancher Desktop is not installed
- Restart terminal after installation

### Docker installed but containers won't run
- Docker Desktop is not running
- On Windows: ensure WSL2 backend is enabled
- Try:
  docker run hello-world

### Rancher Desktop: docker compose missing
- Ensure Docker-compatible CLI is enabled
- Restart Rancher Desktop after changing settings

---

## Port Conflicts

### MLflow fails to start on port 5000
- Another service is using port 5000
- Stop it or change the port in docker-compose.yml

---

## Python Issues

### Wrong Python version
- Use python --version
- On Windows, ensure python from python.org is first in PATH

### Packages fail to install
- Ensure virtual environment is activated
- Upgrade pip:
  pip install -U pip

---

## Windows-Specific

### PowerShell script execution blocked
Run PowerShell as Administrator:
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

### host.docker.internal not resolving
- Use localhost instead
- Or restart Docker Desktop

---

## macOS (Apple Silicon)

### Docker image slow to start
- First run may be slow due to image download
- Subsequent runs are faster

---

## When to Ask for Help
- `env-check.sh` fails repeatedly
- Docker containers exit immediately
- MLflow UI not reachable after 30 seconds

Bring error output when asking for help.
