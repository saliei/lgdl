#!/usr/bin/env python3
import argparse
import sys

from lgdl import libgen_parser
from lgdl.display import pretty_print
from lgdl.download import download


def main():
    parser = argparse.ArgumentParser(prog="libgen-dl", \
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
        mirrors = libgen_parser.get_mirrors(mirrors_url, sort=True)
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
        query_results = libgen_parser.parse_query(search_query, mirrors=mirrors)
        
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
        titles, download_links = libgen_parser.get_download_url(query_results, indices)
        for title, link in zip(titles, download_links):
            download(link, title)

if __name__ == "__main__":
    main()