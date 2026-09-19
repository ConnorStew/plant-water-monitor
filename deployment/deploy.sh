#!/usr/bin/env bash
# Deploys the script to the pi.
# Usage: ./deployment/deploy.sh <user>@<pi-ip>
set -euo pipefail

host="${1:?Usage: $0 <user>@<pi-ip>}"

cd "$(dirname "$0")/.."

# README.md is required: pyproject.toml references it, so the package won't build without it.
# Uses --delete to clean any files removed on the repo side.
rsync -avz --delete --exclude=__pycache__ \
    pyproject.toml uv.lock README.md src res \
    "$host:~/water-monitor/"

# Install the latest unit file and restart the service.
scp deployment/water-monitor.service "$host:/tmp/water-monitor.service"
ssh -t "$host" '
    sudo install -m 644 /tmp/water-monitor.service /etc/systemd/system/water-monitor.service &&
    rm /tmp/water-monitor.service &&
    sudo systemctl daemon-reload &&
    sudo systemctl enable water-monitor.service &&
    sudo systemctl restart water-monitor.service &&
    systemctl --no-pager status water-monitor.service
'
