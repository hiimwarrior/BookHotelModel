#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: $0 [VERSION] [DESTINATION]"
    echo
    echo "This script processes and populates data based on the specified transformation version."
    echo
    echo "VERSION options:"
    echo "  v1    Use the initial transformation script"
    echo
    echo "DESTINATION options:"
    echo "  csv   Save the processed data to a CSV file"
    echo "  db    Save the processed data to a MySQL database"
    echo
    exit 0
}

# Function to check and set up the virtual environment
setup_venv() {
    local venv_dir="data_engineering/venv"

    if [ ! -d "$venv_dir" ]; then
        echo "Virtual environment not found. Creating a new one..."
        python -m venv "$venv_dir"
    fi

    echo "Activating virtual environment..."
    source "$venv_dir/bin/activate"  # macOS/Linux
    source "$venv_dir/Scripts/activate"  # Windows, uncomment if needed

    echo "Installing dependencies..."
    pip install -r data_engineering/requirements.txt
}

# Function to process data based on the version
process_data() {
    local version=$1
    local destination=$2
    local script="data_engineering/src/transformations/process_bookings_data_${version}.py"

    # Check if the transformation script exists
    if [ ! -f "$script" ]; then
        echo "Transformation script '$script' not found!"
        exit 1
    fi

    # Execute the transformation script
    echo "Running transformation script '$script' with destination '$destination'..."
    python "$script" --destination "$destination"
}

# Default version and destination
DEFAULT_VERSION="1"
DEFAULT_DESTINATION="csv"

# Check if the required command is provided
if [ "$#" -gt 2 ]; then
    show_help
elif [ "$#" -eq 2 ]; then
    version="$1"
    destination="$2"
elif [ "$#" -eq 1 ]; then
    version="$1"
    destination="$DEFAULT_DESTINATION"
else
    version="$DEFAULT_VERSION"
    destination="$DEFAULT_DESTINATION"
fi

# Set up the virtual environment and install dependencies
setup_venv

# Call the process_data function with the provided or default version and destination
process_data "$version" "$destination"
