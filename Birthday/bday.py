#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from termcolor import colored

cake = '''
            ,:/+/-
            /M/              .,-=;//;-
       .:/= ;MH/,    ,=/+%$XH@MM#@:
      -$##@+$###@H@MMM#######H:.    -/H#
 .,H@H@ X######@ -H#####@+-     -+H###@X
  .,@##H;      +XM##M/,     =%@###@X;-
X%-  :M##########$.    .:%M###@%:
M##H,   +H@@@$/-.  ,;$M###@%,          -
M####M=,,---,.-%%H####M$:          ,+@##
@##################@/.         :%H##@$-
M###############H,         ;HM##M$=
#################.    .=$M##M$=
################H..;XM##M$=          .:+
M###################@%=           =+@MH%
@#################M/.         =+H#X%=
=+M###############M,      ,/X#H+:,
  .;XM###########H=   ,/X#H+:;
     .=+HM#######M+/+HM@+=.
         ,:/%XM####H/.
              ,.:=-.
              
'''

msg = "> Happy Birthday 色辺 つこ! :D \n"

if __name__ == "__main__":
    os.system('clear')
    print(colored(cake, 'green'))
    print(colored(msg, 'green', attrs=['reverse', 'blink']))
