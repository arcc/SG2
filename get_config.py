#!/usr/bin/python
import os
def get_config(filename):
    curr_file_path = os.path.abspath(__file__)
    path, pyf = os.path.split(curr_file_path)
    fn = os.path.join(path, filename)
    f = open(fn)
    config = {}
    local = False
    for line in f.readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.startswith('local'):
            ls = line.split()
            if ls[1].lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:
                local = True
            continue
        ls = line.split()
        if ls != []:
            if ls[0].startswith('<'):
                block = ls[0][1:-1]
                config[block] = {}
            else:
                if block == '':
                    raise ValueError("A information block has to start wtih <block_name>")
                config[block][ls[0]]=ls[1]
    result_local = {}
    result = {}
    for key in config.keys():
        if 'local' in key:
            reskey = key.split('_')[1]
            result_local[reskey] = config[key]
        else:
            result[key] = config[key]
    if local:
        return result_local
    else:
        return result

if __name__== "__main__":
    print get_config('config.dat')
