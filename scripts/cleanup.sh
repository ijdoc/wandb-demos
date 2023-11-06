#!/usr/bin/env bash

# Inser the header (should be a sibling of this script)
source $(dirname "$0")/header.sh
test_command_outcome "Import header file"

# Change to repo root
cd $(get_repo_root)
test_command_outcome "Go to repo root"

# Find all .py files and reformat them
pipenv clean
test_command_outcome "Clean dev pipenv environment"

# Find all .py files to reformat them
find . -type f -name '*.py' ! -path './*/wandb/*' ! -path './*/node_modules/*' ! -path './*/artifacts/*' -exec pipenv run black {} \;
test_command_outcome "Format python files"

# Find all .ipynb files to clean and reformat them
find . -type f -name '*.ipynb' ! -path './*/wandb/*' ! -path './*/node_modules/*' ! -path './*/artifacts/*' -print0 | xargs -0 -I {} pipenv run jupyter nbconvert --clear-output --inplace {}
test_command_outcome "Clear notebook outputs"
find . -type f -name '*.ipynb' ! -path './*/wandb/*' ! -path './*/node_modules/*' ! -path './*/artifacts/*' -print0 | xargs -0 -I {} pipenv run python scripts/format.py {}
test_command_outcome "Format notebooks"