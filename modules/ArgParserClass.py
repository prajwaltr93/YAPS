import argparse
from os import path

class ArgParser:
    
    arg_dict = [ 
            [
                "input_file",
                {
                    "help" : "path to PDF file"
                }
            ],
            [
                "-o", "--output_dir",
                {
                    "help" : "Path to store Split PDF's"
                }
            ],
            [
                "-l", "--level",
                {
                    "help": "Level to use to Split PDF's",
                    "type" : int,
                    "default" : 1,
                }
            ],
            [
                "-v", "--verbose",
                {
                    "help": "Print Parsed selected bookmark data",
                    "action" : "store_true"
                }
            ],
            [
                "metadata",
                {
                    "help": "Path to metadata.txt",
                }
            ],
            [
                "-d", "--dryrun",
                {
                    "help": "Parse Bookmark MetaData and Display selected. will not write PDF's",
                    "action" : "store_true",
                    "default" : False
                }
            ],
    ] 

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()

    def init_parser(self) -> None:

        for arg in ArgParser.arg_dict:
            self.parser.add_argument(*arg[:-1], **arg[-1])

    def verify_arguments(self):

        args = self.parser.parse_args()

        # check validity of arguments
        input_file_path = args.input_file
        output_dir_path = args.output_dir
        metadata_path = args.metadata

        if not path.exists(input_file_path):
            raise Exception("Invalid Input File Path")

        if output_dir_path and not path.exists(output_dir_path):
            raise Exception("Invalid output directory path")

        if not path.exists(metadata_path):
            raise Exception("Invalid Metadata File Path")

        return args
