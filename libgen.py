from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import sys
import cgi
import re


proxies = {
    'http' : 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

url = "https://sci-hub.41610.org/library-genesis"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

gen_links = soup.find_all('a', {"rel":"nofollow noopener"})


pool = []
# for link in gen_links:
    # link = link["href"]
    # page = requests.get(link, proxies=proxies)
    # if page.status_code == 200:
        # pool.append(link)
pool.append(gen_links[0]["href"])


# if there are pages more than (get by the number of results and resolution) add &page=2 to the link
ll = "http://libgen.rs/search.php?req=quantum&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def"
pp = requests.get(ll, proxies=proxies)
ss = BeautifulSoup(pp.text, "html.parser")

# needs finding tables in another pages also
tb = ss.find("table", class_="c")
trs = tb.find_all("tr")
trs = trs[1:]


results = []
num_results = ss.find("td", text=re.compile("files found")).text
num_results = int(num_results.partition("files")[0])

for tr in trs:
    tds = tr.find_all('td')
    result = {}
    #TODO: catch exceptions
    result["id"]        = int(tds[0].text)
    result["author"]    = tds[1].text
    #TODO: extract ISBN from title
    result["title"]     = tds[2].find('a', href=re.compile(r'index\.php')).text
    result["publisher"] = tds[3].text
    result["year"]      = tds[4].text
    result["pages"]     = tds[5].text
    result["language"]  = tds[6].text
    result["size"]      = tds[7].text
    result["extension"] = tds[8].text
    result["mirrors"]   = [link.find('a')["href"] for link in tds[9:]]
    results.append(result)


# downlod part
# link = mirrors[0]
link = results[0]["mirrors"][0]
page = requests.get(link, proxies=proxies)
soup = BeautifulSoup(page.content, "html.parser")
download_link = soup.find('a', text=re.compile("GET"))["href"]

# r = requests.get(download_link, proxies=proxies)
# n = r.headers["Content-Disposition"]
# _, __, name = n.partition("filename=")
# name = name.strip('"')

# progress bar?
# with open(name, "wb") as _file:
    # _file.write(r.content)

def download(url):
    buffer_size = 1024
    response = requests.get(url, stream=True, proxies=proxies)
    file_size = int(response.headers.get("Content-Length", 0))
    # file_name = str(r.headers["Content-Disposition"].partition("filename=")[2]).strip('"')
    default_filename = title + '.' + extension
    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition:
        value, params = cgi.parse_header(content_disposition)
        filename = params.get("filename", default_filename)
    else:
        filename = default_filename
    
    progress = tqdm(response.iter_content(buffer_size), f"Downloading {title}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))


# download(download_link)

color = {
        'purple': '\x1b[95m',
        'cyan': '\x1b[96m',
        'darkcyan': '\x1b[36m',
        'blue': '\x1b[94m',
        'green': '\x1b[92m',
        'yellow': '\x1b[93m',
        'red': '\x1b[91m',
        'bold': '\x1b[1m',
        'underline': '\x1b[4m',
        'end': '\x1b[0m'
        }
def prety_print(result, index):
    #TODO: make dashes dynamic
    _id = index + 1
    print("\nID: {}\n{}".format(_id, "----" + '-'*len(str(_id))))
    print("      Title: {}".format(color["bold"] + result["title"]  + color["end"]))
    print("     Author: {}".format(color["bold"] + result["author"] + color["end"]))
    print("       Year: {}".format(result["year"]))
    print("  Publisher: {}".format(result["publisher"]))
    print("     Format: {}".format(result["extension"]))

# prety_print(results[2])
for index, result in enumerate(results):
    prety_print(result, index)
