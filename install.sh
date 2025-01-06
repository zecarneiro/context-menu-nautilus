#!/bin/bash
# Exit if
# e: exit as soon as any command it executes fails
# u: exit if it tries to use an uninitialized variable
# o pipefail: exits if any command in a pipeline fails
set -euo pipefail

TYPE_INSTALL="${1:-1}"
INSTALL_PATH="${HOME}/.local/share/nautilus-python/extensions"
EXTENSION_NAME="context-menu-nautilus"
EXTENSION_FILE_NAME="${EXTENSION_NAME}.py"
EXTENSION_FILE="${INSTALL_PATH}/${EXTENSION_FILE_NAME}"
CONFIG_DIR="$HOME/.config/${EXTENSION_NAME}"
BASHRC_FILE="${HOME}/.bashrc"
INSTALLER_CONFIG_DIR="$HOME/.local/bin"
INSTALLER_CONFIG="$INSTALLER_CONFIG_DIR/install-context-menu-nautilus-conf"

# Install python-nautilus
echo "Installing python-nautilus..."
if type "pacman" > /dev/null 2>&1
then
    # check if already install, else install
    pacman -Qi python-nautilus &> /dev/null
    if [ `echo $?` -eq 1 ]
    then
        sudo pacman -S --noconfirm python-nautilus
    else
        echo "python-nautilus is already installed"
    fi
elif type "apt-get" > /dev/null 2>&1
then
    # Find Ubuntu python-nautilus package
    package_name="python-nautilus"
    found_package=$(apt-cache search --names-only $package_name)
    if [ -z "$found_package" ]
    then
        package_name="python3-nautilus"
    fi

    # Check if the package needs to be installed and install it
    installed=$(apt list --installed $package_name -qq 2> /dev/null)
    if [ -z "$installed" ]
    then
        sudo apt-get install -y $package_name
    else
        echo "$package_name is already installed."
    fi
elif type "dnf" > /dev/null 2>&1
then
    installed=`dnf list --installed nautilus-python 2> /dev/null`
    if [ -z "$installed" ]
    then
        sudo dnf install -y nautilus-python
    else
        echo "nautilus-python is already installed."
    fi
else
    echo "Failed to find python-nautilus, please install it manually."
fi

if [ ! -d "$CONFIG_DIR" ]; then
    echo "Creating directory: $CONFIG_DIR"
    mkdir "$CONFIG_DIR"
fi

if [ ! -d "$INSTALLER_CONFIG_DIR" ]; then
    echo "Creating directory: $INSTALLER_CONFIG_DIR"
    mkdir "$INSTALLER_CONFIG_DIR"
fi

if [ "$TYPE_INSTALL" = "local" ]; then
    eval "${PWD}/uninstall.sh"
    echo "Install..."
    cp "${PWD}/${EXTENSION_FILE_NAME}" "${EXTENSION_FILE}"
    cp "${PWD}/install-context-menu-nautilus-conf" "$INSTALLER_CONFIG"
    chmod +x "$INSTALLER_CONFIG"
else
    # Uninstall
    wget -qO- https://raw.githubusercontent.com/zecarneiro/context-menu-nautilus/master/uninstall.sh | bash

    echo "Downloading and install newest version..."
    wget -q -O "${EXTENSION_FILE}" https://raw.githubusercontent.com/zecarneiro/context-menu-nautilus/master/context-menu-nautilus.py
    wget -q -O "$INSTALLER_CONFIG" https://raw.githubusercontent.com/zecarneiro/context-menu-nautilus/master/install-context-menu-nautilus-conf
    chmod +x "$INSTALLER_CONFIG"
fi

# Restart nautilus
echo "Restarting nautilus..."
nautilus -q

echo "Installation Complete"
