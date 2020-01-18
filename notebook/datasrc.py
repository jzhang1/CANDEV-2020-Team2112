import os

def data_files():
    data_dir = "../data/Raw Data"
    return (os.path.join(data_dir, file) for file in os.listdir(data_dir) if file[-3:] == "csv")