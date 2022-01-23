import libgen_parser as parser
from display import pretty_print
from download import download

search_query = "quantum"
mirrors_url = "https://sci-hub.41610.org/library-genesis"

mirrors = parser.get_mirrors(mirrors_url)
query_results = parser.parse_query(search_query)
download_link = parser.get_download_url(query_results)

for index, result in enumerate(query_results):
    pretty_print(result, index)

download(download_link)

