'''
Name:     irc.py
Function: IRC class.
By:       NotPike
'''

import socks
import socket
import sys
import re
import time
import ssl

class IRC:
 
    s = socks.socksocket()
  
    def __init__(self, server, ircPort=6667, sslBool=False, torBool=False, socksPort=9050):

        self.server = server
        self.socksPort = socksPort
        self.ircPort = ircPort
        self.sslBool = sslBool
        self.torBool = torBool
        
        ## Proxy to Local Host
        if(sslBool == True and torBool == False): #Works
            print("[+] SSL == TRUE")
            print("[!] TOR == FALSE")
            self.irc = socket.socket()
            self.irc = ssl.wrap_socket(self.irc)
        elif(sslBool == True and torBool == True): #Works
            print("[+] SSL == TRUE")
            print("[+] TOR == TRUE")
            global s
            s = socks.socksocket()
            s.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", self.socksPort, True)
        elif(sslBool ==  False and torBool == True):
            print("[!] SSL == FALSE")
            print("[+] TOR == TRUE")
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", self.socksPort, True)
            socket.socket = socks.socksocket
            self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            print("[!] SSL == FALSE")            
            print("[!] TOR == FALSE")
            self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    def bootStrap(self,botNick, channel):
        self.botNick = botNick
        self.channel = channel
        
        if(self.sslBool == True and self.torBool == True):
            from ssl import SSLError
            try:
                s.connect((self.server, self.ircPort))
            except:
                print "[!] Error on connect"
            try:
                self.irc = ssl.wrap_socket(s)
            except SSLError as e:
                print "[!] SSL Error: " + e
            self.register(botNick)
            self.nick(botNick)
            self.join(channel)
        else:
            self.connect()
            self.register(botNick)
            self.nick(botNick)
            self.join(channel)

    def restart(self):
        print "[!] Restart"
        if(self.sslBool == True and self.torBool == False): #Works
            print("[+] SSL == TRUE")
            print("[!] TOR == FALSE")
            self.irc = socket.socket()
            self.irc = ssl.wrap_socket(self.irc)
        elif(self.sslBool == True and self.torBool == True): #Works
            print("[+] SSL == TRUE")
            print("[+] TOR == TRUE")
            global s
            s = socks.socksocket()
            s.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", self.socksPort, True)
        elif(self.sslBool ==  False and self.torBool == True):
            print("[!] SSL == FALSE")
            print("[+] TOR == TRUE")
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", self.socksPort, True)
            socket.socket = socks.socksocket
            self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            print("[!] SSL == FALSE")            
            print("[!] TOR == FALSE")
            self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        print "[!] Closing connection"
        if(self.sslBool == True):
            self.irc.close()
            self.s.close()
        else:
            self.irc.close()
        
    def send(self, chan, msg):
        from ssl import SSLError
        try:
            self.irc.send("PRIVMSG " + chan + " " + msg + "\r\n")
        except:
            print "[!] Send Error"
            self.irc.close()
            self.restart()
            self.bootStrap(self.botNick, self.channel)
        time.sleep(0.2) #Prevents RecvQ exceeded error

    def connect(self):
        print "[+] Connecting to: "+self.server
        try:
            self.irc.connect((self.server, self.ircPort))
        except:
            print "[!] Somthing's broke, not sure what"

    def part(self, channel, msg):
        self.irc.send("PART " + channel + " " + msg + "\r\n")
                
    def register(self, botNick):
        print "[+] Regerstering " + botNick
        self.irc.send("USER " + botNick + " 0 * " + ":" + botNick + "\r\n")

    def nickServRegister(self, password, email):
        print "[+] Regerstering with Nick Serv"
        self.irc.send("PRIVMSG NickServ REGISTER " + password + " " + email + "\r\n")

    def nickServIdentify(self, password):
        print "[+] Identifying with Nick Serv"
        self.irc.send("PRIVMSG NickServ IDENTIFY " + password + "\r\n")

    def nick(self,botNick):
        print "[+] Nick changed to " + botNick       
        self.irc.send("NICK " + botNick + "\r\n")               

    def join (self,channel):
        print "[+] Joining " + channel       
        self.irc.send("JOIN " + channel + "\r\n")        

    def getText(self):
        text=self.irc.recv(2040)  
        if text.find('PING') != -1:                      
            self.irc.send('PONG ' + text.split() [1] + "\r\n") 
        return text

    def getIP(self,url):
        from socket import gaierror    
        try:
            return socket.gethostbyname(url)
        except socket.gaierror, e:
            return 'None'
            print "[!] Socket Error: " + e
