from nemreader import read_nem_file

def read_NEM(path, ignore_headers):
    return read_nem_file(path, ignore_missing_header=ignore_headers)