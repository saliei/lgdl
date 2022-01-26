import requests
from tqdm import tqdm

from .read_config import parse_config_file
config = parse_config_file()

#TODO: add option in config file for the filename, title or full name
def download(url, title):
    buffer_size = 1024
    response = requests.get(url, stream=True, proxies=config["proxies"])
    file_size = int(response.headers.get("Content-Length", 0))
    
    progress = tqdm(response.iter_content(buffer_size), f"Downloading {title}", \
            total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))
