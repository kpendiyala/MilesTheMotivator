import spacy
from random import choice
from wikipedia import *

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
			
			checkPropN checks for a proper Noun that we can extract a Wiki
			Summary for.
			
			The final function of the list should ALWAYS be self.final. This
			will prefill the output with a generic line as a last resort.
		'''
		checklist = [
			self.checkMedia,
			self.checkPropN,
			self.checkQuestion,
		]
		print(self.message)
		for check in checklist:
			if(check()): return
		self.final()
			

	def checkMedia(self):
		for token in self.doc:
			if(token.like_url):
				if(token.text in "youtube,crunchyroll,twitch"):
					choices = [
						"An interesting listen indeed!",
						"Personally, I did not enjoy that video :(",
						"This intrigues me. I will save this video for future reference."
					]
					self.output = choice(choices)
					return True
				elif(token.text in "spotify,soundcloud"):
					choices = [
						"An interesting listen indeed!",
						"You have good taste!",
						"What an interesting genre! I will save this piece for later."
					]
					self.output = choice(choices)
					return True
				elif(token.text.endswith(".gif")):
					choices = [
						"I am having trouble analyzing this meme. Will save for later.",
						"An amusing meme indeed!",
						"Meming when you have work to do. Tsk Tsk..."
					]
					self.output = choice(choices)
					return True
			return False


	def checkPropN(self):
		propList = []
		for token in self.doc:
			print(token.pos_)
			if(token.pos_ == "PROPN"):
				propList.append(token.text)
			elif(len(propList) > 0 and token.text.title() == token.text and token.pos_ not in ["SYM", "PUNCT"]):
				propList.append(token.text)
			elif(len(propList) > 0):
				break

		if(len(propList) == 0): return False
		print(" ".join(propList))
		
		temp = suggest(" ".join(propList))
		info = ""
		for i in range(10):
			try:
				info = summary(choice(search(temp)), sentences=4)
				break
			except:
				pass
		else: return False
		self.output = "I see you are taking about {}. Here is some information I found on the subject:\n\n{}".format(
			temp.title(),
			info
		)
		return True

	def checkQuestion(self):
		for token in self.doc:
			if(token.text == "?"):
				self.output = "If you have a question, please feel free to let me know by doing Hey Miles, <question?>. Have a good day!"
				return True
			return False

	def final(self):
		flist = [
			f"Hey {self.author}, how is it going?",
			f"What's up {self.author}",
			"An interesting conversation!",
			f"I hope you've completed your homework {self.author}"
		]
		self.output = choice(flist)
		return True

	def getOutput(self):
		return self.output
			
            