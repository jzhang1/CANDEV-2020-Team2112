import ais.stream
from tqdm import tqdm
import os
import json
from math import sin, cos, sqrt, atan2, radians
from geopy import distance

def get_dist(loc1,loc2):
    # approximate radius of earth in km
    R = 6373.0
    '''
    lat1 = radians(loc1[0])
    lon1 = radians(loc1[1])
    lat2 = radians(loc2[0])
    lon2 = radians(loc2[1])
    '''
    dist = distance.distance(loc1,loc2).km

    dist = dist * 0.53996 #convert to knot
    return dist

def get_time_diff(t1,t2):
    '''
    ret: time in secs
    '''
    #print(t1)
    #print(t2)
    return (t2[0] - t1[0]) + (t2[1] - t1[1])/60 + (t2[2] - t1[2])/3600 


def parse_raw(path):
    with open(path,'r') as f:
        for msg in ais.stream.decode(f):
            yield msg

def print_by_mmsi(mmsi: int, path: str):
    for msg in parse_raw(path):
        if msg['mmsi'] == mmsi:
            print(msg)

def check_msg(msg: dict):
    if 'hour' in msg:
        return True
    return False

def write_json(raw_file, json_file):
    if os.path.exists(json_file):
        os.remove(json_file)
    count = 0
    with open(json_file,'w') as f:
        for msg in tqdm(parse_raw(raw_file)):
            if check_msg(msg):
                json.dump(msg,f)
                f.write('\n')
                count += 1
    return count

def add_speed(in_file):
    prev_dic = {}
    with open(in_file,'r') as f:
        for line in f:
            msg = json.loads(line)
            if msg['mmsi'] not in prev_dic:
                loc = (msg['y'],msg['x'])
                time = (msg['hour'],msg['minute'],msg['second'])
                prev_dic[msg['mmsi']] = {'loc':loc,'time':time}
                msg['speed'] = -1
            else:
                t_prev = prev_dic[msg['mmsi']]['time']
                t_cur = (msg['hour'],msg['minute'],msg['second'])
                time_h = get_time_diff(t_prev,t_cur)
                if time_h != 0:
                    msg['speed'] = get_dist(prev_dic[msg['mmsi']]['loc'],(msg['y'],msg['x']))/time_h
                    prev_dic[msg['mmsi']] = {'loc':(msg['y'],msg['x']),'time':t_cur}
                    if msg['speed'] > 500:
                        print(t_prev)
                        print(t_cur)
                else:
                    msg['speed'] = -1
            yield msg

def write_speed(infile,outfile):
    with open(outfile,'w') as f:
        for msg in add_speed(infile):
            json.dump(msg,f)
            f.write('\n')

if __name__ == "__main__":
    raw_dir = "../../data/raw_all/CCG_AIS_Log_2018-05-02.csv"
    count = write_json(raw_dir,'out_hour.json')
    print(count)
    write_speed('out_hour.json', 'out_speed.json')
            