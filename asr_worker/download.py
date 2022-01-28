import dramatiq
from dramatiq.middleware import CurrentMessage
import logging
from pathlib import Path
import requests
import shutil
import subprocess
# import time
import os

from app.services.dramatiq import init_dramatiq
from app.core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

init_dramatiq()

dir_path = os.path.dirname(os.path.realpath(__file__))


@dramatiq.actor(store_results=True)
def download_url(url, asr_model_label):

    logger.debug(f"Decoding with model {asr_model_label}")

    message_id = CurrentMessage.get_current_message().message_id

    local_filename = url.split('/')[-1]

    filename, _ = os.path.splitext(local_filename)

    with requests.get(settings.BASE_URL + url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    output_directory = os.path.join(
        settings.WORKER_OUTPUT_DIRECTORY,
        filename)

    Path(output_directory).mkdir(parents=True, exist_ok=True)

    logger.debug(f"Decoding output {output_directory}")

    p = subprocess.Popen([
        settings.WORKER_DOCKER_COMMAND,
        local_filename,
        output_directory],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        close_fds=True)

    output = p.stdout.read()
    logger.debug(output)

    p.terminate()

    files = {'file': open(os.path.join(output_directory, "out.ctm"), 'r')}

    response = requests.post(
        f"{settings.BASE_URL}/api/results/",
        files=files,
        data={
            "filename": f"{message_id}.result.ctm",
            "message_id": message_id
        }
    )

    print(response.text)

    return local_filename
