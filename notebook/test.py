import ais.stream
import csv
import os
import sys
from tqdm import tqdm

def data_src():
    data_dir = "../data"
    filename = "CCG_AIS_Log_2018-05-01.csv"
    path = os.path.join(data_dir, filename)
    return path

def verify_datasrc(path: str):
    with open(path) as f:
        try:
            for msg in tqdm(enumerate(ais.stream.decode(f))):
                pass
        except e:
            print(e)

def data_fields(path: str):
    fields = set()
    with open(path) as f:
        for msg in tqdm(ais.stream.decode(f)):
            for key in msg:
                fields.add(key)
    print(fields)
            
if __name__ == "__main__":
    path = data_src()
    data_fields(path)