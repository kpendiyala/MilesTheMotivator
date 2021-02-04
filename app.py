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
TOKEN = 'DID YOU REALLY THINK YOU COULD GET MY TOKEN!!!'

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
    if(len(m) > 11 and m[:11] == "hey miles, "):
        processed = Query(m[11:]) #Query is NLP that stores keywords of the resulting message and determines type of query
        
        if(processed.type == "QUESTION"):
            ctx = await client.get_context(message)
            async with ctx.typing():
                await processed.answerQuestion(message.channel) #This will answer the question with a search query on both Google and Youtube and return an embed of top 3 searches
        
        elif(processed.type == "WHITELIST"):
            blacklistR = open("files/blacklist.txt", "r")
            blacklistContent = blacklistR.read().split("\n")
            blacklistR.close(); 
            
            blacklistW = open("files/blacklist.txt", "w")
            try:
                blacklistContent.remove(str(message.author.id))
                blacklistW.write("\n".join(blacklistContent) + "\n")
            except:
                blacklistW.write("\n".join(blacklistContent))
        
            blacklistW.close()
            await message.channel.send("You have been whitelisted for stalker mode.")

        
        elif(processed.type == "BLACKLIST"):
            blacklist = open("files/blacklist.txt", "a")
            blacklist.write(str(message.author.id) + "\n")
            blacklist.close()
            await message.channel.send("You have been blacklisted from stalker mode.")
        
        elif(processed.type == "GAME"):
            game = Game(message.channel) #creates Game class that runs a script to play a simple random game
            await game.play(client, message.author)
            
        else:
            await message.channel.send("Sorry, I was unable to understand your message")

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
            ctx = await client.get_context(message)
            async with ctx.typing():
                s = Stalker(message)
            await message.channel.send(s.getOutput()) #Sends random message based on NLP (sometimes might fail due to complex nature of message)


client.run(TOKEN)

