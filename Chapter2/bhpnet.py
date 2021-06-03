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


def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # establishing a connection w/ defined target host
        client.connect((target, port))
    
        if len(buffer):
            client.send(buffer.encode('utf-8'))

        while True:

            # wait for data back
            recv_len = 1
            response = b""

            while recv_len:

                data     = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response.decode('utf-8'), end=' ')

            # wait for more input
            buffer = input("")
            buffer += "\n"

            # send it off
            client.send(buffer.encode('utf-8'))

    except socket.error as exc:   
    
        # catching error and printing it
        print("[*] Exception! Exiting.")
        print(f"[*] Caught exception socket.error: {exc}")

        # close connection
        client.close()

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
    
    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except: getopt.GetoptError as err:
        print str(err)
        usage()


    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"


    if not listen and len(target) and port > 0:

        buffer = sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()
