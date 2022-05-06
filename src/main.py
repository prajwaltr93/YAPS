import argparse
from os import path
from collections import defaultdict
import re
from operator import itemgetter
from modules.IteratorClass import Iterator

first_element = itemgetter(0)

find_int = re.compile("(\d+)")

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="path to PDF file")
parser.add_argument("-o", "--output_dir", help="directory to store split PDF's")
parser.add_argument("-l", "--level", help="level to use to split PDF's", type=int, default=1)
parser.add_argument("metadata", help="path to metadata.txt")

def get_title(line):
    return first_element(line.split(":"))

def parse_metadata(file_path):
    store = []
    total_pages = 0
    with open(file_path, "r") as file_handle:

        for line in file_handle:
            if not total_pages and line.startswith("NumberOfPages"):
                total_pages = first_element(find_int.findall(line))
            if line.startswith("BookmarkBegin"):
                store.append([])
            if line.startswith("BookmarkTitle") or line.startswith("BookmarkPageNumber") or line.startswith("BookmarkLevel"):
                store[-1].append(line.strip())

    return store, total_pages

def create_meta_tree(store, level, iterator_obj):

    while iterator_obj.has_next:
        title, level_got, page_number = iterator_obj.peek()
        # print(title, level_got, page_number)
        d = defaultdict(list)
        d["title"] = title
        d["level"] = level_got 
        d["page_number"] = page_number
        if level == level_got:
            # same level
            store.append(d)
            next(iterator_obj)
            create_meta_tree(store, level_got, iterator_obj)

        if level < level_got:
            store[-1]['child'].append(d)
            next(iterator_obj)
            create_meta_tree(store[-1]['child'], level_got, iterator_obj)

        if level > level_got:
            break

def pretty_print(level_data):
    for entity in level_data:
        print(" " * entity['level'], entity['title'])
        if entity['child']:
            pretty_print(entity['child'])
def main():
    # driver code

    # sanity check arguments
    args = parser.parse_args()

    # check validity of arguments
    input_file_path = args.input_file
    output_dir_path = args.output_dir
    level = args.level 
    metadata_path = args.metadata

    if not path.exists(input_file_path):
        raise Exception("Invalid Input File Path")

    if output_dir_path and not path.exists(output_dir_path):
        raise Exception("Invalid output directory path")

    if not path.exists(metadata_path):
        raise Exception("Invalid Input File Path")

    # parse metadata
    metadata_structure, total_pages = parse_metadata(metadata_path) 

    iterator_obj = iter(Iterator(meta_data=metadata_structure, total_pages=total_pages))

    tree_store = []

    create_meta_tree(store=tree_store, level=1, iterator_obj=iterator_obj)

    # for i in range(5):
    pretty_print(tree_store)

    # split pdfs and write them

    # clean up and close 

if __name__ == "__main__":
    main()