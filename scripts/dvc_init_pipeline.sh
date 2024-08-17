#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "This script initializes DVC, sets up a virtual environment, adds files to Git, and reproduces the DVC pipeline."
    echo
    echo "Options:"
    echo "  -h, --help              Show this help message and exit"
    echo "  --skip-dvc-init         Skip DVC initialization"
    echo "  --skip-git-commit       Skip Git commit of DVC files"
    echo "  --skip-venv             Skip virtual environment setup"
    exit 0
}

# Function to check and install DVC
install_dvc() {
    if ! command -v dvc &> /dev/null; then
        echo "DVC not found. Installing DVC..."
        pip install dvc
    fi
}

# Function to set up the virtual environment
setup_venv() {
    # Define the path for the virtual environment
    venv_path="data_engineering/venv"
    
    # Create the virtual environment if it doesn't exist
    if [ ! -d "$venv_path" ]; then
        echo "Creating virtual environment in '$venv_path'..."
        python -m venv "$venv_path"
    fi

    # Activate the virtual environment
    echo "Activating virtual environment..."
    source "$venv_path/bin/activate"
    source "$venv_path/Scripts/activate"  # Windows, uncomment if needed

    # Install required packages
    requirements_file="data_engineering/requirements.txt"
    if [ -f "$requirements_file" ]; then
        echo "Installing required packages..."
        pip install -r "$requirements_file"
    else
        echo "requirements.txt not found in 'data_engineering'!"
        exit 1
    fi
}

# Parse command-line arguments
skip_dvc_init=false
skip_git_commit=false
skip_venv=false

while [[ "$1" != "" ]]; do
    case $1 in
        -h | --help )          show_help
                              ;;
        --skip-dvc-init )      skip_dvc_init=true
                              ;;
        --skip-git-commit )    skip_git_commit=true
                              ;;
        --skip-venv )          skip_venv=true
                              ;;
        * )                    echo "Invalid option: $1" >&2
                              show_help
                              ;;
    esac
    shift
done

# Ensure we're in the root directory of the project
cd "$(dirname "$0")/.."

# Set up virtual environment if not skipped
if [ "$skip_venv" = false ]; then
    setup_venv
fi

# Ensure DVC is installed
install_dvc

# Check if DVC is initialized
if [ ! -d ".dvc" ]; then
    if [ "$skip_dvc_init" = false ]; then
        echo "Initializing DVC..."
        dvc init
    else
        echo "DVC is not initialized. Please initialize DVC before running the pipeline."
        exit 1
    fi
fi

# Add the dvc.yaml file and DVC configuration to Git, unless skipped
if [ "$skip_git_commit" = false ]; then
    if [ -f "dvc.yaml" ] && [ -d ".dvc" ]; then
        echo "Adding files to git..."
        git add dvc.yaml .dvc/config .dvc/.gitignore
        git commit -m "Add DVC pipeline for data download"
    else
        echo "Files to commit not found. Ensure dvc.yaml and DVC configuration exist."
        exit 1
    fi
fi

# Execute the DVC pipeline
echo "Reproducing DVC pipeline..."
dvc repro
