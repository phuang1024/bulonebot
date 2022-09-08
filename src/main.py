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

import random
import re
import discord
import conv
import logger
from context import Context

# Channel IDs for buloning, not responding.
TEXT_ID = 910323880948817970   # bulone/writing-prompt-discussions
VOICE_ID = 910033905804013612  # bulone/turn-and-talk
TEXT_ID = 932788451932242012   # segfault/testing
VOICE_ID = 949806823114956821  # segfault/voice

RESTRICTED = True  # Allow others to start bulone.

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
client = discord.Client(intents=intents)


async def start_bulone(msg, voice):
    ctx = Context()
    if ctx.locked():
        logger.warn(f"{msg.author} tried to start bulone while locked.")
        await msg.channel.send("Already buloning. Please try again later or contact phuang1024.")
        return
    ctx.lock()
    logger.info(f"{msg.author} started bulone, voice={voice}")

    await ctx.init(client, (VOICE_ID if voice else TEXT_ID), voice)

    await msg.channel.send("Starting Bulone on " + ("voice" if voice else "text"))
    await conv.start(ctx)
    await ctx.close()
    ctx.unlock()


@client.event
async def on_ready():
    text = await client.fetch_channel(TEXT_ID)
    voice = await client.fetch_channel(VOICE_ID)
    assert isinstance(text, discord.TextChannel)
    assert isinstance(voice, discord.VoiceChannel)

    logger.debug(f"BuloneBot is ready.")
    logger.debug(f"Restricted mode: {RESTRICTED}")
    logger.debug(f"Text channel:  \"{text.guild}\" / \"{text}\"")
    logger.debug(f"Voice channel: \"{voice.guild}\" / \"{voice}\"")

    Context.unlock()

@client.event
async def on_message(msg: discord.Message):
    if msg.author == client.user:
        return

    content = msg.content.lower().strip()
    pat_cmd = re.compile(r"(bulonebot|bb) *\(.*?\)")
    pat_arg = re.compile(r"\(.*?\)")

    if pat_cmd.findall(content):
        find = pat_arg.findall(content)
        arg = find[0][1:-1].strip() if find else ""
        logger.info(f"{msg.author} sent command: \"{arg}\"")

        if arg == "":
            await msg.channel.send(f"Hello {msg.author.display_name}. Try `bulonebot(help)` for more info.")

        elif arg == "help":
            text = "```\n"
            text += "Bulone Discord bot.\n"
            text += "Usage:\n"
            text += "  bulonebot(arg) or bb(arg)\n"
            text += "Arguments:\n"
            text += "  help:   Show this help message.\n"
            text += "  about:  About BuloneBot.\n"
            text += "  text:   Start Bulone in a text channel.\n"
            text += "  voice:  Start Bulone in a voice channel.\n"
            text += "  talk:   Say something that Bulone says.\n"
            text += "  math:   Help about any math problem.\n"
            text += "```"
            await msg.channel.send(text)

        elif arg == "about":
            text = "Mr. Bulone is the best English teacher."
            await msg.channel.send(text)

        elif arg in ("text", "voice"):
            if msg.author.display_name != "phuang1024" and RESTRICTED:
                logger.warn(f"{msg.author} tried to start bulone when restricted.")
                await msg.channel.send("You don't have permission to use this command. Try `sudo`.\n"
                    "This is most likely because the bot is disabled for testing.")
                return

            await start_bulone(msg, arg == "voice")

        elif arg == "talk":
            phrase = random.choice(Context.json("phrases"))
            await msg.channel.send(phrase)

        elif arg == "math":
            tip = random.choice(Context.json("math"))
            await msg.channel.send(tip)

        else:
            await msg.channel.send(f"Unknown command. Try `bulonebot(help)` for more info.")


def main():
    with open("token.txt", "r") as fp:
        client.run(fp.read().strip())


if __name__ == "__main__":
    main()
