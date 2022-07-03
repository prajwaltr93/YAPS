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

    # parse metadata
    metadata_structure, total_pages = MetaData.parse_metadata(args.metadata) 

    iterator_obj = iter(Iterator(meta_data=metadata_structure, total_pages=total_pages))

    tree_store = MetaData.create_meta_tree(level=1, iterator_obj=iterator_obj)

    # get chapter on args.level
    # level-order traversal
    level_store = MetaData.wrapped_level_order_traversal(tree_store, args.level, total_pages)

    if args.verbose:
        # TODO : override __repr__ MetaData
        MetaData.pretty_print(level_store)

    if not args.dryrun:
        # split pdfs and write them
        if not args.output_dir:
            args.output_dir = f"{args.input_file}_{args.level}"
            if not path.exists(args.output_dir):
                mkdir(args.output_dir)

        input_file = PdfFileReader(args.input_file) 

        for l_s in level_store:
            title_prep = l_s['BookmarkTitle'].replace("/", " or ")
            with open(path.join(args.output_dir, title_prep + ".pdf"), "wb") as out_file:
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