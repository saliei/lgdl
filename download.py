import requests
import sys
import cgi
from tqdm import tqdm

from read_conf import get_proxies

proxies = get_proxies()

def download(url):
    buffer_size = 1024
    response = requests.get(url, stream=True, proxies=proxies)
    file_size = int(response.headers.get("Content-Length", 0))
    #TODO: get the name from query result
    # default_filename = title + '.' + extension
    default_filename = "test"
    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition:
        value, params = cgi.parse_header(content_disposition)
        filename = params.get("filename", default_filename)
    else:
        filename = default_filename
    
    progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", \
            total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))