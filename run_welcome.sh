#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
source "${VENV_PATH:-$SCRIPT_DIR/.venv}/bin/activate"
./guest_wifi.py
