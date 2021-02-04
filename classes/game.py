import discord
from discord.ext import commands
from random import choice, randint

class Game():
    combinations = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]

    def __init__(self, channel):
        self.channel = channel
        self.board =  ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.marked = [1,2,3,4,5,6,7,8,9]

    def printBoard(self):
        # This creates the board for the game
        return '\n ' + self.board[0] + ' | ' + self.board[1] + ' | ' + self.board[2] + "\n" + ' ' + self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5] + "\n" + ' ' + self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8]


    async def checkBoard(self):
        #This checks to see if there has been a winning position or a tie
        for c in self.combinations:
            if(self.board[c[0]] == self.board[c[1]] == self.board[c[2]]):
                if(self.board[c[0]]== "X"):
                    await self.channel.send(f"```{self.printBoard()}```\nYou win!! Good job!")
                else:
                    await self.channel.send(f"```{self.printBoard()}```\nLooks like you need more practice (and luck...)")
                return False
        else:
            return True
                    

    async def play(self, client, author):
        #The control center for the game
        isPlayer = True
        await self.channel.send("Starting Game...")

        def check(m):
            return m.author == author
        
        while await self.checkBoard():
            if(isPlayer):
                await self.channel.send(f"Enter a number from 1-9. Make sure to enter a valid number: ```{self.printBoard()}```")
                ans = await client.wait_for("message", check=check)
                
                try: 
                    ans = int(ans.content)-1
                    if(self.board[ans] in ["X", "O"] or not 0 <= ans <= 8):
                        await self.channel.send("Not sure what you mean! I'll just take my turn now.")
                    elif(ans+1 not in self.marked):
                        await self.channel.send("Cheater, that is already taken! I'll just take my turn now.")
                    else:
                        self.board[ans] = "X" 
                        self.marked.remove(ans+1)
                except ValueError: 
                    await self.channel.send("Not sure what you mean! I'll just take my turn now.")
            else:
                x = choice(self.marked)
                self.board[x-1] = "O"
                await self.channel.send(f"```{self.printBoard()}```\n I chose to select {x} as my choice. Your turn!")
            isPlayer = not isPlayer


