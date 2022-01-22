from bs4 import BeautifulSoup
import requests
import re

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
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


ll = "http://libgen.rs/search.php?req=quantum&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def"
pp = requests.get(ll, proxies=proxies)
ss = BeautifulSoup(pp.text, "html.parser")

# needs fiding tables in another pages also
tb = ss.find("table", class_="c")
tr = tb.find_all("tr")
tr = tr[1:]

# find atuhors
tr[1].find_all('a', href=re.compile(r'author'))

# id is the first table data
id_ = tr[1].find('td')

# title of the book
# ISBN numbers?
title = tr[1].find('a', href=re.compile(r'index\.php')).text

# table datas
# 0: id
# 1: authors
# 2: title and series
# 3: pubisher
# 4: year
# 5: pages
# 6: language
# 7: size
# 8: extension
# 9 onward: mirrors
tds = tr[1].find_all('td')

gen_id    = tds[0].text
author    = tds[1].text
title     = tds[2].find('a', href=re.compile(r'index\.php')).text
publisher = tds[3].text
year      = tds[4].text
pages     = tds[5].text
language  = tds[6].text
size      = tds[7].text
extension = tds[8].text
mirrors   = [link.find('a')["href"] for link in tds[9:]]


# downlod part
link = mirrors[0]
page = requests.get(link, proxies=proxies)
soup = BeautifulSoup(page.content, "html.parser")
download_link = soup.find('a', text=re.compile("GET"))["href"]

r = requests.get(download_link, proxies=proxies)
n = r.headers["Content-Disposition"]
_, __, name = n.partition("filename=")
name = name.strip('"')

# progress bar?
with open(name, "wb") as _file:
    _file.write(r.content)
