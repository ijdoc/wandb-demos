import argparse
import json
import os
import time
import random
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_lambda(event, context):
    job_type = "local"

    if event != "" and context != "":
        print(f"Event: {event}")
        print(f"Context: {context}")
        job_type = "lambda"

    # Check W&B credentials
    if not "WANDB_API_KEY" in os.environ.keys():
        raise RuntimeError("WANDB_API_KEY environment key not defined")
    # else:
    #     # Check if the key has the right length (should be 40 characters)
    #     print(f'API key has {len(os.environ["WANDB_API_KEY"])} characters')

    return job_type


def make_response(event):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Your function executed successfully!",
                "input": event,
            }
        ),
    }

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Your function executed successfully!",
        "event": event
    }
    """


def hello(event, context):
    job_type = check_lambda(event, context)

    logger.info("Python Path: {}".format(sys.path))
    # Try to import wandb and log if it's successful or not
    try:
        import wandb

        logger.info("Successfully imported wandb.")
    except ImportError as e:
        logger.error("Error importing wandb: {}".format(e))
    logger.info("PYTHONPATH: {}".format(os.environ["PYTHONPATH"]))

    # return {
    #     'statusCode': 200,
    #     'body': {"sys.executable": sys.executable,
    #              "job_type": job_type,
    #              "WANDB__EXECUTABLE": os.environ["WANDB__EXECUTABLE"],
    #              "wandb":dir(wandb)}
    # }

    run = wandb.init(
        config={"epochs": 10},
        entity=os.environ["WANDB_ENTITY"],
        project=os.environ["WANDB_PROJECT"],
        job_type=job_type,
    )
    for i in range(run.config["epochs"]):
        i += random.random()
        # Mock up variable length step
        time.sleep(1.0 + random.random())
        run.log(dict(accuracy=(i * i) / 100))

    run.finish()
    return make_response(event)


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="A demo lambda handler function definition."
    )
    parser.add_argument(
        "function",
        choices=["hello"],
        type=str,
        help="The demo function to invoke. Choices are: "
        "'hello' - run a mock process logging data to W&B ",
    )

    # Parse the arguments
    args = parser.parse_args()

    if args.function == "hello":
        hello("", "")
