#! /usr/bin/env python

from copy import deepcopy
import json
import sys

def dict_of_dicts_merge(x, y):
    z = {}
    overlapping_keys = x.keys() & y.keys()
    for key in overlapping_keys:
        z[key] = dict_of_dicts_merge(x[key], y[key])
    for key in x.keys() - overlapping_keys:
        z[key] = deepcopy(x[key])
    for key in y.keys() - overlapping_keys:
        z[key] = deepcopy(y[key])
    return z

########################################################
#This program reads all the args as input file and combine them to one json file with the name of the last output
# usage:
# $ combine_json.py T2POC_* T2POC
########################################################

all_data=dict([])
for f in sys.argv[1:-1]:
    with open(f,"r") as fi:
        data_in=json.load(fi)

    all_data=dict_of_dicts_merge(all_data,data_in)



with open(sys.argv[-1],"w") as fo:
    json.dump(all_data,fo,indent=4)

