import sys
import socket
import getopt
import threading
import subprocess


# global variables
listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0


def usage():

    print("BHP Net Tool")
    print()
    print("Usage: bhpnet.py -t target_host -p port")
    print("-l --listen              - listen on [host]:[port] for \n
                                      incoming connections")
    print("-e --execute=file_to_run - execute the given file upon \n
                                      receiving a connection")
    print("-c --command             - initiate a command shell")
    print("-u --upload=destination  - upload a file and write to \n
                                      [destination] upon receiving \n
                                      a connection")
    print()
    print()
    print("Examples: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)


def main():

    global listen
    global command
    global upload
    global execute
    global target
    global upload_destination
    global port

    if not len(sys.argv[1:]):
       usage()
    
    # red the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:"
