#!/usr/bin/python
def get_config(filename):
    f = open(filename)
    config = {}
    for line in f.readlines():
        if line.startswith("#"):
            continue
        ls = line.split()
        config[ls[0]] = ls[1]
    return config
