#!/bin/sh

# Local .env
if [ -f .env ]; then
    # Load Environment Variables
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

mysql -h "${WALLET_DB_HOST}" -u "${WALLET_DB_USER}" -p"${WALLET_DB_PASS}" < ./mysql-init/initial-data.sql