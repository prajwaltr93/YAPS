from os import mkdir, path
from PyPDF2 import PdfFileReader, PdfFileWriter
from html import unescape

class PDFHandler:
    def __check_or_create_output_dir(self, output_dir):
        if not output_dir:
            output_dir = f"{self.input_file_path}_{self.level}"
        if not path.exists(output_dir):
            mkdir(output_dir)
        
        return output_dir
    
    def __create_input_pdf_obj(self, input_file_path):
        return PdfFileReader(input_file_path)

    def __init__(self, output_path, level_store, input_file, level):
        self.level_store = iter(level_store)
        self.input_file_path = input_file
        self.input_file = self.__create_input_pdf_obj(input_file_path=input_file)
        self.parent_file_meta = self.input_file.getDocumentInfo()
        self.level = level
        self.output_path = self.__check_or_create_output_dir(output_dir=output_path)

    def __iter__(self):
        return self

    def __next__(self):
        l_s = next(self.level_store)
        title_prep = l_s['BookmarkTitle'].replace("/", " or ")
        page_range = range(l_s['BookmarkPageNumber'], l_s['BookmarkLastPageNumber'] + 1)
        return unescape(title_prep), page_range
    
    def write_page_range_to_file(self, page_range):
        out_writer = PdfFileWriter()
        out_writer.addMetadata(self.parent_file_meta)
        for page_number in page_range:
            # 0 based indexing of pages, compared to real-word page numbers
            page_got = self.input_file.pages[page_number - 1]
            out_writer.addPage(page_got)
        return out_writer
