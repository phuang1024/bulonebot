import discord

client = discord.Client()


@client.event
def on_ready():
    print("Bulone is ready.")


@client.event
def on_message(msg):
    pass


with open("token.txt", "r") as fp:
    client.run(fp.read().strip())
