#!/usr/bin/python3
#GroupSMS V0.1
#Twitter fixed mass messaging so this script no longer works.

#Quick Start Guide
#1.) Add creds from the 2 acounts you want to use
#2.) Change bot1 and bot2 to the twitter profile names without the @ that you have for your bots
#3.) Add photos to the 'dank_memes' folder for random pics and edit the 'msg_list.txt' for random messages. 
#4.) Research! :D

#Twitter added a new feature where you can chain up to 50 people into a twitter conversation.
#This script abuses that feature by scraping up to 48 (you and the target make 50) of a targets
#friends. You can specify how many conversation chains you want as well. The first
#chain (which is 0 when promoted at the beginning of the script) will be the first 48 friends
#scraped from the target. If you specify more then one chain (1-48) it will scrape another 48 
#(or the number specified)  friends of the target's friends.  When it's done gathering all the friends of
#the friends Bot1 will then create an initial post with a random image, targets name, a random
#hashtag, and all the targets friends until it hits the 140 character limit. Bot2 then replies to the initial
#post with another new random image, new random hashtag and more friends  until it reaches the 140
#character limit. Both bots will take turns replying to each others tweets until the chain completes 
#(all 48 users where mentioned). After that it will start the next conversation chain if specified.
#Basically you can start 49 different conversations with 48 users in each conversation.
#The target will see any fave, re tweet, and reply from the 2352 users. Hashtages and images increase
#the likelihood of interaction from outside influences (bots, people searching tags) to increase 
#the amount of notifications the target gets. 

#Because the twitter API has rate limiting, you're limited to 180 events every 15min there are
#'Tactical Pauses' in between push/get events. If you maxed out the friends and chains to 48 this
#attack #will take around 4.5-7.7hr to complete. Don’t have more chains then friends, the script will brake.
#This script also saves the scraped friends to ‘masterlist.txt’


import tweepy
import tweepy as tweepy2
import time
import random
import glob


#your bot's twitter names 
bot1 = '@bot1'
bot2 = '@bot2'


#Creds for bot1
#https://apps.twitter.com
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

#auth handling for the first acount
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


#Creds for bot2
consumer_key_2 = ""
consumer_secret_2 = ""
access_token_2 = ""
access_token_secret_2 = ""

#auth handling for 2nd acount
auth_2 = tweepy2.OAuthHandler(consumer_key_2, consumer_secret_2)
auth_2.set_access_token(access_token_2, access_token_secret_2)
api_2 = tweepy2.API(auth_2)


#Creates a list of 48 frinds from a user
def get_friends(user_id, friends, pages=1):

    print("<*> Scraping "+str(friends)+" friends from "+user_id)
    users = []
    ScreenName = []

    try:
        for user in tweepy.Cursor(api.friends, id=user_id, count=friends).pages(pages):
            users.extend(user)

            
            #Takes User data list to make a screen name list
            for name in users:
                ScreenName.append(str(name.screen_name))

            print("<*> Scraped: ",ScreenName)
            print("<*> Tactical pause, 5min") #Takes 4hr for 48freinds and 48chains, avoids rate limiting
            for i in range(5*60):
                time.sleep(1)
    
        return ScreenName
    except tweepy.TweepError as e:
        print(e.reason)


#Builds the List Of DOOOMMMM!!!! >:D
def build_list_of_doom(target, friends, chains):
    
    #Finds the last friends (friends) of the target, then finds each target friend's (chains) friends
    MasterList = []
    KeyChain = get_friends(target, friends) #The frinds from the target
    MasterList.append(KeyChain)

    for name in KeyChain:
        if chains != 0:
            foaf = get_friends(name, friends) #foaf == Friend of a friend
            MasterList.append(foaf)
            chains -= 1
        else:
            break

    #Saves MasterList to a file
    print("<*> Saving users to 'masterlist.txt'")
    SaveGame = open('masterlist.txt', 'w')
    for name in MasterList:
        SaveGame.write("%s\n" % name)
    SaveGame.close()

    return MasterList


def rando_img():
    
    PicList = glob.glob("dank_memes/*")
    RandoChoice = random.randint(0,len(PicList))
    return PicList[RandoChoice]


def rando_msg():
    
    wordlist = []
    with open('msg_list.txt') as file:
        for line in file:
            wordlist.append(line.strip())
    choice = random.randint(0,len(wordlist)-1)
    return wordlist[choice]
    
       
def fire_the_missles(message, target):

    #works it's way down the list
    for chain in range(len(message)):

        msg = ''
        new_chain = 1
        reply = 0
        rmsg = rando_msg()

        
        for name in message[chain]:

            #Begines the chain with '@target <message> @freinds
            if new_chain == 1:
                msg += "@"+target+" "
                msg += rmsg+' ' #random message
                msg += "@"+name+" "
                new_chain = 0
                botname = '' #don't count the length of the bot's reply to eachother


            #Adds a freind after each loop until the message reaches 140 characters
            #The +3 is for the '@'s
            elif len(msg)+len(name)+len(botname)+3 <= 140:
                msg += "@"+name+" "
                

            #When the message reaches 140 characters, it sends it off and starts the reply messages
            #Adds a message at the begining of each reply    
            else:
                post_message(msg, reply) #send the message off
                reply = 1
                msg = ''

                #switch back and forth from bot names for msg length
                if botname == bot1 or botname == '':
                    botname = bot2
                else:
                    botname = bot1

                #new conversation chain, resets    
                if new_chain == 0:
                    rmsg = rando_msg()
                    msg += rmsg+" "
                    
                pass
        post_message(msg, reply)




           
bot = 1 #bad programing on my part lol, controls wich bot goes first
def post_message(message, reply):

    global bot
    
      pause = random.randint(1,60)
      print("<*> Tactical pause, "+str(pause)+"sec...")
      for i in range(pause):
          time.sleep(1)

    try:
        
        if reply == 0:
            bot = 1
            print("<*> Bot 1 Posted: "+message+'\n')
            #api.update_status(message)
            api.update_with_media(rando_img(),message)

        else:
            if bot == 1:
                tweetID = api.user_timeline()[0].id #last tweet from bot 1
                #api_2.update_status(message, in_reply_to_status_id=tweetID)
                api_2.update_with_media(rando_img(),bot1+" "+message, in_reply_to_status_id=tweetID)
                print("<*> Bot 2 Posted: "+message+"\nin_reply_to_status_id="+str(tweetID)+"\n")
                bot = 0

            else:
                tweetID2 = api_2.user_timeline()[0].id #last tweet from bot 2
                #api.update_status(message, in_reply_to_status_id=tweetID2)
                api.update_with_media(rando_img(),bot2+" "+message, in_reply_to_status_id=tweetID2)
                print("<*> Bot 1 Posted: "+message+"\nin_reply_to_status_id="+str(tweetID2)+"\n")
                bot = 1
                
    except tweepy.TweepError or tweepy2.TweepError as e:
        print(e.reason)


def MissleCommand(target, friends, chains):
    MasterList = build_list_of_doom(target, friends, chains)
    fire_the_missles(MasterList, target)



if __name__ == "__main__":
    print('GroupSMS V0.1')
    target = input("Who is your target? (Name without the '@'): ")
    friends = int(input("How many friends should we scrape from the target?: "))
    chains = int(input("How many conversation chains do you want to have?: "))
    MissleCommand(target, friends, chains)
