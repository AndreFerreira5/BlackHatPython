import socket

target_host = input("Enter the target host: ")
target_port = int(input("Enter the target port: "))


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# creating a socket object / AF_INET for IPv4 address or hostname / SOCK_STREAM for TCP client

client.connect((target_host,target_port))
# connecting the client

client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
# sending some data

response = client.recv(4096)
# receiving some data

client.close()

print ("[*] Received: %s" % response)
