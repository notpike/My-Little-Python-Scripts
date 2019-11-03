import socket
s = socket.socket()
s.settimeout(0.5)

print "Enter port number:",
port = int(raw_input())
#65535


try:
    s.connect(("ad.samsclass.info", port))
    print s.recv(1024)
    s.close()
except socket.error as err:
    print err
