#!/usr/bin/env bash
set -euo pipefail


# This script adds a virtual mailbox user to Postfix and Dovecot containers.
# Usage: ./add-mail-user.sh [userfile]
# Reads email:password lines from the given file (default ./scripts/mails.txt)
USER_FILE="${1:-./scripts/mails.txt}"
if [[ ! -f "$USER_FILE" ]]; then
  echo "User file '$USER_FILE' not found"
  exit 1
fi

added_any=0

while IFS=: read -r EMAIL PASSWORD || [[ -n "$EMAIL" ]]; do
  [[ -z "$EMAIL" || "$EMAIL" == \#* ]] && continue

  # Check and add to Postfix
    if ! docker-compose exec -T postfix grep -q "^$EMAIL " /etc/postfix/vmailbox < /dev/null; then
    echo "Adding $EMAIL to Postfix..."
    docker-compose exec -T postfix sh -c \
      "echo '$EMAIL $EMAIL' >> /etc/postfix/vmailbox && postmap /etc/postfix/vmailbox" < /dev/null
    echo "$EMAI $EMAILL" >> ../postfix/config/vmailbox 
    added_any=1
  else
    echo "$EMAIL already exists in Postfix, skipping"
  fi

  # Check and add to Dovecot
  if ! docker-compose exec -T dovecot grep -q "^$EMAIL:" /etc/dovecot/users < /dev/null; then
    echo "Adding $EMAIL to Dovecot..."
    docker-compose exec -T dovecot sh -c \
      "echo '$EMAIL:{PLAIN}$PASSWORD' >> /etc/dovecot/users && chown vmail:vmail /etc/dovecot/users" < /dev/null
    echo "$EMAIL $PASSWORD" >> ../dovecot/config/users
    added_any=1
  else
    echo "$EMAIL already exists in Dovecot, skipping"
  fi

  # Ensure Maildir structure
  echo "Ensuring Maildir for $EMAIL..."
  docker-compose exec -T dovecot sh -c \
    "mkdir -p /var/mail/$EMAIL/Maildir/ && chown -R vmail:vmail /var/mail/$EMAIL" < /dev/null
done < "$USER_FILE"

# Restart services if needed
if [[ $added_any -eq 1 ]]; then
  echo "Restarting Postfix and Dovecot containers..."
  docker-compose restart postfix dovecot
else
  echo "No new users to add"
fi 