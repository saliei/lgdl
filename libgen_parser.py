from bs4 import BeautifulSoup
import requests
import urllib
import re

from read_conf import get_proxies

proxies = get_proxies()

#TODO: make fast mirror list sort optional and onetime.
def get_mirrors(url, sort=False):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    mirrors_pool = soup.find_all('a', {"rel":"nofollow noopener"})
    mirrors_pool = [link["href"] for link in mirrors_pool]
    # sort mirrors based on response time
    mirrors_res_time = []
    for link in mirrors_pool:
        try:
            response = requests.get(link, proxies=proxies)
            if sort:
                res_time = response.elapsed.total_seconds()
                mirrors_res_time.append([link, res_time])
            else:
                mirrors_res_time.append(link)
        except:
            pass
    if sort:
        mirrors_res_time.sort(key=lambda x: x[1])
        mirrors_pool = [url_res_time[0] for url_res_time in mirrors_res_time]
    else:
        mirrors_pool = mirrors_res_time

    return mirrors_pool


#TODO: add other mirrors, currently works for libgen.rs
def parse_query(search_query, mirror_url=None):
    search_resolution = 100
    search_query_urlencoded = urllib.parse.quote_plus(search_query)
    search_url = ("http://libgen.rs/search.php?req={}&lg_topic=libgen&"
                  "open=0&view=simple&res={}&phrase=1&column=def")\
                  .format(search_query_urlencoded, search_resolution)
    page = requests.get(search_url, proxies=proxies)
    soup = BeautifulSoup(page.content, "html.parser")
    
    table = soup.find("table", class_='c')
    table_rows = table.find_all("tr")[1:]

    num_results = soup.find("td", text=re.compile("files found")).text
    num_results = int(num_results.partition("files")[0])
    #TODO: if there are more pages than one, query those also if asked.
    if num_results > search_resolution:
        other_pages = True
    else:
        other_pages = False

    results = []
    for table_row in table_rows:
        table_data = table_row.find_all('td')
        result = {}
        #TODO: catch exceptions
        result["id"]        = int(table_data[0].text)
        result["author"]    = table_data[1].text
        #TODO: extract ISBN from title
        result["title"]     = table_data[2].find('a', href=re.compile(r'index\.php')).text
        result["publisher"] = table_data[3].text
        result["year"]      = table_data[4].text
        result["pages"]     = table_data[5].text
        result["language"]  = table_data[6].text
        result["size"]      = table_data[7].text
        result["extension"] = table_data[8].text
        result["mirrors"]   = [link.find('a')["href"] for link in table_data[9:]]
        results.append(result)

    return results


#TODO: get the id of document to be downloaded from user.
def get_download_url(query_results, indices):
    download_links = []
    for index in indices:
        mirror_link = query_results[index-1]["mirrors"][0]
        page = requests.get(mirror_link, proxies=proxies)
        soup = BeautifulSoup(page.content, "html.parser")
        download_link = soup.find('a', text=re.compile("GET"))["href"]
        download_links.append(download_link)

    return download_links

