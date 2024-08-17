#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTION]"
    echo
    echo "This script sets up the virtual environment, installs dependencies, and starts the MLflow UI."
    echo
    echo "OPTIONS:"
    echo "  -h, --help         Show this help message and exit"
    echo
    exit 0
}

# Function to check and set up the virtual environment
setup_venv() {
    local venv_dir="data_science/venv"

    if [ ! -d "$venv_dir" ]; then
        echo "Virtual environment not found. Creating a new one..."
        python -m venv "$venv_dir"
    fi

    echo "Activating virtual environment..."
    source "$venv_dir/bin/activate"  # macOS/Linux
    source "$venv_dir/Scripts/activate"  # Windows, uncomment if needed

    echo "Installing dependencies..."
    pip install -r data_science/requirements.txt
}

# Function to start MLflow UI
start_mlflow_ui() {
    local mlruns_dir="data_science/mlruns"
    
    # Ensure the directory exists
    if [ ! -d "$mlruns_dir" ]; then
        echo "MLflow tracking directory not found. Creating a new one..."
        mkdir -p "$mlruns_dir"
    fi

    # Set the MLFLOW_TRACKING_URI environment variable
    export MLFLOW_TRACKING_URI="file://$(pwd)/data_science/mlruns"

    echo "Starting MLflow UI..."
    cd data_science  # Change to the directory containing mlruns
    echo "The MLflow UI will be accessible at http://localhost:5000"
    mlflow ui --port 5000
}

# Check for help option
if [ "$#" -gt 0 ]; then
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        show_help
    else
        echo "Error: Invalid option '$1'. Use '-h' or '--help' for usage information."
        exit 1
    fi
fi

# Set up the virtual environment and install dependencies
setup_venv

# Start the MLflow UI
start_mlflow_ui