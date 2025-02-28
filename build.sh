#!/bin/zsh

# Folder that contains all locally installed packages
DIRECTORY=.venv

if [[ -d "${DIRECTORY}" && ! -L "${DIRECTORY}" ]]
then
    echo ".venv folder already exists!"
    echo "Activating virtual environment"
    source ${DIRECTORY}/bin/activate

    echo "Listing all installed packages"
    pip3 list

    echo "Checking for broken requirements"
    pip3 check

    echo "Installing necessary packages"
    pip3 install -r requirements.txt

    echo "Listing all installed packages"
    pip3 list
else
    echo "Creating new Python virtual environment"
    python3 -m venv ${DIRECTORY}

    echo "Activating virtual environment"
    source ${DIRECTORY}/bin/activate

    echo "Installing necessary packages"
    pip3 install -r requirements.txt

    echo "Listing all installed packages"
    pip3 list
fi

echo "Deactivating virtual environment"
deactivate