import discord

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)


@client.event
def on_ready():
    print("Bulone is ready.")

@client.event
def on_message(msg):
    pass


with open("token.txt", "r") as fp:
    client.run(fp.read().strip())
