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
    print("-l --listen              - listen on [host]:[port] for \nincoming connections")
    print("-e --execute=file_to_run - execute the given file upon \nreceiving a connection")
    print("-c --command             - initiate a command shell")
    print("-u --upload=destination  - upload a file and write to \n[destination] upon receiving \na connection")
    print()
    print()
    print("Examples: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)


# function for incoming connections
def server_loop():
    global target
    global port

    # if no target is set we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:

        client_socket, addr = server.accept()

        # thread init for our new client
        client_thread = threading.Thread(target = client_handler, args = (client__socket,))
        client_thread.start()



# function for running a command and returning its output
def run_command():

    #trim the newline
    cmd = cmd.rstrip()

    # run the given command and get the output back
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    # send the output back to the client
    return output


# function for handling incoming client connections
def client_handler():
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):

        # read in all of the bytes and write to our destination
        file_buffer = ""

        # keep reading data until none is available
        while True:

            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # taking the bytes and tryin to write them out
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer.encode('utf-8'))
            file_descriptor.close()

            # acknowledge that the file has been written
            client_socket.send("successfully saved file to %s\r\n" % upload_destination)

        except OSError:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)


    # check for command execution
    if len(execute):

        # run the command
        output = run_command(execute)

        client_socket.send(output)


    # loop if command shell was requested
    if command:

        while True:

            # show a simple prompt
            client_socket.send("<BHP:#> ".encode('utf-8'))

            # receive until enter has been pressed
            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # enter has been pressed so exec it and returning the results
            responde = run_command(cmd_buffer)

            # sending back the response
            client_socket.send(response)

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
    except getopt.GetoptError as err:
        print (str(err))
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
