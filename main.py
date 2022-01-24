#!/usr/bin/env python3
import argparse
import sys

import libgen_parser
from display import pretty_print
from download import download

mirrors_url = "https://sci-hub.41610.org/library-genesis"

parser = argparse.ArgumentParser(prog="lgdl", \
        description="Command Line Interface for Library Genesis.")
parser.add_argument("-s", "--search", nargs='?', type=str, help="search query")
args = parser.parse_args()

mirrors = libgen_parser.get_mirrors(mirrors_url)
query_results = libgen_parser.parse_query(args.search)

for index, result in enumerate(query_results):
    pretty_print(result, index)

ids = sys.stdin.readline()
ids = ids.rstrip().replace(' ', '').split(',')

indices = []
for _id in ids:
    try:
        _id = int(_id)
        indices.append(_id)
    except Exception as err:
        if '-' in _id:
            _id = [int(_id) for _id in _id.split('-')]
            indices.append(_id)
        else:
            print("Indices Not accepted!")
            raise

download_links = libgen_parser.get_download_url(query_results, indices)
for link in download_links:
    download(link)
            
