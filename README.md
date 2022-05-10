# YAPS - Yet Another PDF Splitter

Splits PDF's based on Bookmarks.

## Usage

```shell
usage: main.py [-h] [-o OUTPUT_DIR] [-l LEVEL] [-v] input_file metadata

positional arguments:
  input_file            path to PDF file
  metadata              path to metadata.txt

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        directory to store split PDF's
  -l LEVEL, --level LEVEL
                        level to use to split PDF's
  -v, --verbose         print created meta tree
```

## what is metadata and how to get it

metadata is used by `main.py` to split chapters into smaller PDF's

### metadata

metadata is a simple .txt file with information regarding the bookmark data of your input PDF file

### how to get it

Using an Open source tool `pdftk` which comes with most linux distribution bundled, you can extract metadata 
of your PDF file.

```
pdftk input_file.pdf dump_data >> metadata.txt
```

## TODO 

- [ ] document tree creation and traversal
- [ ] fix page range bug
- [ ] fix chapter names with special characters
- [ ] refactor code 