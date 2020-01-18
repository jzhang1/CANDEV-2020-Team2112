# Find the minimum subset of fields contained in every record
# Find the mamimum set of fields contained in corpus

from datasrc import data_files
import ais.stream
from tqdm import tqdm
import ntpath

def min_max_field_sets():
    min_set = None
    max_set = None
    for file in data_files():
        filename = ntpath.basename(file)
        lines = 0
        with open(file) as f:
            for _ in f:
                lines += 1
        with open(file) as f:
            for msg in tqdm(enumerate(ais.stream.decode(f)), desc=filename, total=lines):
                fields = set(msg)
                if min_set == None:
                    min_set = fields
                else:
                    min_set = min_set.intersection(fields)
                if max_set == None:
                    max_set = fields
                else:
                    max_set = max_set.union(fields)
    return min_set, max_set
if __name__ == "__main__":
    min_set, max_set = min_max_field_sets()
    print(min_set)
    print(max_set)