from discord import Client
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from discord.utils import get
from os import environ as env

CHANNEL_ID = env.get("CHANNEL_ID", 714790972051030096)
TARGET_REACTIONS_COUNT = env.get("TRC", 2)

with open("badwords.txt", encoding='utf-8') as file:
    badwords = [row.strip().lower() for row in file]


class Bot(Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.badword_message = None
        self.bwans = None
        self.incorrect_reactions_count = 0
        self.correct_reactions_count = 0
        self.badword_state = False

    async def on_ready(self):
        print("Bot started as {0}".format(self.user.name))

    async def on_message(self, message):
        print("Message from {message.author},which contains {message.content}, to channel with id {message.channel.id}")

        if message.channel.id == CHANNEL_ID:
            if self.badword_state:
                await message.delete()
                return

            mess_arr = message.content.split(" ")

            for word in mess_arr:
                word = word.lower()
                for badword in badwords:
                    if fuzz.ratio(word, badword) > 65:
                        print("bad word detected")
                        self.bwans = await message.channel.send("Был обнаружен мат. Если согласен ставь <:correct:714834242390982756> , если же нет, то <:incorrect:714834242525331498>")
                        self.badword_message = message
                        self.badword_state = True
                        await self.bwans.add_reaction("<:correct:714834242390982756>")
                        await self.bwans.add_reaction("<:incorrect:714834242525331498>")
                        return

    async def on_reaction_add(self, reaction, user):
        print("New reaction from user {user.name},its content {reaction.emoji},from message {reaction.message.content}")

        if reaction.message.id == self.bwans.id:
            if str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/714834242390982756.png":
                print("correct")
                self.correct_reactions_count += 1

                if self.correct_reactions_count >= TARGET_REACTIONS_COUNT:
                    self.correct_reactions_count = 0
                    self.incorrect_reactions_count = 0
                    self.badword_state = False
                    await self.bwans.delete()
                    await self.badword_message.delete()
                    await reaction.message.channel.send("User {0} used bad words!!".format(self.badword_message.author))

            elif str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/714834242525331498.png":
                print("incorrect")
                self.incorrect_reactions_count += 1

                if self.incorrect_reactions_count >= TARGET_REACTIONS_COUNT:
                    self.correct_reactions_count = 0
                    self.incorrect_reactions_count = 0
                    self.badword_state = False
                    await self.bwans.delete()


print(CHANNEL_ID)
print(TARGET_REACTIONS_COUNT)

client = Bot()
client.run("NzE0Nzg5Njc5ODc0MTc5MDgy.XtTIGg.eGGO8ppCr3vSVtJYBQWuVOButc4")#env["DISCORD_TOKEN"])
