
# **DupeHunter Documentation**

This document provides an overview of the DupeHunter project. It is intended for developers contributing to the codebase and for end users looking to run the CLI tool.

---

## **Purpose**

The `cli.py` module serves as the entry point for the DupeHunter command-line interface (CLI). It allows users to execute the deduplication workflow by specifying directories for scanning, a database for metadata storage, and logging preferences.

---

## **Features**

- Parses user-provided arguments for:
  - **Base Path**: The directory to scan for image files.
  - **Target Path**: The directory to store deduplicated files.
  - **Database Path**: SQLite database file to store file metadata.
  - **Logging Level**: Logging verbosity (e.g., DEBUG, INFO).
- Configures logging to ensure consistent output across the application.
- Orchestrates the deduplication workflow by calling the `main` function from `core.py`.
- Handles errors gracefully and provides informative logs.

---

## **For Contributors**

### **Development Setup**

1. **Install Poetry**:
   Ensure you have Poetry installed to manage dependencies and the project environment.
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Clone the Repository**:
   Clone the DupeHunter repository from GitHub:
   ```bash
   git clone https://github.com/frecke/dupehunter.git
   cd dupehunter
   ```

3. **Install Dependencies**:
   Use Poetry to install project and development dependencies.
   ```bash
   poetry install
   ```

4. **Activate the Virtual Environment**:
   Activate the Poetry-managed environment for development.
   ```bash
   poetry shell
   ```

5. **Pre-commit Hooks**:
   Install pre-commit hooks to enforce code style and static checks.
   ```bash
   pre-commit install
   ```

### **Code Style and Linting**

- **Black**: Automatically formats Python code.
  ```bash
  black .
  ```
- **Flake8**: Lints Python code to ensure it meets PEP 8 standards.
  ```bash
  flake8 .
  ```
- **Mypy**: Performs static type checking.
  ```bash
  mypy .
  ```
- **isort**: Organizes imports in Python files.
  ```bash
  isort .
  ```

### **Testing**

1. **Run Tests**:
   Use `pytest` to execute tests and check code coverage.
   ```bash
   pytest --cov=dupehunter --cov-report=term-missing
   ```

2. **Run Tests in Parallel**:
   Speed up tests using `pytest-xdist`.
   ```bash
   pytest -n auto
   ```

### **Directory Structure**

```
dupehunter/
├── cli.py                 # Command-line interface module
├── core.py                # Core orchestration logic
├── database.py            # Database interaction logic
├── files.py               # File-related utilities
├── processing.py          # File processing and traversal
├── catalog.py             # Duplicate detection and catalog utilities
├── utils.py               # General-purpose helper functions
├── tests/                 # Unit and integration tests
└── pyproject.toml         # Project configuration
```

---

### **How to Contribute**

1. **Fork the Repository**:
   Create a fork of the repository on GitHub.

2. **Create a Feature Branch**:
   Work on new features or bug fixes in a dedicated branch.
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Changes**:
   Follow best practices for commit messages.
   ```bash
   git commit -m "Add feature: description of your feature"
   ```

4. **Run Pre-commit Hooks**:
   Ensure code style and linting checks pass before pushing.
   ```bash
   pre-commit run --all-files
   ```

5. **Push Changes and Open a Pull Request**:
   Push your branch and open a pull request to the `main` branch.

### **Contribution Guidelines**

- Write tests for all new features or bug fixes.
- Ensure all tests pass and maintain high code coverage.
- Adhere to PEP 8 standards and use `black` for formatting.
- Document all new functionality clearly.

---

### **dupehunter.cli Module Overview**

### `parse_arguments`
Parses command-line arguments using `argparse`. Ensures all required arguments are provided and validates optional arguments like the logging level.

**Arguments:**
- `--base-path`: Required; directory to scan for images (type: `Path`).
- `--target-path`: Required; directory to store deduplicated files (type: `Path`).
- `--db-path`: Optional; SQLite database path (default: `file_catalog.db`, type: `Path`).
- `--log-level`: Optional; logging level (default: `INFO`, choices: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

### `configure_logging`
Configures logging using the specified logging level.

**Parameters:**
- `log_level (str)`: The logging level to configure.

### `cli_entry_point`
The main entry point for the CLI. Combines argument parsing, logging configuration, and workflow orchestration.

**Workflow:**
1. Parses arguments with `parse_arguments()`.
2. Configures logging using `configure_logging()`.
3. Calls the `main` function from `core.py` with parsed arguments.

### **How It Works**

1. User invokes the CLI with required and optional arguments.
2. The module validates and parses these arguments.
3. Logging is configured based on the user-specified level.
4. The deduplication workflow is executed, and results (e.g., files to copy, delete candidates) are written to specified locations.

---

## **For End Users**

### **Usage**

Run the CLI tool using the following command:

```bash
python -m dupehunter.cli --base-path <directory_to_scan> --target-path <output_directory>
```

### **Options**

| Option                  | Description                                           | Default                  |
|-------------------------|-------------------------------------------------------|--------------------------|
| `--base-path`           | Directory to scan for images (required).             | None                     |
| `--target-path`         | Directory to store deduplicated files (required).    | None                     |
| `--db-path`             | Path to the SQLite database.                         | `file_catalog.db`        |
| `--log-level`           | Logging verbosity (`DEBUG`, `INFO`, etc.).           | `INFO`                   |

### **Examples**

#### Basic Example
```bash
python -m dupehunter.cli --base-path /images --target-path /output
```

#### Custom Database Path
```bash
python -m dupehunter.cli --base-path /images --target-path /output --db-path /data/catalog.db
```

#### Adjust Logging Level
```bash
python -m dupehunter.cli --base-path /images --target-path /output --log-level DEBUG
```

---

## **Development Notes**

### **Testing**
- Tests for this module are located in `tests/test_cli.py`.
- Run tests using:
  ```bash
  pytest --cov=dupehunter.cli
  ```

### **Mocking and Isolation**
- Tests use `pytest-mock` to mock external dependencies like `core.main`.
- Argument parsing is tested with patched `sys.argv` to simulate command-line input.

### **Future Improvements**
- Add support for additional file formats or metadata extraction options via CLI flags.
- Implement dry-run functionality to preview results without making changes.

---

## **Common Issues**

### **Missing Required Arguments**
If a required argument like `--base-path` or `--target-path` is missing, the program will exit with an error. Ensure all required arguments are provided.

### **Invalid Logging Level**
Providing an unsupported logging level (e.g., `INVALID`) will result in an error. Use one of the supported levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.

---

## **Contact**
For questions or contributions, contact the project maintainers or refer to the project repository.
