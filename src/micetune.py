#!/usr/bin/python
#
# -*- coding: utf-8 -*-
#
# micetune script by Lars Ole Pontoppidan 2017-11-10, updated 2018-03-08
#
# Intended to be Python 2 and 3 compatible
#

import os
import re
import sys

# Speed value examples:
#   0.5  :  Half pointer speed
#   1    :  Unchanged pointer speed
#   1.5  :  150% pointer speed

speeds = {
u'Lenovo USB Receiver': 0.75,
u'Logitech M315/M235': 1.2,
u'Logitech M505/B605': 0.7
}

def getPointers():
    raw = os.popen("xinput --list").read()
    
    # For Python 2, UTF decoding must be done manually
    if sys.version_info.major < 3:
        raw = raw.decode("UTF-8")
        
    # The regex picks name and id from xinput list output lines with type slave pointer.
    # \u21b3 is unicode for the right arrow used in the list
    r1 = re.compile(u"\u21b3 (.*?)\s*id\=(\d+)\s+\[slave\s+pointer")
    
    p = []    
    for match in re.finditer(r1, raw):
        p.append(match.groups())
    return (raw, p)

def setSpeed(id, speed, test):
    inv_speed = 1.0 / speed
    cmd = "xinput --set-prop %d 'Coordinate Transformation Matrix' 1.0 0.0 0.0  0.0 1.0 0.0  0.0 0.0 %f" % (id, inv_speed)
    if test:
        print(cmd)
    else:
        os.popen(cmd)

def usage():
    print("micetune: A script for setting individual mouse pointer speeds\n"
          "\n"
          "Invalid arguments, syntax: micetune {list, test, run}")

if __name__ == "__main__":    
    if len(sys.argv) < 2:
        usage()
    elif sys.argv[1] == 'list':
        (raw, pointers) = getPointers()
        print("This is the output from: 'xinput --list'\n\n" + raw)
        print("Pointer devices identified:")
        for (name, id_str) in pointers:
            print("'%s'" % (name))
            
        print("\nScript configuration:")
        for key, value in speeds.items():
            print("'%s' = %f" % (key, value))
            
    elif sys.argv[1] == 'test':        
        (raw, pointers) = getPointers()
        for (name, id_str) in pointers:
            if name in speeds:
                setSpeed(int(id_str), speeds[name], True)

    elif sys.argv[1] == 'run':        
        (raw, pointers) = getPointers()
        for (name, id_str) in pointers:
            if name in speeds:
                setSpeed(int(id_str), speeds[name], False)
    else:
        usage()


