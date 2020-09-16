# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 18:26:48 2020

@author: sethf
"""


import os, sys, time, re

while 1: #keep running our mini shell untill forced exit

    pid = os.getpid()

    if 'PS1' in os.environ: #use the ps1 promt
        os.write(1, (os.environ['PS1']).encode())
        try:
            command = [str(n) for n in input().split()]
        except EOFError:    #catch error
            sys.exit(1)
    else:
        os.write(1, ('$>> ').encode()) #if ps1 is not present use $>>
        try:
            command = [str(n) for n in input().split()]
        except EOFError:    #if err occurs then end prog
            sys.exit(1)

    if 'cd' in command:
        try:#if cd in comand try to change directory
            os.chdir(command[1])
        except FileNotFoundError:
            os.write(1, ("File not found").encode())
            os.write(1,("\n").encode())#newline
            continue#restart shell
        os.write(1,("\n").encode())#newline
        continue#restart shell
    
    if 'ls' in command:
        try:
            myDir = os.listdir()
            for i in range(len(myDir)):
                if i%4 == 0:
                    os.write(1,("\n").encode())#every 4 listed directories make a new line
                os.write(1,(str(myDir[i]) + "\t").encode())
        except:
            os.write(1,("Error occured while listing current dir...\n").encode())
            os.write(1,("\n").encode())#newline
            continue
        os.write(1,("\n").encode())#newline
        continue#restart shell
    if 'exit' in command:
        sys.exit(1)
        
    