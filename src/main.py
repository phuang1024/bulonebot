#
#  Bulonebot
#  Bulone discord bot.
#  Copyright  Patrick Huang  2022
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import asyncio
import discord
import conv
from context import Context

#TEXT_ID = 910323880948817970   # bulone/writing-prompt-discussions
#VOICE_ID = 910033905804013612  # bulone/turn-and-talk

TEXT_ID = 932788451932242012   # segfault/testing
VOICE_ID = 949806823114956821  # segfault/voice

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Bulone is ready.")
    print("Text channel:", await client.fetch_channel(TEXT_ID))
    print("Voice channel:", await client.fetch_channel(VOICE_ID))

@client.event
async def on_message(msg: discord.Message):
    if msg.author == client.user:
        return

    content = msg.content.lower().strip()
    if content.startswith("bulonebot"):
        voice = "voice" in content
        ctx = Context()
        await ctx.init(client, (VOICE_ID if voice else TEXT_ID), voice)

        await msg.channel.send("Starting Bulone on " + ("voice" if voice else "text"))
        await asyncio.sleep(4)
        await conv.start(ctx)
        await ctx.close()


with open("token.txt", "r") as fp:
    client.run(fp.read().strip())
