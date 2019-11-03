'''
Name:     Tor.py
Function: Tor controller class.
By:       NotPike
'''

import sys
import stem
from stem import Signal
from stem.control import Controller

class TOR:

    def __init__(self, controlPort, torKey):
        self.CONTROL_PORT = controlPort
        self.TOR_KEY      = torKey

    def torConnect(self):
        ## Connect to Controler
        try:
            with Controller.from_port(port = self.CONTROL_PORT) as controller:

                ## TOR Auth
                print("[+] Authing the TORZ")
                try:    
                    controller.authenticate(self.TOR_KEY)
                except stem.connection.PasswordAuthFailed:
                          print("[!] Password Sucked...")
                          print("[+] Exiting")
                          sys.exit(1)

                ## NEWNYM New Path Threw TOR
                print("[+] New Pathway Threw The TORZ")
                flag = True
                while(flag):
                    if(controller.is_newnym_available()):
                        controller.signal(Signal.NEWNYM)
                        flag = False
                        break
                    else:
                        ans = input("[!] NEWNYM not available. Wait %s sec? [Y/N]: ")
                        time = controler.get_newnym_wait()
                        ansFlag = true
                        while(ansFlag):
                            if(ans.lower() == 'y'):
                                timer = 0
                                while(timer < time):
                                    time.sleep(1)
                                    timer += 1
                            elif(ans.lower() == 'n'):
                                ans2Flag = True
                                while(ans2Flag):
                                    ans2 = input("[+] Continue with last NEWNYM? [Y/N]: ")
                                    if(ans2.lower() == 'y'):
                                        ans2Flag = False
                                        ansFlag  = False
                                        break
                                    elif(ans2.lower() == 'n'):
                                        print("[+] Exiting")
                                        sys.exit(1)
                                    else:
                                        print("[!] Bad Input")
                            else:
                                print("[!] Bad Input")

        except stem.SocketError as e:
            print("[!] Unable to connect to TOR on port %s: %s" %(self.CONTROL_PORT, e))
            print("[+] Exiting")
            sys.exit(1)
                         
