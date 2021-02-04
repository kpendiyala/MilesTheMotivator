import discord
import spacy
from googlesearch import search
from youtubesearchpython import VideosSearch

class Query():

    def __init__(self, clientMessage):
        self.message = clientMessage
        self.renderQuestion()

    def renderQuestion(self):
        nlp = spacy.load("en_core_web_sm")
        self.doc = nlp(self.message)
        self.tokenTexts = [t.text for t in self.doc]
        
        '''
            Here we will iterate through all the checks to find a match.
            
            checkGame will check to see if there are any words synonymous with play or game, and if so will return GAME

            checkBlacklist will check if blacklist or whitelist is within the word, and if it is, will update the blacklist/whitelist

            checkQuestion will break down the message into sentences, and find the first sentence that looks like a question. If it looks like one, it will bring up the first three google links and youtube links and will rate them based on relevancy. Finally a list of the top three relevant websites will be posted
        '''

        checklist = [
            self.checkBlackList,
            self.checkGame,
            self.checkQuestion
        ]
        for check in checklist:
            if(check()): return
        self.type = "NONE"

    def checkGame(self):
        if("game" in self.message or "play" in self.message):
            self.type = "GAME"
            return True
        return False
        
    def checkBlackList(self):
        if("blacklist" in self.message):
            self.type = "BLACKLIST"
            return True
        if("whitelist" in self.message):
            self.type = "WHITELIST"
            return True
        return False

    def checkQuestion(self):
        for token in self.doc:
            if(token.text in ["?", "what", "who", "where", "when", "why", "how"]):
                self.type = "QUESTION"
                return True
        return False
                    


    async def answerQuestion(self, channel):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.message)
        keywords = []
        for token in doc:
            if(token.pos_ in ['PROPN', 'NOUN', 'VERB', 'ADJ']): 
                keywords.append(token.text)
        keywords = ",".join(keywords)
        
        print(keywords)
        
        if(len(keywords) == 0):         
            await channel.send("Sorry, I did not understand your question. Please rephrase it.")
            return

        

        webSites = []
        gSearchLinks = list(search(keywords, tld='com', lang='en', num=2, stop=2, pause=2.0))
        ytSearchLinks = [v["title"] + " : " + v["link"] for v in VideosSearch(keywords, limit = 2).result()["result"]]

        webSites += gSearchLinks + ["\nAnd Some Videos As Well:"] + ytSearchLinks
        
        await channel.send("Here are some links related to your question:\n")
        await channel.send("```{}```".format('\n'.join(webSites)))
        

