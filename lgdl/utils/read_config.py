import shutil
import os
import re
import ast


def strip_comments(conf_content):
    conf_content = str(conf_content)
    content_without_comment = re.sub(r'(?m)^ *#.*\n?', '', conf_content)
    
    return content_without_comment


def get_substring(string, start, end):
    l1 = string.find(start)
    l2 = string.find(end)
    substring  = string[l1:l2+1]

    return substring


def get_proxies(config):
    proxies_substring = get_substring(config, "proxies", "}")
    proxies_substring = proxies_substring.replace("\n", '')
    if proxies_substring:
        proxies = ast.literal_eval(proxies_substring.partition('=')[-1])
    else:
        # tor socks proxy
        proxies = { 'http' : 'socks5h://127.0.0.1:9050',
                    'https': 'socks5h://127.0.0.1:9050' }
    return proxies


def get_resolution(config):
    conf_lines = config.split("\n")
    for line in conf_lines:
        if line.startswith("resolution"):
            resolution = int(line.partition('=')[-1])
    if resolution not in [25, 50, 75, 100]:
        print("Warning: accepted resolutions are 25, 50, 75, or 100.\
                Got: {}. Setting resolution to 25.".format(resolution))
        resolution = 25

    return resolution


def read_conf_file(config_path):
    with open(config_path, "r") as conf_file:
        conf_content = conf_file.read()
    
    return conf_content


def copy_config_file():
    config_path = os.path.join(os.path.expanduser('~'), ".config", "lgdl", "lgdlrc")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    if not os.path.exists(config_path):
        shutil.copy("lgdlrc", config_path)

    return config_path


def parse_config_file():
    config_path = copy_config_file()
    conf_content = read_conf_file(config_path)
    conf_content = strip_comments(conf_content)
    conf_content = conf_content.replace(' ', '')
    proxies = get_proxies(conf_content)
    resolution = get_resolution(conf_content)
    config = {"proxies": proxies, "resolution": resolution}

    return config

