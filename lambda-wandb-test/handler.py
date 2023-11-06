import json
import os
import time
import wandb
import random
import multiprocessing as mp


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
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def do_work(thread, job_type):
    run = wandb.init(
        config=dict(thread=thread, epochs=10),
        entity=os.environ["WANDB_ENTITY"],
        project=os.environ["WANDB_PROJECT"],
        job_type=job_type,
        group="multiprocess",
    )
    for i in range(run.config["epochs"]):
        i += random.random()
        run.log(dict(accuracy=(i * i)))
        time.sleep(1)
    run.finish()


def run_process(n):
    check_lambda("", "")
    do_work(n, "multiprocess")


def main(event, context):
    job_type = check_lambda(event, context)

    do_work(-1, job_type)

    return make_response(event)


def multiprocess(event, context):
    wandb.setup()
    pool = mp.Pool(processes=4)
    pool.map(run_process, range(4))

    return make_response(event)


if __name__ == "__main__":
    main("", "")
