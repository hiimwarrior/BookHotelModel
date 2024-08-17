#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Error: This command requires exactly one argument ('ds' for data_science or 'de' for data_engineering)."
    exit 1
fi

directory=$1

case $directory in
    ds)
        venv_dir="data_science/venv"
        requirements_file="data_science/requirements.txt"
        notebook_dir="data_science/src/experiments"
        ;;
    de)
        venv_dir="data_engineering/venv"
        requirements_file="data_engineering/requirements.txt"
        notebook_dir="data_engineering/src/experiments"
        ;;
    *)
        echo "Error: Invalid argument '$directory'. Use 'ds' for data_science or 'de' for data_engineering."
        exit 1
        ;;
esac

if [ ! -d "$venv_dir" ]; then
    echo "Virtual environment not found in $venv_dir. Creating it..."
    python3 -m venv "$venv_dir"
    echo "Virtual environment created."
fi

echo "Activating virtual environment in $venv_dir..."
source "$venv_dir/bin/activate"

# Install dependencies from the requirements.txt file
if [ -f "$requirements_file" ]; then
    echo "Installing dependencies from $requirements_file..."
    pip install -r "$requirements_file"
else
    echo "No requirements.txt found in $requirements_file. Skipping dependency installation."
fi

echo "Starting Jupyter Notebook in $notebook_dir..."
cd "$notebook_dir" || exit
jupyter notebook
