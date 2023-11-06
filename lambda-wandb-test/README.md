# AWS Lambda Demo for W&B

## Requirements

- Python 3.9
- pipenv
- node

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

3. Setup your AWS credentials. If you need a sample permissions policy document, check the "How this project was created" section at the end of this README

4. Deploy the lambda functions with (repeat every time you make changes to the code):
    ```shell
    sls deploy
    ```

5. Execute a function and log the results (e.g.):
    ```shell
    sls invoke -f multipipe & sleep 2; sls logs -f multipipe -t &
    ```

## Local debugging

You can debug any of the included functions locally by executing the handler.py function directly from the pipenv shell (e.g.):
```shell
pipenv shell
python handler.py multipipe
```

You can also obtain information on all possible functions via:
```shell
pipenv shell
python handler.py -h
```

<details>
<summary>How this project was created</summary>

This project was created as follows:

1. Installed serverless framework with:
   ```
   npm install -g serverless
   ```
2. Created a serverless project from the repo root by running:
   ```shell
   sls create --template aws-python3 --path lambda-wandb-test
   ```

3. Created AWS user group with initial permissions created with the [serverless policy generator](https://open-sl.github.io/serverless-permission-generator/). Some required permissions were still missing:
    - `cloudformation:CreateChangeSet`
    - `cloudformation:ExecuteChangeSet`
    - `cloudformation:DeleteChangeSet`
    - `logs:TagResource`
    - `lambda:TagResource`

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
            "arn:aws:cloudformation:{region}:{account_id}:stack/{project_name}-{stage}/*"
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
            "arn:aws:s3:::{project_name}*serverlessdeploy*"
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
            "arn:aws:s3:::{project_name}*serverlessdeploy*"
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
            "arn:aws:lambda:{region}:{account_id}:function:{project_name}-{stage}-*"
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
            "arn:aws:logs:{region}:{account_id}:*"
          ],
          "Effect": "Allow"
        },
        {
          "Action": [
            "logs:PutLogEvents"
          ],
          "Resource": [
            "arn:aws:logs:{region}:{account_id}:*"
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
            "arn:aws:events:{region}:{account_id}:rule/{project_name}-{stage}-{region}"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "events:DescribeRule"
          ],
          "Resource": [
            "arn:aws:events:{region}:{account_id}:rule/{project_name}-{stage}-*"
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
            "arn:aws:iam::{account_id}:role/{project_name}-{stage}-{region}-lambdaRole"
          ]
        }
      ]
    }
    ```

4. Ran `sls remove && sls deploy` to debug policy permissions, until the stack was properly created

5. Added necessary `serverless` plugins using `npm`

</details>
