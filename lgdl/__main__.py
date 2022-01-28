#!/usr/bin/env python3
import argparse
import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lgdl")))
sys.path.insert(0, os.path.abspath("."))

from parsers import libgen
from utils.display import pretty_print
from utils.download import download
from utils.read_config import parse_config_file


def main():
    config = parse_config_file()

    parser = argparse.ArgumentParser(prog="lgdl", \
            description="Command Line Interface for Library Genesis.")
    parser.add_argument("pos_search", nargs='?', type=str, help="search query")
    parser.add_argument("-s", "--search", type=str, help="search query")
    parser.add_argument("--update-mirrors", dest="update", action="store_true",\
            help="update mirrors and sort based on response time")
    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)
    else:
        args = parser.parse_args()

    if args.update:
        print("Fast tracking mirrors...")
        mirrors_url = "https://sci-hub.41610.org/library-genesis"
        mirrors = libgen.get_mirrors(mirrors_url, config, sort=True)
        for index, mirror in enumerate(mirrors):
            print("-- {}: {}".format(index, mirror))
    else:
        #TODO: get from a file under CONF dir.
        mirrors = None

    search = False
    if args.pos_search:
        search = True
        search_query = args.pos_search
    elif args.search:
        search = True
        search_query = args.search

    if search:
        query_results = libgen.parse_query(search_query, config, mirrors=mirrors)
        
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
        titles, download_links = libgen.get_download_url(query_results, indices, config)
        for title, link in zip(titles, download_links):
            download(link, title, config)

if __name__ == "__main__":
    main()
