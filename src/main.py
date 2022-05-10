import argparse
from os import path, mkdir
import re
from operator import itemgetter
from PyPDF2 import PdfFileReader, PdfFileWriter

from modules.IteratorClass import Iterator
from functools import partial

first_element = itemgetter(0)

find_int = re.compile("(\d+)")

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="path to PDF file")
parser.add_argument("-o", "--output_dir", help="directory to store split PDF's")
parser.add_argument("-l", "--level", help="level to use to split PDF's", type=int, default=1)
parser.add_argument("-v", "--verbose", help="print created meta tree", action="store_true")
parser.add_argument("metadata", help="path to metadata.txt")
parser.add_argument("-d", "--dryrun", help="don't write pdf's, just show chapters traversed", action="store_true", default=False)

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

def create_meta_tree(level, iterator_obj, store):

    while iterator_obj.has_next:
        d = iterator_obj.peek()

        prep_create_meta_tree = partial(create_meta_tree, d['BookmarkLevel'], iterator_obj)

        level_got = d['BookmarkLevel']

        if level == level_got:
            # same level
            store.append(d)
            next(iterator_obj)
            prep_create_meta_tree(store)

        if level < level_got:
            store[-1]['child'].append(d)
            next(iterator_obj)
            prep_create_meta_tree(store[-1]['child'])

        if level > level_got:
            break

def pretty_print(level_data):
    for entity in level_data:
        print(" " * 2 * entity['BookmarkLevel'], end=" ")
        print("|", end="")
        print("--", entity['BookmarkTitle'])
        if entity['child']:
            pretty_print(entity['child'])

def level_order_traversal_tree(store, metadata, level_req):
    for index, entity in enumerate(metadata):
        level_got = entity['BookmarkLevel']

        if level_got == level_req:
            if store:
                if "BookmarkLastPageNumber" not in store[-1]:
                    store[-1]["BookmarkLastPageNumber"] = entity["BookmarkPageNumber"]
            store.append(entity)

        if level_got < level_req:
            level_order_traversal_tree(store, entity['child'], level_req)
            if store:
                if "BookmarkLastPageNumber" not in store[-1]:
                    if index <= (len(metadata) - 2): 
                        store[-1]["BookmarkLastPageNumber"] = metadata[index + 1]["BookmarkPageNumber"]

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

    create_meta_tree(level=1, iterator_obj=iterator_obj, store=tree_store)

    if args.verbose:
        pretty_print(tree_store)

    # get chapter on args.level
    # level-order traversal
    level_store = []
    level_order_traversal_tree(level_store, tree_store, level)
    if level_store:
        if "BookmarkLastPageNumber" not in level_store[-1]:
            level_store[-1]['BookmarkLastPageNumber'] = int(total_pages)

    if args.verbose:
        pretty_print(level_store)

    if not args.dryrun:
        # split pdfs and write them
        if not output_dir_path:
            output_dir_path = f"{input_file_path}_{level}"
            if not path.exists(output_dir_path):
                mkdir(output_dir_path)

        input_file = PdfFileReader(input_file_path) 

        for l_s in level_store:
            with open(path.join(output_dir_path, l_s['BookmarkTitle'] + ".pdf"), "wb") as out_file:
                out_writer = PdfFileWriter()
                for page_number in range(l_s['BookmarkPageNumber'], l_s['BookmarkLastPageNumber']):
                    # 0 based indexing of pages, compared to real-word page numbers
                    page_got = input_file.pages[page_number - 1]
                    out_writer.addPage(page_got)

                out_writer.write(out_file)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] : {str(e)}")