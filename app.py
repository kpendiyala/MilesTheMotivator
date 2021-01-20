# import discord
# from discord.ext import commands
# from googlesearch import search
# from youtubesearchpython import *
# from time import sleep
# from os import *

import discord
from discord.ext import commands
from random import choice, randint

from classes.stalker import Stalker
from classes.game import Game
from classes.query import Query


#discord setup
TOKEN = 'ODAxMTQ0OTc3MTIzMDQ5NDcy.YAcaZw.lmsqGULYwAS7ic419vT421N8kd0'

client = commands.Bot(command_prefix = "Hey Miles,")

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	

@client.event
async def on_member_join(member):
	await member.send('Welcome! My name is Miles and it is a pleasure to meet your acquantince. If you need me, just say "Hey Miles, help me!" and I\'ll be there')

@client.event
async def on_message(message):
    m = message.content.lower().rstrip()
    print(m)
    
    if(len(m) > 11 and m[:11] == "hey miles,"):
        processed = Query(m[11:]) #Query is NLP that stores keywords of the resulting message and determines type of query
        
        if(processed.type == "QUESTION"):
            processed.answerQuestion() #This will answer the question with a search query on both Google and Youtube and return an embed of top 3 searches
        
        elif(processed.type == "WHITELIST"):
            blacklist = open("/files/blacklist.txt", "w")
            blacklistContent = blacklist.readlines().split("\n")
            blacklistContent.remove(str(message.author.id))
            blacklist.write("\n".join(blacklistContent) + "\n")
        
        elif(processed.type == "GAME"):
            game = Game() #creates Game class that runs a script to play a simple random game
    
    else:
        blacklist = open("files/blacklist.txt", "r")
        b = [x.rstrip() for x in blacklist.readlines()]
        if str(message.author.id) in b:
            blacklist.close()
            return
        blacklist.close() 
        
        #8% chance to respond to someone not on the blacklist
        milesActive = randint(1,100)
        if(milesActive >= 2):
            s = Stalker(message)
            await message.channel.send(s.output) #Sends random message based on NLP (sometimes might fail due to complex nature of message)


client.run(TOKEN)

