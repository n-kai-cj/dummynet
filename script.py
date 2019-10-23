# 
#  Copyright (c) 2002-2003,2010,2019 
# 
#  Redistribution and use in source forms, with and without modification,
#  are permitted provided that this entire comment appears intact.
# 
#  Redistribution in binary form may occur without any restrictions.
#  Obviously, it would be nice if you gave credit where credit is due
#  but requiring it would be too onerous.
# 
#  This software is provided ``AS IS'' without any warranties of any kind.
# 
#  $FreeBSD: head/sbin/ipfw/dummynet.c 206843 2010-04-19 15:11:45Z luigi $
# 
#  dummynet support
#

# coding utf-8

import sys
import time
import subprocess
import csv
import threading

### read next line ###
def nextread(f):
    for line in f:
        if len(line) == 0 or line == None or line[0].startswith('#'):
            continue
        return line

### flush ipfw pipe ###
def flush_ipfw():
    subprocess.call('ipfw -q -f pipe flush', shell=True)
    subprocess.call('ipfw -q -f flush', shell=True)

### pass through ssh and rdp session ###
def allow_ssh_rdp():
    subprocess.call('ipfw add 1 allow ip from any to any 22,3389', shell=True)
    subprocess.call('ipfw add 2 allow ip from any 22,3389 to any', shell=True)

### network shaping ###
def run(idx, csv_name, sleep):
    runfirst = True
    while True:
        with open(csv_name, 'r') as csv_file:
            ### read header ###
            f = csv.reader(csv_file)
            line = nextread(f)
            proto = line[0]
            line = nextread(f)
            srcip = line[0]
            srcport = line[1]
            line = nextread(f)
            dstip = line[0]
            dstport = line[1]
            line = nextread(f)
            opt = line[0]
            if idx == 100:
                print("--------------------------------------------------")
                print("%s from %s:%s to %s:%s %s"
                      % (proto, srcip, srcport, dstip, dstport, opt))
            ### exec ipfw add pipe for the first time  ###
            if runfirst == True:
                subprocess.call("ipfw -q add pipe {} ip from {} {} to {} {} {}".format(idx, srcip, srcport, dstip, dstport, opt), shell=True)
                runfirst = False
            ### network shaping loop ###
            while True:
                line = nextread(f)
                if line == None:
                    break
                if len(line) != 4:
                    continue
                try:
                    bw = int(line[0])
                    delay = int(line[1])
                    plr = float(line[2])
                    queue = int(line[3])
                    cmd = "ipfw -q pipe {} config bw {}K delay {} plr {} queue {}K".format(idx, bw, delay, plr, queue)
                    subprocess.call(cmd, shell=True)
                    if idx == 100:
                        print("--------------------------------------------------")
                        subprocess.call("ipfw pipe show", shell=True)
                except ValueError:
                    print("error: invalid {}".format(line))
                time.sleep(sleep)
            
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python3 {} <data.csv>'.format(sys.argv[0]))
        exit(1)
    flush_ipfw()
    allow_ssh_rdp()
    run(100, sys.argv[1], 1)

