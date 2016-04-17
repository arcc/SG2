#!/usr/bin/python
import os
def get_config(filename):
    curr_file_path = os.path.abspath(__file__)
    path, pyf = os.path.split(curr_file_path)
    fn = os.path.join(path, filename)
    f = open(fn)
    config = {}
    for line in f.readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        ls = line.split()
        if ls != []:
            config[ls[0]] = ls[1]
    return config
