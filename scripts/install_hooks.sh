#!/usr/bin/env bash
set -e

# Ensure we are at the project root
PROJECT_ROOT="$(pwd)"

# Check if this is already a git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[setup] No git repository detected."
  echo "[setup] Initializing git repository..."
  git init
  echo "[setup] Git repository initialized."
else
  echo "[setup] Git repository already exists."
fi

# Ensure hooks directory exists
mkdir -p .git/hooks

# Install post-commit hook
cat > .git/hooks/post-commit <<'EOF'
#!/usr/bin/env bash
set -e

echo "[post-commit] Triggering local CI/CD pipeline"

# Always run from the repo root
cd "$(git rev-parse --show-toplevel)"

# Run deployment pipeline
./scripts/deploy_local.sh
EOF

# Make hook executable
chmod +x .git/hooks/post-commit

echo "[setup] post-commit hook installed successfully."
echo "[setup] CI/CD will now run automatically after each commit."

