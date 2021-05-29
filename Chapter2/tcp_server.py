import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# creating socket object, IPv4/hostname, TCP

server.bind((bind_ip, bind_port))
# setting ip and port for the server to listen on

server.listen(5)
# server start listening with a max of 5 connections

print("[*] Listening on %s:%d" % (bind_ip, bind_port))


def handle_client(client_socket):

    request = client_socket.recv(1024)

    print ("[*] Received: %s" % request)
    # printing what the client sends

    client_socket.send(b"ACK!")
    # sending back a packet

    client_socket.close()

while True:

    client, addr = server.accept()

    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

    client_handler = threading.Thread(target = handle_client, args = (client,))
    client_handler.start()
    # client thread that handles incoming data
