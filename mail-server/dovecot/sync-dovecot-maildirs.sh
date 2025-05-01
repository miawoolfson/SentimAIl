#!/bin/bash

# Path to Dovecot users file (flat file)
USER_FILE="./dovecot/config/users"

# Target Docker container name
DOVECOT_CONTAINER="dovecot"

# Loop through each user in the users file
while IFS=: read -r EMAIL _; do
  if [[ -z "$EMAIL" ]]; then continue; fi

  echo "🔍 Checking Maildir for: $EMAIL"

  docker exec "$DOVECOT_CONTAINER" sh -c "test -d /var/mail/$EMAIL/Maildir"
  if [[ $? -ne 0 ]]; then
    echo "➕ Creating Maildir for $EMAIL..."
    docker exec "$DOVECOT_CONTAINER" sh -c "mkdir -p /var/mail/$EMAIL/Maildir && chown -R vmail:vmail /var/mail/$EMAIL"
    echo "✅ Maildir created"
  else
    echo "✅ Maildir already exists"
  fi
done < "$USER_FILE"

docker cp ./dovecot/config/users dovecot:/etc/dovecot/users
docker-compose restart dovecot

echo "🎉 Sync complete!"
