import argparse
import asyncio
import datetime
import json
import pathlib
import pprint
import random
import traceback
import uuid

import pandas as pd
import tqdm
from deeppavlov_agent.setup_agent import setup_agent

random.seed(315)


async def dataset_processor(register_msg, args):
    response = await register_msg(
        utterance=json.dumps(instance),
        user_external_id=str(uuid.uuid4()),
        user_device_type="cmd",
        location="lab",
        channel_type="cmd_client",
        deadline_timestamp=None,
        require_response=True,
    )
    response = json.loads(response["dialog"].utterances[-1].text)


def run_cmd(args):
    agent, session, workers = setup_agent(pipeline_configs=args.pipeline_configs)
    loop = asyncio.get_event_loop()
    loop.set_debug(args.debug)
    future = asyncio.ensure_future(dataset_processor(agent.register_msg, args))
    for i in workers:
        loop.create_task(i.call_service(agent.process))
    try:
        loop.run_until_complete(future)
    except KeyboardInterrupt:
        pass
    except Exception:
        print(traceback.format_exc())
    finally:
        future.cancel()
        if session:
            loop.run_until_complete(session.close())
        loop.stop()
        loop.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-pl",
        "--pipeline_configs",
        help="Pipeline config (overwrite value, defined in settings)",
        type=str,
        action="append",
    )
    parser.add_argument(
        "--report_dir",
        help="A report path",
        type=pathlib.Path,
        default=pathlib.Path(f"/data/services/agent/reports/{datetime.datetime.now().strftime('%Y-%m-%d%T%H:%M:%S')}"),
    )
    parser.add_argument("-d", "--debug", help="Run in debug mode", action="store_true")
    parser.add_argument("-r", "--restore", help="Restore an interrupted run", action="store_true")
    parser.add_argument(
        "--out_data_dir",
        help="A dir path to store resulted file",
        type=pathlib.Path,
        default=None,
    )
    # Options for handle one file
    parser.add_argument(
        "--in_data_file",
        help="A file path",
        type=pathlib.Path,
        default=None,
    )
    # Options for handle datasets
    parser.add_argument(
        "-i",
        "--in_dataset_paths",
        help="A dataset path",
        type=pathlib.Path,
        default=[],
        action="append",
    )
    parser.add_argument("-n", "--n_samples", help="Number of sampled instances", type=int, default=0)
    parser.add_argument(
        "-s",
        "--data_selectors",
        help="Use it to select data by the presence mask in the file path.\n" "example: run -s neznaika -s test -s eng",
        action="append",
        default=[],
    )
    args = parser.parse_args()

    run_cmd(args)
