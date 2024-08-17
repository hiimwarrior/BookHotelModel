#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: $0 [DIRECTORY]"
    echo
    echo "This script sets up a virtual environment and runs tests for the specified directory."
    echo
    echo "Directories:"
    echo "  api                  Run tests for the api directory"
    echo "  data_engineering     Run tests for the data_engineering directory"
    echo "  data_science         Run tests for the data_science directory"
    echo
    echo "Options:"
    echo "  -h, --help           Show this help message and exit"
}

# Check if the required command is provided
if [ "$#" -ne 1 ]; then
    echo "Error: No directory specified."
    show_help
    exit 1
fi

# Define paths
BASE_DIR=$(dirname "$(realpath "$0")")/..
TARGET_DIR="$BASE_DIR/$1"
VENV_DIR="$TARGET_DIR/venv.test"
REQUIREMENTS_FILE="$TARGET_DIR/requirements-test.txt"

# Verify that the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory $TARGET_DIR does not exist."
    exit 1
fi

# Create and activate virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found in $TARGET_DIR. Creating one..."
    python -m venv "$VENV_DIR"
    echo "Virtual environment created."
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"
source "$VENV_DIR/Scripts/activate"  # Windows, uncomment if needed

# Install dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "$REQUIREMENTS_FILE not found. Skipping dependency installation."
fi

# Change to the base directory to run tests
cd "$TARGET_DIR" || { echo "Failed to change directory to $TARGET_DIR"; exit 1; }

# Run pytest in the base directory
echo "Running tests in the base directory..."
pytest

# Deactivate the virtual environment
deactivate
