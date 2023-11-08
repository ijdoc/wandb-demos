# AWS Lambda Layer implementation for W&B Nexus

Additional inormation on Nexus available [here](https://github.com/wandb/wandb/blob/main/nexus/README.md#installation) 

## Requirements

- pipenv: to manage python (version 3.10) and dependencies
- node: to manage serverless plugins (e.g., `serverless-python-requirements`)
- docker: to isolate environment when collecting pip requirements
- aws cli: to setup AWS credentials for serverless to use

This lambda demo is setup using the [serverless framework](https://www.serverless.com/), which can be installed with:

```
npm install -g serverless
```

## Getting Started

1. Create a `.env` file with the following contents:
    ```
    WANDB_API_KEY="your-api-key"
    WANDB_ENTITY="your-entity"
    WANDB_PROJECT="your-project"
    ```

2. Sync `npm` and `pipenv` dependencies
    ```shell
    npm install
    pipenv sync --dev
    ```

3. Setup AWS user and credentials for serverless.
    - While debugging, you can create a debugging AWS user with admin priviledges (not recommended for production) and setup its credentials by running `aws configure`
    - When ready to deploy, remove admin permissions for your user and instead create a user group with the permissions included in the "Policy Permissions" section below.

4. Log into the pipenv shell
    ```shell
    pipenv shell
    ```

5. Deploy the lambda function (repeat every time the code changes):
    ```shell
    sls deploy
    ```

6. Execute the function and return the log:
    ```shell
    sls invoke -f hello -l
    ```

## Local debugging

You can debug the function locally by executing the handler.py function directly from the pipenv shell (e.g.):
```shell
pipenv shell
python handler.py hello
```

<details>
<summary>Policy Permissions</summary>

These permissions apply to a single serverless lambda stack. Replace `{account_id}` accordingly.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:List*",
        "cloudformation:Get*",
        "cloudformation:ValidateTemplate"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:CreateUploadBucket",
        "cloudformation:CreateChangeSet",
        "cloudformation:ExecuteChangeSet",
        "cloudformation:DeleteChangeSet",
        "cloudformation:DeleteStack",
        "cloudformation:Describe*",
        "cloudformation:UpdateStack"
      ],
      "Resource": [
        "arn:aws:cloudformation:*:{account_id}:stack/lambda-wandb*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:CreateBucket",
        "s3:DeleteBucket",
        "s3:ListBucket",
        "s3:GetBucketPolicy",
        "s3:PutBucketPolicy",
        "s3:ListBucketVersions",
        "s3:PutAccelerateConfiguration",
        "s3:GetEncryptionConfiguration",
        "s3:PutEncryptionConfiguration",
        "s3:DeleteBucketPolicy"
      ],
      "Resource": [
        "arn:aws:s3:::lambda-wandb*serverlessdeploy*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::lambda-wandb*serverlessdeploy*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "lambda:Get*",
        "lambda:List*",
        "lambda:CreateFunction"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "lambda:AddPermission",
        "lambda:CreateAlias",
        "lambda:TagResource",
        "lambda:DeleteFunction",
        "lambda:InvokeFunction",
        "lambda:PublishVersion",
        "lambda:RemovePermission",
        "lambda:Update*"
      ],
      "Resource": [
        "arn:aws:lambda:*:{account_id}:function:lambda-wandb*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:DeleteLogGroup",
        "logs:TagResource"
      ],
      "Resource": [
        "arn:aws:logs:*:{account_id}:*"
      ],
      "Effect": "Allow"
    },
    {
      "Action": [
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:*:{account_id}:*"
      ],
      "Effect": "Allow"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:DescribeLogStreams",
        "logs:DescribeLogGroups",
        "logs:FilterLogEvents"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "events:Put*",
        "events:Remove*",
        "events:Delete*"
      ],
      "Resource": [
        "arn:aws:events:*:{account_id}:rule/lambda-wandb*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "events:DescribeRule"
      ],
      "Resource": [
        "arn:aws:events:*:{account_id}:rule/lambda-wandb*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:PassRole"
      ],
      "Resource": [
        "arn:aws:iam::{account_id}:role/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:GetRole",
        "iam:CreateRole",
        "iam:PutRolePolicy",
        "iam:DeleteRolePolicy",
        "iam:DeleteRole"
      ],
      "Resource": [
        "arn:aws:iam::{account_id}:role/lambda-wandb*-lambdaRole"
      ]
    }
  ]
}
```
