# tiny Installation Utility Script
# This script sets up the tiny environment

#!/bin/bash

#check git
whereis -b "git"

if command -v git >/dev/null 2>&1; then
    echo "INFO: git found."
else
    echo "ERR: git not installed. Please install git using your package manager."
    exit
fi

#check python
whereis -b "python"

if command -v python >/dev/null 2>&1; then
    echo "INFO: python found."
else
    echo "WARN: python not available under 'python'. Checking for 'python3'"
    whereis -b "python3"
    if command -v python3 >/dev/null 2>&1; then
        echo "INFO: python3 found. Creating symlink from python3 to python"
        sudo ln -s $(which python3) /usr/bin/python
        if [ $? -eq 0 ]; then
            return 0
        else
            echo "ERR: failed to create symlink from python3 to python."
        fi
    else
        echo "ERR: python/python3 not installed. Please install python using your package manager."
        exit
    fi
fi

whereis -b "pip"
if command -v pip >/dev/null 2>&1; then
    echo "INFO: pip found."
else
    echo "ERR: pip not installed. If you are using the python binaries including with your operating system, try reinstalling/updating python with your package manager."
    exit
fi
# clean if updating
rm -rf ~/.tiny
sudo rm -rf /usr/bin/tiny
#install dependencies
pip install psutil --break-system-packages
# make installation directory
cd ~
mkdir .tiny
cd .tiny
mkdir temp
cd temp
git clone https://github.com/pherionics-ltd/tiny.git
cd tiny
sudo mv ./tiny /usr/bin/tiny
sudo chmod +x /usr/bin/tiny
sudo mv ./modules ../../modules
