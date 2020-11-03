#!/bin/bash

set +x
set -Eeuo pipefail

ERRBOT="/errbot/venv/bin/errbot"
RUN_MONO_INSTALL=${MONO_PLUGIN_REQ_INSTALL:-False}
# Execute code to install plugins repos
eval "/errbot/venv/bin/python /errbot/install_plugins.py"

# Source errbot venv
echo "Activate virtual environment"
source /errbot/venv/bin/activate

EXTRA_REQUIREMENTS_FILE_PATH=${EXTRA_REQUIREMENTS_FILE:-/config/extra-requirements.txt}
# install any extra requirements
if [[ -f "$EXTRA_REQUIREMENTS_FILE_PATH" ]]; then
    /errbot/venv/bin/pip install -r $EXTRA_REQUIREMENTS_FILE_PATH
fi

if [[ "$RUN_MONO_INSTALL" = "True" ]]; then
  pip install -r $(find /k8s-volume/plugins/ -name "requirements.txt" | sed ':a;N;$!ba;s/\n/ -r /g')
  export INSTALL_DEPS=False
fi

# Run bot
echo "Executing: $ERRBOT"
eval $ERRBOT
