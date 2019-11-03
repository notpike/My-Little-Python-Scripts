#!/usr/bin/python3

'''
Program Name: CryptBot.py
Writen By:    NotPike
Function:     One Time Pad for Twitter

One Time Pad logic based off of jailuthra's code
https://github.com/jailuthra
'''

#Import
import tweepy
import argparse
import binascii
import itertools
import base64
import os
import datetime

#Twitter Creds
twitterName = ""
consumerKey = ""
consumerSecret = ""
accessToken = ""
accessTokenSecret = ""

#Twiter Auth
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#Msg Formating
STARTMSG = "-----BEGIN MESSAGE-----"
ENDMSG   = "------END MESSAGE------"

def main():
    #Command Arguments
    parser = argparse.ArgumentParser(description="Crypt Twitter Bot by NotPike")
    parser.add_argument('-dm', dest="directMsg",help='Send an Direct message. -dm')
    parser.add_argument('-e', dest="encrypt",help="encrypted. -e <'plain text msg'>")
    parser.add_argument('-d', dest="decrypt",help='decrypt. -d <encrypted msg>')
    parser.add_argument('-k', dest="key",help='key. -k <key>')
    parser.add_argument('-kg', dest="keyGen",help='key gen. -kg <key length>')
    parser.add_argument('-l', dest="log",help='log. -l <log.csv>')
    arguments = parser.parse_args()

    #Dem Arument Logic
    if(arguments.directMsg and arguments.encrypt and arguments.key and arguments.log):
        msg = arguments.encrypt
        key = arguments.key
        user = arguments.directMsg
        cryptMsg, key = tweetDM(user,msg,key) 
        fileWrite(arguments.log,user,key,msg,cryptMsg)
    elif(arguments.directMsg and arguments.encrypt and arguments.key):
        msg = arguments.encrypt
        key = arguments.key
        user = arguments.directMsg
        tweetDM(user,msg,key)
    elif(arguments.directMsg and arguments.encrypt and arguments.log):
        msg = arguments.encrypt
        user = arguments.directMsg
        cryptMsg, key = tweetDM(user,msg)
        fileWrite(arguments.log,user,key,msg,cryptMsg)
    elif(arguments.directMsg and arguments.encrypt):
        msg = arguments.encrypt
        user = arguments.directMsg
        tweetDM(user,msg)

    elif(arguments.encrypt and arguments.key and arguments.log):
        msg = arguments.encrypt
        key = arguments.key
        cryptMsg, key = tweet(msg,key)
        fileWrite(arguments.log,'',key,msg,cryptMsg)
    elif(arguments.encrypt and arguments.key):
        msg = arguments.encrypt
        key = arguments.key
        tweet(msg,key)
    elif(arguments.encrypt and arguments.log):
        msg = arguments.encrypt
        cryptMsg, key = tweet(msg)
        fileWrite(arguments.log,'',key,msg,cryptMsg)       
    elif(arguments.encrypt):
        msg = arguments.encrypt
        tweet(msg)

    elif(arguments.decrypt and arguments.key):
        msg = arguments.decrypt
        key = arguments.key
        print(oneTimePadDecrypt(msg,key))
    elif(arguments.keyGen):
        key = keyGen(int(arguments.keyGen))
        print("Key: " + key + "\n")
    elif(arguments.decrypt):
        print("Missing -k")
    elif(arguments.directMsg):
        print("Missing -e")

def fileWrite(name,to,key,msg,cryptMsg):
    time = datetime.datetime.now().strftime('%H:%M:%S')
    if os.path.exists(name):
        file = open(name,"a")
        file.write(time + "," + to +"," + str(key) + "," + str(msg) + "," + str(cryptMsg) + "\n")
        file.close()
    else:
        file = open(name,"w")
        file.write("TIME STAMP,TO:,KEY,PLAINTEXT MSG,ENCRYPTED MSG\n")
        file.write(time + "," + to +"," + str(key) + "," + str(msg) + "," + str(cryptMsg) + "\n")
        file.close()      

def oneTimePadEncrypt(msg,key = 'nokey'):
    if(key == 'nokey'):
        key = keyGen(len(msg))
    print("\nKey: " + key + "\n")
    cipher = xor(msg, key)
    cipher = (binascii.hexlify(cipher.encode())).decode()
    return cipher, key

def oneTimePadDecrypt(cipher,key):
    cipher = (binascii.unhexlify(cipher.encode())).decode()
    msg = xor(cipher, key)
    return msg

def xor(a,b):
    xorred = ''.join([chr(ord(x)^ord(y)) for x, y in zip(a, itertools.cycle(b))])
    return xorred

def keyGen(msgLength):
    key = base64.b64encode(os.urandom(msgLength)).decode('utf-8')
    return key

def tweet(msg,key = 'nokey'):
    cryptMsg, key = oneTimePadEncrypt(msg,key)
    #Checks to see if encrypted msg is larger then 240 chr
    #len(STARTMSG+ENDMSG) acounts for the begin and end of msg
    if(len(cryptMsg) > 240 - len(STARTMSG+ENDMSG)):
        print("Message is too long")
    else:
        print(STARTMSG + "\n" + cryptMsg + "\n" + ENDMSG + "\n")
        api.update_status(STARTMSG + "\n" + cryptMsg + "\n" + ENDMSG)
    return cryptMsg, key

def tweetDM(user,msg,key = 'nokey'):              
    cryptMsg, newKey = oneTimePadEncrypt(msg,key)
    if(len(cryptMsg) > 240 - len(STARTMSG+ENDMSG)):
        print("Message is too long")
    else:
        print(STARTMSG + "\n" + cryptMsg + "\n" + ENDMSG + "\n")
        api.send_direct_message(user,'','',STARTMSG + "\n" + cryptMsg + "\n" + ENDMSG)
    return cryptMsg, newKey 

if __name__ == "__main__":
    main()
