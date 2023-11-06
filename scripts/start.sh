#!/usr/bin/env bash

# TODO: Check the output of nvidia-smi and exit if error
pipenv sync --dev
pipenv run jupyter labextension install @yudai-nkt/jupyterlab_city-lights-theme
pipenv run jupyter lab build
pipenv run jupyter lab --ip=0.0.0.0 --no-browser --port 8888
