from types import *

'''
==SQL Header==
Packet Length: <ff 00 00>
Packet Number: <00>

==Server Greeting==
Packet Length: <ff 00 00>
Packet Number: <00>

Protocol: <0a> #protocl 10
Version: "ascii hex"
Thread ID: <0f 00 00 00> #15
Salt 1: <11 11 11 11 11 dd ee ff 00>
Server Capabilities: <ff ff>
Server Language: <08>
Server Status: <00 02>
Extended Server Capabilities: <c0 7f>
Authentication Plugin Length <00>
Unused: <00 00 00 00 00 00 00 00 00 00>
Salt 2: <35 2e 36 2e 34 30 2d 6c 6f 67 00>   x~2w'V]RcyV#
Authentatication Plugin: <6d 79 73 71 6c 5f 6e 61 74 69 76 
                          56 5f 70 61 73 73 77 6f 72 64 00> mysql_native_password 

==Login Request==
Packet Length: <c3 00 00>
Packet Number: <01>

Client Capabilities: <a6 85>
Extended Client Capabilities: <20 3f>
MAX Packet <00 00 00 01> #1677216
Charset: <2d> #utf8mb4 COLLATE
Username: <61 64 6d 69 6e 00> #admin
password: <11 62 8a 00 9a 0b 7f 3b a5 f2 56 f0 e9 dd 82 ab 04 7b 13 51>   #11628a009a0b7f3ba5f256f0e9dd82ab047b1351
Client Auth Plugin: <6d 79 73 71 6c 5f 6e 61 74 69 76 65 5f 70 61 73 73 77 6f 72 64 00> #mysql_native_password
Connection Attributes Length <71> #113 Bytes total, Every Length is 1 Byte + it's defined length
Connection Attribute Name Length: <03> #3 Bytes of data
Connection Attribute Name: <3 Byte String>
........
Connection Attribute Name Length: <10> #16 Bytes of data
Connection Attribute Name: <16 Byte String>

==Response OK==
Packet Length: <07 00 00>
Packet Number: <02>

Affected Rows: <00>
Server Status: <00 02>
Warnings: <00>
'''


