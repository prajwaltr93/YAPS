from collections import defaultdict
from operator import itemgetter
import re

first_element = itemgetter(0)
second_element = itemgetter(1)

find_pair = re.compile("(\w+):\s?(.*)")

class Iterator:
    
    def __init__(self, meta_data, total_pages):
        self.meta_data = meta_data
        self.len = len(self.meta_data) - 1
        self.current = -1
        self.total_pages = total_pages

    def peek(self):
        current = self.meta_data[self.current + 1] 
        d = defaultdict(list)
        for i in range(len(current)):
            found = first_element(find_pair.findall(current[i]))
            if i:
                d[first_element(found)] = int(second_element(found))
            else:
                d[first_element(found)] = second_element(found)
        return d

    def __next__(self):
        self.current += 1 

    def __iter__(self):
        return self

    @property
    def has_next(self):
        return self.current < self.len