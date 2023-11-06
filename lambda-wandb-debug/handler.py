import argparse
import json
import os
import time
import wandb
import random
import multiprocessing as mp
from multiprocessing import Pipe, Process


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


def do_work(id, job_type, group, connection=None):
    run = wandb.init(
        config=dict(thread_id=id, epochs=10),
        entity=os.environ["WANDB_ENTITY"],
        project=os.environ["WANDB_PROJECT"],
        job_type=job_type,
        group=group,
    )
    for i in range(run.config["epochs"]):
        i += random.random()
        # Mock up variable length step
        time.sleep(1.0 + random.random())
        run.log(dict(accuracy=(i * i) / 100))

    run.finish()
    if connection:
        # Let the parent process know we are done!
        connection.send([None])


def run_process(id):
    check_lambda("", "")
    do_work(id, None, "multipool")


def single(event, context):
    job_type = check_lambda(event, context)

    do_work(-1, job_type, "single")

    return make_response(event)


def multipool(event, context):
    wandb.setup()
    _pool = mp.Pool(processes=4)
    _pool.map(run_process, range(4))

    return make_response(event)


def multipipe(event, context):
    job_type = check_lambda(event, context)

    wandb.setup()

    # Get number of available logical cores
    plimit = mp.cpu_count()
    print(f"This environment has {plimit} logical cores")

    # Setup management variables
    results = []
    parent_conns = []
    processes = []
    pcount = 0
    pactive = []
    i = 0

    for id in range(4):
        # Create the pipe for parent-child process communication
        parent_conn, child_conn = Pipe()
        # create the process, pass item to be operated on and connection
        process = Process(
            target=do_work,
            args=(
                id,
                job_type,
                "multipipe",
                child_conn,
            ),
        )
        parent_conns.append(parent_conn)
        process.start()
        pcount += 1

        if pcount == plimit:  # There is not currently room for another process
            # Wait until there are results in the Pipes
            finishedConns = mp.connection.wait(parent_conns)
            # Collect the results and remove the connection as processing
            # the connection again will lead to errors
            for conn in finishedConns:
                results.append(conn.recv()[0])
                parent_conns.remove(conn)
                # Decrement pcount so we can add a new process
                pcount -= 1

    # Ensure all remaining active processes have their results collected
    for conn in parent_conns:
        results.append(conn.recv()[0])
        conn.close()

    return make_response(event)


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="A demo lambda handler function definition."
    )

    # Add the 'function' argument
    parser.add_argument(
        "function",
        choices=["single", "multipipe", "multipool"],
        type=str,
        help="The demo function to invoke. Choices are: "
        "'single' - a standard single-thread process; "
        "'multipipe' - a multi-threaded execution based on process pipes; "
        "'multipool' - a multi-threaded execution based on a process pool",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Now you can use args.function as the string argument in your script
    print(f"The 'function' argument was passed in with the value: {args.function}")
    if args.function == "single":
        single("", "")
    if args.function == "multipipe":
        multipipe("", "")
    if args.function == "multipool":
        multipool("", "")
