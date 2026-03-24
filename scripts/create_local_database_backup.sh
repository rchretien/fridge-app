#!/usr/bin/env bash
set -euo pipefail

# --- LOAD .env VARIABLES ---
if [ -f ".env" ]; then
  echo "📥 Loading environment variables from .env"
  set -o allexport
  source .env
  set +o allexport
else
  echo "❌ No .env file found. Please create one."
  exit 1
fi

# --- CHECK REQUIRED VARIABLES ---
REQUIRED_VARS=(DB_USER DB_PASSWORD DB_HOST DB_NAME DB_PORT)

for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var:-}" ]; then
    echo "❌ Environment variable '$var' is missing in .env"
    exit 1
  fi
done

# --- BUILD CONNECTION URL ---
DB_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

# --- BACKUP SETTINGS ---
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
FILENAME="backup_${TIMESTAMP}.dump"
FULL_PATH="${BACKUP_DIR}/${FILENAME}"

# Create backup directory if missing
mkdir -p "$BACKUP_DIR"

echo "📦 Running pg_dump..."
pg_dump "$DB_URL" -Fc -f "$FULL_PATH"

echo "✅ Backup created: $FULL_PATH"
