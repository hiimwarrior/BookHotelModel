#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "This CLI script allows you to manage DVC pipelines, database setups, data initialization, linting, and testing."
    echo
    echo "Commands:"
    echo "  dvc-init-pipeline      Initialize DVC, set up virtual environment, and run the pipeline"
    echo "  setup-db [ENV]         Set up and start the database containers for the specified environment (prod, local, test)"
    echo "  initialize-data [VERSION] [DESTINATION]    Process and populate data based on the specified transformation version and destination"
    echo "  lint [DIRECTORY]       Run linting checks using ruff on the specified directory (api, data_science, data_engineering or all directories)"
    echo "  test [DIRECTORY]       Run tests in the specified directory (api, data_engineering, data_science)"
    echo "  start-mlflow-ui        Start the MLflow UI server"
    echo "  start-notebook [ds|de]         Start a Jupyter Notebook in the specified directory (data_science or data_engineering)."
    echo
    echo "Options:"
    echo "  -h, --help             Show this help message and exit"
}

# Function to check and activate the virtual environment
activate_venv() {
    if [ ! -d "venv" ]; then
        echo "Virtual environment not found. Creating it..."
        python3 -m venv venv
        echo "Virtual environment created."
    fi

    # Activate the virtual environment
    source venv/bin/activate

    # Install dependencies
    if [ -f "scripts/requirements.txt" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip install -r scripts/requirements.txt
    fi
}

# Function to check and activate the test virtual environment
activate_test_venv() {
    if [ ! -d "venv.test" ]; then
        echo "Test virtual environment not found. Creating it..."
        python3 -m venv venv.test
        echo "Test virtual environment created."
    fi

    # Activate the virtual environment
    source venv.test/bin/activate

    # Install test dependencies
    if [ -f "api/deployment/requirements-test.txt" ] && [ "$1" == "api" ]; then
        echo "Installing test dependencies for api from requirements-test.txt..."
        pip install -r api/deployment/requirements-test.txt
    elif [ -f "requirements-test.txt" ]; then
        echo "Installing test dependencies from requirements-test.txt..."
        pip install -r requirements-test.txt
    else
        echo "requirements-test.txt not found. Skipping dependency installation."
    fi
}

# Function to start MLflow UI
start_mlflow_ui() {
    echo "Starting MLflow UI..."
    ./scripts/start_mlflow_ui.sh "$@"
}

# Check if the required command is provided
if [ "$#" -lt 1 ]; then
    echo "Error: No command provided."
    show_help
    exit 1
fi

# Command handling
case $1 in
    dvc-init-pipeline)
        shift
        # Call the dvc_init_pipeline.sh script with any additional arguments
        ./scripts/dvc_init_pipeline.sh "$@"
        ;;
    setup-db)
        shift
        # Call the setup_db.sh script with the environment parameter
        if [ "$#" -ne 1 ]; then
            echo "Error: 'setup-db' command requires exactly one argument (prod, local, or test)."
            show_help
            exit 1
        fi
        ./scripts/setup_db.sh "$1"
        ;;
    initialize-data)
        shift
        # Call the initialize_data.sh script with version and destination parameters
        if [ "$#" -gt 2 ]; then
            echo "Error: 'initialize-data' command accepts at most two arguments (VERSION and DESTINATION)."
            show_help
            exit 1
        fi
        version="${1:-1}"
        destination="${2:-db}"
        ./scripts/initialize_data.sh "$version" "$destination"
        ;;
    lint)
        shift
        # Ensure the virtual environment is activated and dependencies are installed
        activate_venv
        
        # Check if a directory argument is provided
        if [ "$#" -ne 1 ]; then
            echo "Error: 'lint' command requires exactly one argument specifying the directory to lint (api, data_science, or data_engineering)."
            show_help
            exit 1
        fi

        directory=$1

        # Validate the directory argument
        if [[ "$directory" != "api" && "$directory" != "data_science" && "$directory" != "data_engineering" && "$directory" != "all" ]]; then
            echo "Error: Invalid directory '$directory'. Valid options are 'api', 'data_science', 'data_engineering', or 'all'."
            show_help
            exit 1
        fi

        # Run ruff linting on the specified directory
        if [ "$directory" == "all" ]; then
            for dir in api data_science data_engineering; do
                echo "Running linting on $dir..."
                ruff check "$dir" --config .ruff.toml
                if [ $? -ne 0 ]; then
                    echo "Linting failed for $dir. Please check the output above."
                    exit 1
                fi
            done
        else
            echo "Running linting on $directory..."
            ruff check "$directory" --config .ruff.toml
            if [ $? -ne 0 ]; then
                echo "Linting failed for $directory. Please check the output above."
                exit 1
            fi
        fi

        echo "Linting completed successfully for $directory."
        ;;
    test)
        shift
        # Ensure the test virtual environment is activated and dependencies are installed
        if [ "$#" -ne 1 ]; then
            echo "Error: 'test' command requires exactly one argument specifying the directory to test (api, data_engineering, or data_science)."
            show_help
            exit 1
        fi

        directory=$1
        # Validate the directory argument
        if [[ "$directory" != "api" && "$directory" != "data_engineering" && "$directory" != "data_science" ]]; then
            echo "Error: Invalid directory '$directory'. Valid options are 'api', 'data_engineering', or 'data_science'."
            show_help
            exit 1
        fi

        # Activate the virtual environment and install test dependencies
        activate_test_venv "$directory"
        
        # Run tests in the specified directory
        echo "Running tests in $directory..."
        ./scripts/test.sh "$directory"
        if [ $? -ne 0 ]; then
            echo "Tests failed for $directory. Please check the output above."
            exit 1
        fi

        echo "Tests completed successfully for $directory."
        ;;
    start-mlflow-ui)
        start_mlflow_ui
        ;;
    -h|--help)
        show_help
        ;;
    start-notebook)
        echo "Starting Jupyter Notebook..."
        if [ $# -ne 2 ]; then
            echo "Error: start-notebook requires exactly one argument ('ds' for data_science or 'de' for data_engineering)."
            exit 1
        fi
        ./scripts/start_notebook.sh "$2"
        ;;
    *)
        echo "Error: Invalid command '$1'."
        show_help
        exit 1
        ;;
esac
