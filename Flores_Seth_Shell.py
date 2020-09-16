# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 18:26:48 2020

@author: sethf
"""
import os, sys, time, re

def exe(args): #exec
    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to execute program
        except FileNotFoundError:
            os.write(1,("File not found...").encode())
            sys.exit(1)


def run_cmd(command):
    rc = os.fork()      #create child process 
    args = command.copy()#copies the commands to the child

    if rc < 0:#fork forked up
        os.write(1, ("fork failed, returning %d\n" % rc).encode())#inform user of error that occured
        sys.exit(1)
    #continue checking for commands if the fork did not fail
    if '&' in args:
        args.remove('&')#remove & and continue the process
    if rc == 0:#child running
        if '>' in args:#redirect output
            os.close(1)#close current write
            os.open(args[-1], os.O_CREAT | os.O_WRONLY);#opens output file to write in
            os.set_inheritable(1, True)#allows child to inherit
            newArg = args[0:args.index(">")]#updates arguments to get the cmd we need to run
            exe(newArg)
        if '<' in args:#redirect input
            os.close(0)#close current read
            os.open(args[-1], os.O_RDONLY);#opens input to read from
            os.set_inheritable(0, True)#allows child to inherit
            newArg = args[0:args.index("<")]#updates arguments to get the cmd we need to run
            exe(newArg)
        if '/' in args[0]:
            prog = args[0]#get program path
            try:
                os.execve(prog,args,os.environ)#attempt running program at given path
            except FileNotFoundError:
                os.write(1,("File not found at %s\n" % prog).encode())#give user failure
        if '|' in args:
            writeCommands = args[0:args.index("|")]
            readCommands = args[args.index("|") + 1:]
            pr, pw = os.pipe()
    elif not '&' in command:
        childPidCode = os.wait()#wait and get child pid with return code
            

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
    

    if 'exit' in command:
        sys.exit(1)
        
    if len(command) > 0:#if there is a command that is not cd or exit run it
        run_cmd(command)
    
 