#!/usr/bin/python

import sys

if len(sys.argv) != 3:
  print "Usage: ./xor1 infile outfile k"
  print "k is a one-character XOR key"
  print "For hexadecimal keys, use $'\\x01'"
  exit()

f = open(str(sys.argv[1]), "rb")
g = open(str(sys.argv[2]), "a")
#k = ord(sys.argv[3])

abc = list(map(chr, range(97, 123)))

for i in range(0, len(abc)):

    try:
        byte = f.read(1)
        while byte != "":
            xbyte = ord(byte) ^ i
            g.write("==="+str(i)+"===\n")
            g.write(chr(xbyte))
            byte = f.read(1)
    finally:
        f.close()

g.close()
