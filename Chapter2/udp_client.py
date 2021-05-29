import socket

target_host = input("Enter the target host: ")
target_port = int(input("Enter the target port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# creating a socket object / AF_INET for IPv4 address or hostname / SOCK_DGRAM for UDP

client.sendto(b"AAABBBCCC", (target_host,target_port))
# sending some data

data, addr = client.recvfrom(4096)
# receiving some data

client.close()

print (data)
