#!/usr/bin/env bash

# TODO: Check the output of nvidia-smi and exit if error
pipenv run jupyter lab --ip=0.0.0.0 --no-browser --port 8888
