import spacy
from random import choice

class Stalker():
    
    def __init__(self, clientMessage):
        self.message = clientMessage.content
        self.author = clientMessage.author.name
        self.renderMessage()
        
    def renderMessage(self):
        nlp = spacy.load("en_core_web_sm")
        self.doc = nlp(self.message)
        
        '''
            Here we will iterate through all the checks to find a match.
            
            checkMedia checks for if the link is a URL and if it is, what 
            URL type is it
            
            checkGame checks for if any noun symbolizes a game to return
            a relevant video related to that game
            
            checkCeleb checks for if any celeberties are mentioned, and if
            they are, will return a URL specifying information on that celeb
            
            The final function of the list should ALWAYS be self.final. This
            will prefill the output with a generic line as a last resort.
        '''
        checklist = [
            self.checkMedia,
            self.checkGame,
            self.checkCeleb,
            self.checkQuestion,
            self.final
        ]
        for check in checklist:
            if(check(doc)): break
    
    def checkMedia(self):
        pass
    
    def checkGame(self):
        pass

    def checkCeleb(self):
        pass
    
    def checkQuestion(self):
        for token in doc:
            if(token.text == "?"):
                self.output = "If you have a question, please feel free to let me know by doing Hey Miles, <question?>. Have a good day!"
                return True
        return False
    
    def final(self):
        flist = [
            f"Hey {self.author}, how is it going?",
            f"What's Up, {self.author}",
            "An interesting conversation!",
            f"I hope you've completed your homework {self.author}"
        ]
        return choice(flist)

            
            