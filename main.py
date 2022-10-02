#!/usr/bin/env python
from os import path
from modules.IteratorClass import Iterator
from modules.ArgParserClass import ArgParser
from modules.MetaDataClass import MetaData 
from modules.PDFHandlerClass import PDFHandler

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

    # get chapters on args.level
    # level-order traversal
    level_store = MetaData.wrapped_level_order_traversal(tree_store, args.level, total_pages)

    if args.verbose:
        MetaData.pretty_print(level_store)

    if not args.dryrun:
        # split pdfs and write them
        pdf_handler = PDFHandler(output_path=args.output_dir, level_store=level_store, input_file=args.input_file, level=args.level)

        for title_prep, page_range in pdf_handler:
            with open(path.join(pdf_handler.output_path, title_prep + ".pdf"), "wb") as out_file:
                out_writer = pdf_handler.write_page_range_to_file(page_range=page_range)
                out_writer.write(out_file)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] : {str(e)}")