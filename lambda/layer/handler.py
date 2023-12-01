import argparse
import json
import os
import time
import random
import sys
import logging
import wandb

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log some helpful system info
logger.info(f"sys.path: {sys.path}")
logger.info(f"PYTHONPATH: {os.environ['PYTHONPATH']}")

wandb.require("nexus")
logger.info(f"Using wandb nexus")


def check_lambda(event, context):
    job_type = "local"

    if event != "" and context != "":
        logger.info(f"Event: {event}")
        logger.info(f"Context: {context}")
        job_type = "lambda"

    # Check W&B credentials
    if not "WANDB_API_KEY" in os.environ.keys():
        raise RuntimeError("WANDB_API_KEY environment key not defined")
    else:
        # Check if the key has the right length (should be 40 characters)
        key_length = 40
        logger.info(
            f'WANDB_API_KEY key has {len(os.environ["WANDB_API_KEY"])} characters'
        )
        assert (
            len(os.environ["WANDB_API_KEY"]) == key_length
        ), f"WANDB_API_KEY must be {key_length} characters long"

    logger.info(f"This is a {job_type} job")
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
        "'hello' - run a mock process that logs data to W&B ",
    )

    # Parse the arguments
    args = parser.parse_args()

    if args.function == "hello":
        hello("", "")
