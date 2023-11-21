#!/usr/bin/env bash

# Inser the header (should be a sibling of this script)
source $(dirname "$0")/header.sh
test_command_outcome "Import header file"

cd $(get_repo_root)
pipenv clean
pipenv sync --dev
test_command_outcome "Clean root pipenv"

# Find all .py files to reformat them
find . -type f -name '*.py' ! -path './*/.wandb/*' ! -path './*/wandb/*' ! -path './*/node_modules/*' ! -path './*/artifacts/*' -exec pipenv run black {} \;
test_command_outcome "Format python files"

# Find all .ipynb files to clean and reformat them
find . -type f -name '*.ipynb' ! -path './*/.virtual_documents/*' ! -path './*/.wandb/*' ! -path './*/.ipynb_checkpoints/*' ! -path './*/wandb/*' ! -path './*/node_modules/*' ! -path './*/artifacts/*' -print0 | xargs -0 -I {} pipenv run jupyter nbconvert --clear-output --inplace {}
test_command_outcome "Clear notebook outputs"
find . -type f -name '*.ipynb' ! -path './*/.virtual_documents/*' ! -path './*/.wandb/*' ! -path './*/.ipynb_checkpoints/*' ! -path './*/wandb/*' ! -path './*/node_modules/*' ! -path './*/artifacts/*' -print0 | xargs -0 -I {} pipenv run python scripts/format.py {}
test_command_outcome "Format notebooks"
