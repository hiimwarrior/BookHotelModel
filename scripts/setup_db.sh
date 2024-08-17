#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: $0 [ENVIRONMENT]"
    echo
    echo "This script sets up and starts the database containers for the specified environment."
    echo
    echo "Environment options:"
    echo "  prod    Use the production environment configuration"
    echo "  local   Use the local environment configuration"
    echo "  test    Use the test environment configuration"
    echo
    exit 0
}

# Function to print a progress message
print_step() {
    echo "==> $1"
}

# Function to set up the database environment
setup_db() {
    local env_file
    local compose_file
    local volume_dir

    case "$1" in
        prod)
            env_file="infra/db/.env"
            compose_file="infra/db/docker-compose.yml"
            volume_dir="infra/volumes/db/prod"
            ;;
        local)
            env_file="infra/db/.env.local"
            compose_file="infra/db/docker-compose.local.yml"
            volume_dir="infra/volumes/db/local"
            ;;
        test)
            env_file="infra/db/.env.test"
            compose_file="infra/db/docker-compose.test.yml"
            volume_dir="infra/volumes/db/test"
            ;;
        *)
            echo "Invalid environment: $1"
            show_help
            ;;
    esac

    # Print step
    print_step "Checking environment file..."

    # Check if the environment file exists
    if [ ! -f "$env_file" ]; then
        echo "Environment file '$env_file' not found!"
        exit 1
    fi

    # Print step
    print_step "Exporting environment variables..."

    # Export environment variables
    export $(grep -v '^#' "$env_file" | xargs)

    # Print step
    print_step "Checking Docker Compose file..."

    # Check if Docker Compose file exists
    if [ ! -f "$compose_file" ]; then
        echo "Docker Compose file '$compose_file' not found!"
        exit 1
    fi

    # Print step
    print_step "Creating volume directory if it doesn't exist..."

    # Create the volume directory if it doesn't exist
    if [ ! -d "$volume_dir" ]; then
        mkdir -p "$volume_dir"
        echo "Created volume directory '$volume_dir'."
    else
        echo "Volume directory '$volume_dir' already exists."
    fi

    # Print step
    print_step "Starting database using '$compose_file'..."

    # Run Docker Compose to set up the database
    docker-compose -f "$compose_file" up -d

    # Print step
    print_step "Database setup completed."

    # Print step
    print_step "Displaying Docker logs for the database setup..."

    # Show Docker logs temporarily
    docker-compose -f "$compose_file" logs --tail=100
}

# Parse command-line arguments
if [ "$#" -ne 1 ]; then
    show_help
fi

# Call the setup_db function with the provided argument
setup_db "$1"
