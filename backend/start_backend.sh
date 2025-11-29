#!/bin/bash
# PM2 wrapper script for backend Flask application
# This script activates the virtual environment and runs app.py

cd "$(dirname "$0")"
source venv/bin/activate
python app.py

