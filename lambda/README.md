# AWS Lambda Implementation Examples for W&B

This directory includes the following examples:

| Directory                         | Description                       |
| -------------------------------- | ---------------------------------- |
| 📂 /[layer](./layer/)             | Fastest `nexus` (beta) implementation of `wandb` packaged in a lambda layer |
| 📂 /[full](./full/)               | `wandb` packaged with the lambda (slow & bulky)   |
| 📂 /[layer-pre-nexus](./layer-pre-nexus/) | `wandb<0.16.0` packaged in a lambda layer |
| 📄 README.md                      | This file                          |

## Requirements

All of the lambda examples here require the following tools:

- `pipenv`: to manage the python virtual environment (version 3.9) and its dependencies
- `node`: to manage the required serverless plugins (e.g., `serverless-python-requirements`)
- `docker`: to isolate the environment when collecting pip requirements
- `aws cli` (optional): to configure the AWS credentials for serverless to use

This lambda demo is setup using the [serverless framework](https://www.serverless.com/), which can be installed with:

```shell
npm install -g serverless
```
