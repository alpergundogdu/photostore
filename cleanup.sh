#!/bin/bash
set -euo pipefail

echo "Sorting imports..."
find photostore/ -type f -name "*.py" | xargs poetry run isort

echo "Formatting scripts..."
find photostore/ -type f -name "*.py" | xargs poetry run autopep8 -i

# echo "Running tests..."
# poetry run python -m unittest discover -s tests -v

echo "Running pylint..."
poetry run pylint_runner --disable=C -v

