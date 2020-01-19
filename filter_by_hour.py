import ais.stream
from tqdm import tqdm
import os
import json

def parse_raw(path):
    with open(path,'r') as f:
        for msg in ais.stream.decode(f):
            yield msg

def check_msg(msg: dict):
    if 'hour' in msg:
        return True
    return False

def write_json(raw_file, json_file):
    if os.path.exists(json_file):
        os.remove(json_file)
    count = 0
    with open(json_file,'a') as f:
        for msg in tqdm(parse_raw(raw_file)):
            if check_msg(msg):
                json.dump(msg,f)
                f.write('\n')
                count += 1
    return count

if __name__ == "__main__":
    raw_dir = "../../data/raw_all/CCG_AIS_Log_2018-05-02.csv"
    count = write_json(raw_dir,'out_hour.json')
    print(count)
            