import hashlib
#passwd = raw_input('Enter password: ')
#print hashlib.new('md5', passwd)


user = {"ming":"7621eca98fe6a1885d4f5f56a0525915",
        "mohammed":"b2173861e8787a326fb4476aa9585e1c",
        "sam":"42e646b706acfab0cf8079351d176121"}




for name, haxHash in user.iteritems():
    pname = name
    #print name + haxHash

    flag = True
    hashCount = 1
    while flag:
        hashCount +=1
    
        for pin in range(100):
            if pin < 10:
                pin = "0" + str(pin)
            #print pin
            name = "CCSF-" + pname + "-" + str(pin)
            msHash = name
    
            for i in range(hashCount):
                msHash = hashlib.new('md5', msHash).hexdigest()
            #print msHash
            #print name +" " + msHash
            if msHash == haxHash.lower():
                print "I got " + name + "Pin " + str(pin) + " hash: " + msHash
                name = ""
                flag = False
            else:
                name = ""
                pass
