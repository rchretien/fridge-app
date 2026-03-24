#!/usr/bin/env bash

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

# List all backups
BACKUPS=$(curl -s -X POST \
            "$SUPABASE_URL/storage/v1/object/list/backups" \
            -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
            -H "Content-Type: application/json" \
            -d '{"prefix": "", "limit": 100, "sortBy": {"column": "created_at", "order": "desc"}}')

echo "Current backups:"
echo "$BACKUPS" | jq '.'

# Get backup filenames, skip the 7 most recent
FILES_TO_DELETE=$(echo "$BACKUPS" | jq -r '.[7:] | .[] | .name')

# Delete old backups
if [ ! -z "$FILES_TO_DELETE" ]; then
  echo "Deleting old backups:"
  echo "$FILES_TO_DELETE"

  for file in $FILES_TO_DELETE; do
    echo "Deleting: $file"
    curl -X DELETE \
                "$SUPABASE_URL/storage/v1/object/backups/$file" \
                -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY"
done
else
  echo "No old backups to delete (7 or fewer backups exist)"
fi