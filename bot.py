from discord import Client
from discord.utils import get

CHANNEL_ID = 714790972051030096


class Bot(Client):
    def __init__(self):
        self.badword_message = None
        self.bwans = None
        self.incorrect_reactions_count = 0
        self.correct_reactions_count = 0
        self.badword_state = False

    async def on_ready(self):
        print("Bot started as {0}".format(self.user.name))

    async def on_message(self, message):
        print("Message from {message.author},which contains {message.content}, to channel with id {message.channel.id}")

        if self.badword_state:
            await message.delete()

        if message.channel.id == CHANNEL_ID:
            for word in badwords:
                if word in message.content:
                    print("Bad word detected")
                    self.bwans = await message.channel.send("Был обнаружен мат. Если согласен ставь <:correct:714834242390982756> , если же нет, то <:incorrect:714834242525331498>")
                    self.badword_message = message
                    self.badword_state = True
                    await self.bwans.add_reaction("<:correct:714834242390982756>")
                    await self.bwans.add_reaction("<:incorrect:714834242525331498>")

    async def on_reaction_add(self, reaction, user):
        print("New reaction from user {0}, its content {1}, from message {2}".format(user.name, reaction.emoji, reaction.message.content))

        if reaction.message.id == self.bwans.id:
            if str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/714834242390982756.png":
                print("correct")
                self.correct_reactions_count += 1

                if self.correct_reactions_count >= 2:
                    self.correct_reactions_count = 0
                    self.incorrect_reactions_count = 0
                    self.badword_state = False
                    await self.bwans.delete()
                    await self.badword_message.delete()
                    await reaction.message.channel.send("User {0} used bad words!!".format(self.badword_message.author))

            elif str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/714834242525331498.png":
                print("incorrect")
                self.incorrect_reactions_count += 1

                if self.incorrect_reactions_count >= 2:
                    self.correct_reactions_count = 0
                    self.incorrect_reactions_count = 0
                    self.badword_state = False
                    await self.bwans.delete()


client = Bot()
client.run("NzE0Nzg5Njc5ODc0MTc5MDgy.Xs5H_Q.BdnGbOB4B6GzrPxEUmjOzYKJ81A")
