#!/usr/bin/env python

import socket

def myMod(denum,num):
  counter = 0
  current = num
  while current >= 0:
    current = round(current - denum,2)
    if current >=0:
      counter = counter + 1
    else:
      current = round(current + denum,2)
      return (current,counter)
  
TCP_IP = '216.165.2.33'
TCP_PORT = 8000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def myRound():
  data = s.recv(BUFFER_SIZE)  # 10000$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(10000.00,float(data.splitlines()[1][1:]))
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""
  
  data = s.recv(BUFFER_SIZE) # 5000$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(5000.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 1000$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(1000.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 500$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(500.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 100$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(100.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 50$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(50.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 20$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(20.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 10$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(10.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 5$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(5.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 1$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(1.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.50$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.50,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.25$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.25,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.10$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.10,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.5$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.05,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.01$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.01,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

def myFirstRound():
  data = s.recv(BUFFER_SIZE)  # 10000$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(10000.00,float(data.splitlines()[0][1:]))
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""
  
  data = s.recv(BUFFER_SIZE) # 5000$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(5000.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 1000$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(1000.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 500$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(500.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 100$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(100.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 50$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(50.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 20$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(20.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 10$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(10.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 5$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(5.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 1$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(1.00,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.50$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.50,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.25$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.25,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.10$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.10,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.5$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.05,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

  data = s.recv(BUFFER_SIZE) # 0.01$ bills
  print "=== Received Data ==="
  print data
  print "=== End Received Data ==="
  print ""
  values = myMod(0.01,values[0])
  s.send(str(values[1])+"\r\n")
  print "Sent value: " + str(values[1])
  print "Current money: " + str(values[0])
  print ""

myFirstRound()
while 1:
  myRound()
