import re
from functools import partial
from html import unescape
from operator import itemgetter

first_element = itemgetter(0)

find_int = re.compile("(\d+)")

class MetaData:

    @staticmethod
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

    @staticmethod
    def create_meta_tree(level, iterator_obj, store=[]): # store is initialized only once on first call

        while iterator_obj.has_next:
            d = iterator_obj.peek()

            prep_create_meta_tree = partial(MetaData.create_meta_tree, d['BookmarkLevel'], iterator_obj)

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
        
        return store

    @staticmethod
    def level_order_traversal_tree(metadata, level_req, store=[]):
        for index, entity in enumerate(metadata):
            level_got = entity['BookmarkLevel']

            if level_got == level_req:
                if store:
                    if "BookmarkLastPageNumber" not in store[-1]:
                        store[-1]["BookmarkLastPageNumber"] = entity["BookmarkPageNumber"]
                store.append(entity)

            if level_got < level_req:
                MetaData.level_order_traversal_tree(entity['child'], level_req, store)
                if store:
                    if "BookmarkLastPageNumber" not in store[-1]:
                        if index <= (len(metadata) - 2): 
                            store[-1]["BookmarkLastPageNumber"] = metadata[index + 1]["BookmarkPageNumber"]

        return store
    
    @staticmethod
    def wrapped_level_order_traversal(metadata, level_req, total_pages):
        level_store = MetaData.level_order_traversal_tree(metadata, level_req)
        if level_store:
            if "BookmarkLastPageNumber" not in level_store[-1]:
                level_store[-1]['BookmarkLastPageNumber'] = int(total_pages)
    
        return level_store


    @staticmethod
    def pretty_print(level_data, depth=1, prefix=""):
        prefix += "  "
        for entity in level_data:
            print(prefix, end="")
            print("|__", unescape(entity['BookmarkTitle']))
            if entity['child']:
                prefix += ":"
                print(prefix, end="")
                print("  \\")
                MetaData.pretty_print(entity['child'], depth=depth+1, prefix=prefix)
                prefix = prefix[:-1]