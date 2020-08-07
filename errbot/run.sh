#!/bin/bash

set +x
set -Eeuo pipefail

ERRBOT="/errbot/venv/bin/errbot"

# Execute code to install plugins repos
eval "/errbot/venv/bin/python /errbot/install_plugins.py"

# Source errbot venv
echo "Activate virtual environment"
source /errbot/venv/bin/activate

# Run bot
echo "Executing: $ERRBOT"
eval $ERRBOT
