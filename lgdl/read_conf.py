import re
import ast

config_filename = "lgdl.conf"

def read_conf_file(filename):
    with open(filename, "r") as conf_file:
        conf_content = conf_file.read()
    return conf_content

def strip_comments(conf_content):
    conf_content = str(conf_content)
    content_without_comment = re.sub(r'(?m)^ *#.*\n?', '', conf_content)
    return content_without_comment

def get_substring(string, start, end):
    l1_proxies = string.find(start)
    l2_proxies = string.find(end)
    substring  = string[l1_proxies:l2_proxies+1]
    return substring

def get_proxies():
    conf_content = read_conf_file(config_filename)
    conf_content = strip_comments(conf_content)
    proxies_substring = get_substring(conf_content, "proxies", "}")
    proxies_substring = proxies_substring.replace("\n", '')
    proxies_substring = proxies_substring.replace(" " , '')
    if proxies_substring:
        proxies = ast.literal_eval(proxies_substring.partition('=')[2])
    else:
        # tor socks proxy
        proxies = { 'http' : 'socks5h://127.0.0.1:9050',
                    'https': 'socks5h://127.0.0.1:9050' }
    return proxies

