from os import path, mkdir
from PyPDF2 import PdfFileReader, PdfFileWriter

from modules.IteratorClass import Iterator
from modules.ArgParserClass import ArgParser
from modules.MetaDataClass import MetaData 

def main():
    # driver code

    # sanity check arguments
    arg_parse_obj = ArgParser()

    arg_parse_obj.init_parser()

    args = arg_parse_obj.verify_arguments()

    input_file_path = args.input_file
    output_dir_path = args.output_dir
    level = args.level 
    metadata_path = args.metadata

    # parse metadata
    metadata_structure, total_pages = MetaData.parse_metadata(metadata_path) 

    iterator_obj = iter(Iterator(meta_data=metadata_structure, total_pages=total_pages))

    tree_store = MetaData.create_meta_tree(level=1, iterator_obj=iterator_obj)

    # get chapter on args.level
    # level-order traversal
    # TODO : add decorator to combine following 3 lines
    level_store = MetaData.level_order_traversal_tree(tree_store, level)
    if level_store:
        if "BookmarkLastPageNumber" not in level_store[-1]:
            level_store[-1]['BookmarkLastPageNumber'] = int(total_pages)

    if args.verbose:
        # TODO : override __repr__ MetaData
        MetaData.pretty_print(level_store)

    if not args.dryrun:
        # split pdfs and write them
        if not output_dir_path:
            output_dir_path = f"{input_file_path}_{level}"
            if not path.exists(output_dir_path):
                mkdir(output_dir_path)

        input_file = PdfFileReader(input_file_path) 

        for l_s in level_store:
            title_prep = l_s['BookmarkTitle'].replace("/", " or ")
            with open(path.join(output_dir_path, title_prep + ".pdf"), "wb") as out_file:
                out_writer = PdfFileWriter()
                for page_number in range(l_s['BookmarkPageNumber'], l_s['BookmarkLastPageNumber'] + 1):
                    # 0 based indexing of pages, compared to real-word page numbers
                    page_got = input_file.pages[page_number - 1]
                    out_writer.addPage(page_got)

                out_writer.write(out_file)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] : {str(e)}")