from operator import itemgetter
import re

first_element = itemgetter(0)

find_int = re.compile("(\d+)")

class Iterator:
    
    def __init__(self, meta_data, total_pages):
        self.meta_data = meta_data
        self.len = len(self.meta_data) - 1
        self.current = -1
        self.total_pages = total_pages

    def peek(self):
        current = self.meta_data[self.current + 1] 
        return (int(first_element(find_int.findall(current[i]))) if i else current[i] for i in range(len(current)))

    def __next__(self):
        self.current += 1 

    def __iter__(self):
        return self

    @property
    def has_next(self):
        return self.current < self.len