import json
import os
from datetime import datetime
import pandas as pd
from utils.logger import get_logger

logger = get_logger()

STATE_FILE = "data/metadata/pipeline_state.json"


def get_last_run_timestamp():
    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, "r") as f:
        state = json.load(f)

    return state.get("last_run_timestamp")


def update_last_run_timestamp():
    state = {
        "last_run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

    logger.info(f"Pipeline state updated: {state['last_run_timestamp']}")