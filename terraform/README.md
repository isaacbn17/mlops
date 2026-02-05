# Terraform Local Example (Optional)

This folder demonstrates **Infrastructure as Code** locally using Terraform's Docker provider.

Why it's optional:
- Terraform must download providers on first run (internet required once).
- It is not required for the core labs (Docker Compose is the main IaC path).

What it does:
- Creates a local Docker network
- Runs a tiny NGINX container reachable at http://localhost:8088

## Prerequisites
- Terraform >= 1.5 installed and on PATH
- Docker running

## Run
terraform init
terraform plan
terraform apply

Then visit:
http://localhost:8088

## Cleanup
terraform destroy
