#!/usr/bin/python3.7

#MySQL server

import socketserver
from mysql import *

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        sql = MySQL()
        
        self.request.sendall(sql.greetingPacket())
        self.data = self.request.recv(1024)
        print("{} wrote: ".format(self.client_address[0]))
        print(sql.getClientInfo(self.data))



if __name__ == "__main__":
    HOST = "localhost"
    PORT = 3306

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()

