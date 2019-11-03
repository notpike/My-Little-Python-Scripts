import socket

#print "Enter port number:",
#port = int(raw_input())
#65535


def portFind(port):
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect(("ad.samsclass.info", port))
        print s.recv(1024)
        s.close()
    except socket.error as err:
        print err


#PortScan
#for i in range(1000, 65000,1000):
#    print "Port: " + str(i)
#    portFind(i)

#PortKnock
#portOrder = [3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900]
#for i in portOrder:
#    portFind(i)
#portFind(3003)
