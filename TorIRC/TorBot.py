#!/usr/bin/python

'''
Name:     TorBot.py
Function: Main program.
By:       NotPike
'''

##TODO
#Command Line
#Threading
#Better IRC objects
#Actual functions of doing things
#Better Shutdown Process

import shodan
import re
import time
from IRC import *
from Tor import *

## Variables
torKey            = ''
shodanKey         = ''
botPassword       = ''

serverAddress     = '' 
channel           = ''
controlPort       = 9051
socksPort         = 9050
ircPort           = 6697

ownerNick         = 'NotPike'
botNick           = 'PikeBot'
email             = ''
killWord          = 'My voice is my passport. Verify Me'
partMsg           = 'Bye'

def main(torBool,sslBool):
    global shodanAPI
    global irc
    global botNick
    global channel
    global botPassword
    global email
    
    ##Shodan
    shodanAPI = shodan.Shodan(shodanKey)
    
    ##TOR
    if(False): 
        tor = TOR(controlPort, torKey)
        tor.torConnect()

    ##IRC
    irc = IRC(serverAddress, ircPort, True, True, socksPort)
    irc.bootStrap(botNick, channel)

    flag = True
    while flag:
        text = irc.getText()
        if(text != None): 
            print text

            #NickServ and Bot Name
            if("NOTICE" in text and "This nickname is registered" in text):
                irc.nickServIdentify(botPassword)
            elif("NickServ" in text and "PRIVMSG" in text and "is not a registered nickname" in text):
                irc.nickServRegister(botPassword,email)
            elif("JOIN :You have not registered\r\n" in text):
                irc.nickServRegister(botPassword,email)
                irc.nickServIdentify(botPassword)
                irc.nick(botNick)
                irc.join(channel)
            elif("PRIVMSG" in text and channel in text and "Nickname is already in use" in text):
                botNick = "IfNot"+botNick
                irc.nick(botNick)

            #Bot Functions
            elif("PRIVMSG" in text and channel in text and "?help" in text):
                irc.send(channel, "?help, ?about, ?shodan host")
            elif("PRIVMSG" in text and channel in text and "?shodan host" in text):
                try:
                    user = re.search(r':(.*)!', text).group(1)
                    host = re.search(r'\?shodan host (.*)\r\n', text).group(1)
                    print '[+] User:' + user
                    print '[+] URL: ' + host 
                except AttributeError:
                    pass            
                shodanHost(host, user)
            elif(("JOIN :" + channel + "\r\n") in text and "NOTICE" not in text and botNick not in text):
                try:
                    user = re.search(r':(.*)!', text).group(1)
                    irc.send(channel, "hey " + user)                
                except AttributeError:
                    pass                  
            elif("PRIVMSG" in text and channel in text and "?about" in text):
                irc.send(channel, "PikeBot V0.1 By:NotPike")
            elif("PRIVMSG" in text and channel in text and killWord in text):
                try:
                    user = re.search(r':(.*)!', text).group(1)
                    if(user == ownerNick):
                        flag = False
                        irc.part(channel, partMsg)
                        irc.close()
			sys.exit(0)
                    else:
                        irc.send(channel, "try harder")
                except AttributeError:
                    pass   

            #Error handling
            elif("ERROR :Closing link:" in text):
                print "[!] Reconnecting..."
                irc.close()
                irc.restart()
                irc.bootStrap(botNick, channel)

        else:
            print "[!] Reconnecting..."
            irc.close()
            irc.restart()
            irc.bootStrap(botNick, channel)

def shodanHost(address,user):
    print "[+] Shodan Host\n"
    
    if(address):
        ip = irc.getIP(re.search(r'(http[s]?://)?(.*)', address).group(2))
        print '[+] IP: ' + str(ip)
    else:
        irc.send(channel, "[!] Missing Address\n")    

    # Lookup the host
    if(ip == 'None'):
        irc.send(channel, "[!] Bad Address\n")
    else:
        try:
            host = shodanAPI.host(ip)
            irc.send(user, "IP: " + str(host['ip_str']))
            irc.send(user, "Org: " + str(host.get('org', 'n/a')))
            irc.send(user, "OS: " + str(host.get('os', 'n/a')))

            # Creates list of lines
            for item in host['data']:
                out = []
                buff = []
                irc.send(user, "Port: " + str(item['port']))
                for line in item['data']:
                    if line == '\n':
                        out.append(''.join(buff))
                        buff = []
                    else:
                        buff.append(line)
                else:
                    if buff:
                        out.append(''.join(buff))

                # Makes sure each line is < 512        
                for msg in out:
                    if(len(msg) > 512): 
                        print "[+] " + str(msg[:511])
                        irc.send(user, str(msg[:511]))
                        print "[+] " + str(msg[511:])
                        irc.send(user, str(msg[511:]))
                    else:
                        print "[+] " + str(msg)
                        irc.send(user, str(msg))

        except shodan.APIError, e:
            irc.send(channel, "[!] " + str(e))            

if __name__ == "__main__":
    try:
        main(True,True)        
    except KeyboardInterrupt:
        irc.part(channel, "Bye")
        irc.close()
        
