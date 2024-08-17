#!/bin/bash

# Define paths
VENV_DIR="../venv"
REQUIREMENTS_FILE="scripts/requirements.txt"
ROOT_DIR=$(dirname "$(realpath "$0")")/..
VALID_DIRECTORIES=("api" "data_science" "data_engineering")

# Function to display help message
show_help() {
    echo "Usage: $0 [DIRECTORY|all]"
    echo
    echo "This script runs linting checks using ruff on the specified directory or on all directories."
    echo
    echo "DIRECTORY:"
    echo "  api                  Lint the 'api' directory"
    echo "  data_science          Lint the 'data_science' directory"
    echo "  data_engineering      Lint the 'data_engineering' directory"
    echo "  all                  Lint all directories in order (api, data_science, data_engineering)"
    echo
    echo "Options:"
    echo "  -h, --help           Show this help message and exit"
    echo "  --fix                Apply automatic fixes where possible"
}

# Check if the required directory parameter is provided
if [ "$#" -lt 1 ]; then
    echo "Error: Directory parameter is required."
    show_help
    exit 1
fi

# Check if the --fix option is provided
FIX_OPTION=""
if [ "$#" -ge 2 ] && [ "$2" == "--fix" ]; then
    FIX_OPTION="--fix"
fi

# Validate the directory argument
ARGUMENT=$1
if [[ ! " ${VALID_DIRECTORIES[@]} " =~ " ${ARGUMENT} " ]] && [ "$ARGUMENT" != "all" ]; then
    echo "Error: Invalid directory '$ARGUMENT'. Valid options are: ${VALID_DIRECTORIES[*]} or 'all'."
    show_help
    exit 1
fi

# Create and activate virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one..."
    python -m venv "$VENV_DIR"
    echo "Virtual environment created."
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"
source "$VENV_DIR/Scripts/activate"  # Windows, uncomment if needed

# Install dependencies from requirements.txt
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "$REQUIREMENTS_FILE not found. Skipping dependency installation."
fi

# Define the function to run ruff linting
run_linting() {
    local dir=$1
    echo "Running ruff linting on $dir..."
    ruff check "$ROOT_DIR/$dir" $FIX_OPTION
    
    if [ $? -eq 0 ]; then
        echo "Linting completed successfully for $dir."
    else
        echo "Linting failed for $dir. Please check the output above."
        exit 1
    fi
}

# Run linting based on the argument
if [ "$ARGUMENT" == "all" ]; then
    for dir in "${VALID_DIRECTORIES[@]}"; do
        run_linting "$dir"
    done
else
    run_linting "$ARGUMENT"
fi
