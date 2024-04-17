#!/usr/bin/python
import os
import subprocess

def cmd(command):
    print(command)
    return subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)

def cmd_and_wait(command):
    print(command)
    cmd_result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, preexec_fn = os.setsid)
    cmd_result.wait()
    output = cmd_result.stdout.readlines()
    err = cmd_result.stderr.readlines()
    return output, err


