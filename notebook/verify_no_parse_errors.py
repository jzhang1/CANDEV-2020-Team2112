# Verify that the libais parser can process the input data without errors
from datasrc import data_files
import ais.stream
from tqdm import tqdm
import ntpath

def verify_parse():
    for file in data_files():
        filename = ntpath.basename(file)
        lines = 0
        with open(file) as f:
            for _ in f:
                lines += 1
        with open(file) as f:
            for _ in tqdm(enumerate(ais.stream.decode(f)), desc=filename, total=lines):
                pass
if __name__ == "__main__":
    verify_parse()