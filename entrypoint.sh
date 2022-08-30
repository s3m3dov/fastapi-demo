#!/bin/sh
# This script checks if the container is started for the first time.

# Load .env variables
export "$(grep -vE "^(#.*|\s*)$" .env)"

# Check if the container is started for the first time.
CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    echo "This container has been started for the first time, running first startup script."
else
    echo "This container has been started before, skipping first startup script."
fi
python main.py
