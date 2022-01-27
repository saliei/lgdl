from tqdm import tqdm
import requests
import cgi


#TODO: add option in config file for the filename, title or full name
def download(url, title, config):
    buffer_size = 1024
    response = requests.get(url, stream=True, proxies=config["proxies"])
    file_size = int(response.headers.get("Content-Length", 0))

    default_filename = title
    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition:
        value, params = cgi.parse_header(content_disposition)
        filename = params.get("filename", default_filename)
    else:
        filename = default_filename
    
    progress = tqdm(response.iter_content(buffer_size), f"Downloading {title}", \
            total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))
