# W&B Examples

## Requirements

- pipenv

## Setup the development environment

```shell
pipenv sync --dev
pipenv run pre-commit install
```

## Start jupyterlab

```shell
bash scripts/start.sh
```

## Authentication

The following command will list all running servers with authentication information

```shell
pipenv run jupyter server list
```