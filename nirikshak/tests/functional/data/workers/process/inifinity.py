#!/usr/bin/python
import socket
import sys


HOST = 'localhost'
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
except socket.error, msg:
    sys.exit()

s.listen(10)
conn = None
while True:
    conn, addr = s.accept()
    conn.close()
