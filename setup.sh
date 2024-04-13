#!/bin/bash

docker-compose up --build -d

cd flask
python3 -m venv mangoflask

directory="./mangoflask/Scripts"
directory2="./mangoflask/bin"


if [ -d "$directory" ]; then
    echo "Scripts dir exists. Running command 1..."
    # Command to execute if directory exists
    source mangoflask/Scripts/activate
elif [[ -d "$directory2" ]]; then
    
    echo "bin dir exists. Running command 2..."
    # Command to execute if directory does not exist
    source mangoflask/bin/activate
else
    echo "Neither directory found. Aborting."
    exit 1
fi

cd ../project
pip install -r requirements.txt
python app.py
