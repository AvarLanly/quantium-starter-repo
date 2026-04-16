#!/bin/bash

# Run the Pink Morsel Sales Visualiser test suite
# This script runs the test suite using the virtual environment's Python
# Can be integrated into CI/CD pipelines to automate testing

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define paths to virtual environment executables
# Uses the virtual environment's Python and pytest to ensure consistent environment
PYTHON_PATH="$SCRIPT_DIR/.venv/Scripts/python.exe"
PYTEST_PATH="$SCRIPT_DIR/.venv/Scripts/pytest.exe"

# Run the test suite with verbose output
echo "Running test suite..."
"$PYTEST_PATH" test_dash_app.py -v

# Capture the exit code from pytest
# Exit code 0 = all tests passed, non-zero = tests failed
EXIT_CODE=$?

# Print status message based on exit code
if [ $EXIT_CODE -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Tests failed!"
fi

# Return the exit code to the calling process
# This allows CI systems to detect test failures
exit $EXIT_CODE
