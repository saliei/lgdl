#!/usr/bin/env python3
import argparse

import libgen_parser
from display import pretty_print
from download import download

mirrors_url = "https://sci-hub.41610.org/library-genesis"

parser = argparse.ArgumentParser(prog="libgen", \
        description="Command Line Interface for Library Genesis.")
parser.add_argument("search", type=str, help="general search query")
parser.add_argument("-s", "--search", default=None, help="general search query")
args = parser.parse_args()


mirrors = libgen_parser.get_mirrors(mirrors_url)
query_results = libgen_parser.parse_query(args.search)
download_link = libgen_parser.get_download_url(query_results)

for index, result in enumerate(query_results):
    pretty_print(result, index)

# download(download_link)

