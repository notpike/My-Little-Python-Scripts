import hashlib
#passwd = raw_input('Enter password: ')
#print hashlib.new('md4', passwd)

#NTLM
#print hashlib.new('md4', passwd.encode('utf-16le')).hexdigest()

#CCSF-username-PIN

user = {"ming":"52C4859C0617E4A8FEC24BA890C5FC57",
        "mohammed":"39057EF3A9FE57D98E7A9BAB7CD2F4F9",
        "sam":"19A641D2520B983ABB7C931CEFF933FA"}




for name, haxHash in user.iteritems():
    pname = name
    #print name + haxHash
    for pin in range(100):
        if pin < 10:
            pin = "0" + str(pin)
        #print pin
        name = "CCSF-" + pname + "-" + str(pin)
        msHash = hashlib.new('md4', name.encode('utf-16le')).hexdigest()
        #print msHash
        #print name +" " + haxHash.lower()
        if msHash == haxHash.lower():
            print "I got " + name + "Pin " + str(pin) + " hash: " + msHash
            name = ""
        else:
            name = ""
            pass
