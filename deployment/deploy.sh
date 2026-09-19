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

# Install the latest unit file as a user service and restart it.
# Lingering lets the service start at boot without logging in.
scp deployment/water-monitor.service "$host:/tmp/water-monitor.service"
ssh -t "$host" '
    install -D -m 644 /tmp/water-monitor.service ~/.config/systemd/user/water-monitor.service &&
    rm /tmp/water-monitor.service &&
    sudo loginctl enable-linger "$USER" &&
    systemctl --user daemon-reload &&
    systemctl --user enable water-monitor.service &&
    systemctl --user restart water-monitor.service &&
    systemctl --user --no-pager status water-monitor.service
'