class MySQL:
    def __init__(self):

        self.packetNumber = 0

        self.protocol = 10 

        self.version = "Python MySQL Server"

        self.threadID = 15

        self.serverSalts = {
            "saltOne": "12345678", 
            "saltTwo": "123456789abc"
        }

        self.serverCapabilities = {
            "Long Password": True,
            "Found Rows": True,
            "Long Column Flags": True,
            "Connect With Database": True,
            "Don't Allow database.table.column": True,
            "Can use compression protocol": True,
            "ODBC Client": True,
            "Can Use LOAD DATA LOCAL": True,
            "Ignore Spaces before '('": True,
            "Speaks 4.1 protocol (new flag)": True,
            "Interactive Client": True,
            "Switch to SSL after handshake": True,
            "Ignore sigpipes": True,
            "Knows about transactions": True,
            "Speaks 4.1 protocol (old flag)": True,
            "Can do 4.1 authentication": True
        }

        self.charsets = {
            "big5_chinese_ci": 1, 
            "latin2_czech_cs": 2, 
            "dec8_swedish_ci": 3, 
            "cp850_general_ci": 4,
            "latin1_german1_ci": 5,
            "hp8_english_ci": 6,
            "koi8r_general_ci": 7,
            "latin1_swedish_ci": 8,
            "latin2_general_ci": 9,
            "swe7_swedish_ci": 10,
            "utf8_general_ci": 33,
            "binary": 63
        }
        
        self.serverStatus = {
            "In Transaction": False,
            "AUTO_COMMIT": True,
            "More Results": False,
            "Multi Query": False,
            "Bad Index Used": False,
            "No Index Used": False,
            "Cursor Exists": False,
            "Last Row Sent": False,
            "Database Dropped": False,
            "No backslash Escapes": False,
            "Session State changed": False,
            "Query Was Slow": False,
            "PS Out Parms": False
        }        

        self.extendedServerCapabilities = {
            "Multiple statements": True,
            "Multiple results": True,
            "PS Multiple results": True,
            "Plugin Auth": True,
            "Connect attrs": False,
            "Plugin Auth LENENC Client Data": False,
            "Client can handle expired passwords": False,
            "Session variable tracking": False,
            "Deprecate EOF": False,
            "unused1": False,
            "unused2": False,
            "unused3": False,
            "unused4": False,
            "unused5": False,
            "unused6": False,
            "unused7": False
        }

        self.unused = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        self.authentaticationPlugin = "mysql_native_password"

    #Takes Dictionary and translates to bits
    def capabilitiesTranslation(self, capabilities):
        capabilities = ''.join(str(int(x)) for x in capabilities.values())[::-1]
        capabilities = int(capabilities, 2).to_bytes(2, byteorder='little')
        return capabilities

    def greetingPacket(self):
        packet = bytearray()

        #Server Protocol
        packet.extend(self.protocol.to_bytes(1, byteorder='little'))

        #Server Version
        packet.extend(self.version.encode('utf-8'))
        packet.extend((0).to_bytes(1, byteorder='little')) # \x00 padding

        #Thread ID
        packet.extend(self.threadID.to_bytes(4, byteorder='little'))

        #Salt One
        packet.extend(self.serverSalts["saltOne"].encode('utf-8'))
        packet.extend((0).to_bytes(1, byteorder='little')) # \x00 padding

        #Server Capabilities 
        packet.extend(self.capabilitiesTranslation(self.serverCapabilities))

        #Language
        packet.extend(self.charsets["utf8_general_ci"].to_bytes(1, byteorder='little'))

        #Server Status
        packet.extend(self.capabilitiesTranslation(self.serverStatus))

        #Extended Server Capabilities
        packet.extend(self.capabilitiesTranslation(self.extendedServerCapabilities))

        #Find/add length of the Authentatication Plugin
        authPluginLength = len(self.authentaticationPlugin)
        packet.extend(authPluginLength.to_bytes(1, byteorder='little'))

        #Unused block
        packet.extend(self.unused)

        #Salt Two
        packet.extend(self.serverSalts["saltTwo"].encode('utf-8'))
        packet.extend((0).to_bytes(1, byteorder='little')) # \x00 padding        

        #Authentatication Plugin
        packet.extend(self.authentaticationPlugin.encode('utf-8'))
        packet.extend((0).to_bytes(1, byteorder='little')) # \x00 padding        

        #Find Packet Length
        packetLength = len(packet)
        
        #Build Final Packet
        finalPacket = bytearray()
        finalPacket.extend(packetLength.to_bytes(3, byteorder='little'))
        finalPacket.extend(self.packetNumber.to_bytes(1, byteorder='little')) #packet number 0
        finalPacket.extend(packet)

        return finalPacket

    def getClientInfo(self, data):
        nameOffset = self.findNameOffset(data[36:]) + 36
                               
        return {
            "Packet Length: ":                data[0:3],
            "Packet Number: ":                data[3:4],
            "Client Capabilities: ":          self.getClientCapabilities(data[4:6]),
            "Extended Client Capabilities: ": self.getExtendedClientCapabilities(data[6:8]),
            "MAX Packet: ":                   data[8:12],
            "Charset: ":                      data[12:13],
            "User Name: ":                    data[36:nameOffset],
            "Password":                       data[(nameOffset+2):(nameOffset+22)],
            "Client Auth Plugin":             data[(nameOffset+22):-1]
        }

    def findNameOffset(self, data):
        j = 0
        for i in data:
            if(i.to_bytes(1,byteorder='little') == b'\x00'):
                return j
            else:
                j += 1

    def getClientCapabilities(self, data):
        return {
            "Long Password": data[0]&1 != 0,
            "Found Rows": data[0]&2 !=0,
            "Long Column Flags": data[0]&4 !=0,
            "Connect With Database": data[0]&8 !=0,
            "Don't Allow database.table.column": data[0]&16 !=0,
            "Can use compression protocol": data[0]&32 !=0,
            "ODBC Client": data[0]&64 !=0,
            "Can Use LOAD DATA LOCAL": data[0]&128 !=0,
            "Ignore Spaces before '('": data[1]&1 !=0,
            "Speaks 4.1 protocol (new flag)": data[1]&2 !=0,
            "Interactive Client": data[1]&4 !=0,
            "Switch to SSL after handshake": data[1]&8 !=0,
            "Ignore sigpipes": data[1]&16 !=0,
            "Knows about transactions": data[1]&32 !=0,
            "Speaks 4.1 protocol (old flag)": data[1]&64 !=0,
            "Can do 4.1 authentication": data[1]&128 !=0
        }
            
    def getExtendedClientCapabilities(self, data):
        return {
            "Multiple statements": data[0]&1 != 0,
            "Multiple results": data[0]&2 != 0,
            "PS Multiple results": data[0]&4 != 0,
            "Plugin Auth": data[0]&8 != 0,
            "Connect attrs": data[0]&16 != 0,
            "Plugin Auth LENENC Client Data": data[0]&32 != 0,
            "Client can handle expired passwords": data[0]&64 != 0,
            "Session variable tracking": data[0]&128 != 0,
            "Deprecate EOF": data[1]&1 != 0
        }
                           

        
        


        

