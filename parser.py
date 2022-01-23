from bs4 import BeautifulSoup
import requests
import re

from display import pretty_print
from read_conf import get_proxies

proxies = get_proxies()

mirrors_url = "https://sci-hub.41610.org/library-genesis"

#TODO: make fast mirror list optional and onetime
def get_mirrors(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    mirrors_pool = soup.find_all('a', {"rel":"nofollow noopener"})
    mirrors_pool = [link["href"] for link in mirrors_pool]
    # sort mirrors based on response time
    mirrors_res_time = []
    for link in mirrors_pool:
        try:
            response = requests.get(link, proxies=proxies)
            res_time = response.elapsed.total_seconds()
            mirrors_res_time.append([link, res_time])
        except:
            pass
    mirrors_res_time.sort(key:lambda x: x[1])
    mirrors_pool = [url_res_time[0] for url_res_time in mirrors_res_time]
    return mirrors_pool




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



# download(download_link)


# prety_print(results[2])
for index, result in enumerate(results):
    pretty_print(result, index)
