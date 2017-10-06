#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#"""
#Created on Mon Oct  2 15:39:00 2017
#
#@author: Leilai like Coding
from PCN import PCN
from imp import importlib
import sys
import gc
sys.setrecursionlimit(10000)
gc.enable()
#"""
#name = input("Enter file:")
#if len(name) < 1 : name = "part1.pcn"
filename = "part5.pcn"
## Initilize PCN inst and read PCNs from text
UPR=PCN()
UPR.read_pcn(filename)
print(UPR.PCN_list)
UPR.Complement()
print('Finished')
print(UPR.PCN_list)
UPR.write_pcn("Out_"+filename)
del UPR
gc.collect()
