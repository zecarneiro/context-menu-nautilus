#!/bin/bash
# Exit if
# e: exit as soon as any command it executes fails
# u: exit if it tries to use an uninitialized variable
# o pipefail: exits if any command in a pipeline fails
set -euo pipefail

INSTALL_PATH="${HOME}/.local/share/nautilus-python/extensions"
EXTENSION_NAME="context-menu-nautilus"
EXTENSION_FILE_NAME="${EXTENSION_NAME}.py"
EXTENSION_FILE="${INSTALL_PATH}/${EXTENSION_FILE_NAME}"
EXTENSION_CACHE_FILE="${INSTALL_PATH}/__pycache__/${EXTENSION_NAME}*"
CONFIG_PATH="${HOME}/.config/${EXTENSION_NAME}"
INSTALLER_CONFIG="$HOME/.local/bin/install-context-menu-nautilus-conf"

echo "Uninstall..."
echo "Removing: ${EXTENSION_FILE}"
rm -f "${EXTENSION_FILE}"
echo "Removing extension cache on: ${INSTALL_PATH}/__pycache__"
find "${INSTALL_PATH}/__pycache__" -name "${EXTENSION_NAME}*" -exec rm {} \;
echo "Removing: ${CONFIG_PATH}"
rm -rf "${CONFIG_PATH}"
echo "Removing: ${INSTALLER_CONFIG}"
rm -f "${INSTALLER_CONFIG}"


echo "Uninstallation Complete"
