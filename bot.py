from discord import Client
from discord.utils import get

CHANNEL_ID = 714770037780512808

badwords = [
    'хрен',
    "хуй",
    "еб",
    "педик",
    "пидор"
]


class Bot(Client):
    async def on_ready(self):
        print("Bot started as {0}".format(self.user.name))
        self.correct_reactions_count = 0
        self.incorrect_reactions_count = 0
        self.bwans = None
        self.badword_user = None
        self.badword_message = None

    async def on_message(self, message):
        print("Message from {0}, which contains {1}, to channel with id {2}".format(message.author, message.content, message.channel.id))

        if message.channel.id == CHANNEL_ID:
            for word in badwords:
                if word in message.content:
                    print("Bad word detected")
                    self.bwans = await message.channel.send("Был обнаружен мат. Если согласен ставь :correct: , если же нет, то :incorrect:")
                    self.badword_user = message.author
                    self.badword_message = message
                    await self.bwans.add_reaction("<:correct:714834242390982756>")
                    await self.bwans.add_reaction("<:incorrect:714834242525331498>")

    async def on_reaction_add(self, reaction, user):
        print("New reaction from user {0}, its content {1}, from message {2}".format(user.name, reaction.emoji, reaction.message.content))

        # await user.remove_roles(get(reaction.message.guild.roles, id=698175905515831366))

        if reaction.message.id == self.bwans.id:
            if str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/714834242390982756.png":
                print("correct")
                self.correct_reactions_count += 1

                if self.correct_reactions_count >= 2:
                    self.correct_reactions_count = 0
                    self.incorrect_reactions_count = 0
                    await self.bwans.delete()
                    await self.badword_message.delete()
                    await reaction.message.channel.send("User {0} used bad words!!!".format(self.badword_user))

            elif str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/714834242525331498.png":
                print("incorrect")
                self.incorrect_reactions_count += 1

                if self.incorrect_reactions_count >= 2:
                    self.correct_reactions_count = 0
                    self.incorrect_reactions_count = 0
                    await self.bwans.delete()


client = Bot()
client.run("NzE0Nzg5Njc5ODc0MTc5MDgy.Xszx2Q.2d7wsFpujLUPmgOZR9_3HtLIPSw")
