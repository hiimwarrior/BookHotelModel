# CLI Script Documentation

## Overview

This CLI script is designed to manage various tasks related to DVC pipelines, database setups, data initialization, linting, and testing. The script provides commands for initializing DVC pipelines, setting up database containers, processing and populating data, linting code, and running tests.

## Commands

### `dvc-init-pipeline`

- **Description**: Initializes DVC, sets up the virtual environment, and runs the DVC pipeline.
- **Usage**: `./cli_script.sh dvc-init-pipeline [OPTIONS]`

### `setup-db [ENV]`

- **Description**: Sets up and starts the database containers for the specified environment (`prod`, `local`, or `test`).
- **Usage**: `./cli_script.sh setup-db [ENV]`
- **Options**:
  - `prod` - Set up production database
  - `local` - Set up local database
  - `test` - Set up test database

### `initialize-data [VERSION] [DESTINATION]`

- **Description**: Processes and populates data based on the specified transformation version and destination (`csv` or `db`).
- **Usage**: `./cli_script.sh initialize-data [VERSION] [DESTINATION]`
- **Options**:
  - `VERSION` - Specify the version of the transformation (default: `1`)
  - `DESTINATION` - Specify the destination for the processed data (`csv` or `db`, default: `db`)

### `lint [DIRECTORY]`

- **Description**: Runs linting checks using `ruff` on the specified directory (`api`, `data_science`, `data_engineering`, or `all`).
- **Usage**: `./cli_script.sh lint [DIRECTORY]`
- **Options**:
  - `api` - Lint the `api` directory
  - `data_science` - Lint the `data_science` directory
  - `data_engineering` - Lint the `data_engineering` directory
  - `all` - Lint all specified directories

### `test [DIRECTORY]`

- **Description**: Runs tests in the specified directory (`api`, `data_engineering`, or `data_science`).
- **Usage**: `./cli_script.sh test [DIRECTORY]`
- **Options**:
  - `api` - Run tests in the `api` directory
  - `data_engineering` - Run tests in the `data_engineering` directory
  - `data_science` - Run tests in the `data_science` directory

## Options

- `-h, --help` - Show the help message and exit.

## Installation and Usage

### Prerequisites

- **Python**: Ensure Python 3 is installed.
- **Virtual Environment**: The script uses virtual environments for managing dependencies.
- **Ruff**: For linting.
- **Database**: Ensure Docker is installed and configured if you are using database-related commands.
