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

import os
import random
import json
import asyncio
import discord
from subprocess import DEVNULL, Popen, PIPE
from typing import Tuple, Union

PARENT = os.path.dirname(os.path.realpath(__file__))


class Context:
    chn: Union[discord.TextChannel, discord.VoiceChannel]
    voice: bool
    voice_conn: discord.VoiceClient

    async def init(self, client: discord.Client, chn_id: int, voice: bool):
        self.chn = await client.fetch_channel(chn_id)
        self.voice = voice

        if self.voice:
            assert isinstance(self.chn, discord.VoiceChannel)
            self.voice_conn = await self.chn.connect()
        else:
            assert isinstance(self.chn, discord.TextChannel)

    async def close(self):
        if self.voice:
            await self.voice_conn.disconnect()

    async def send(self, msg: str, delay: float = 0):
        if self.voice:
            msg = msg.replace(":", ",").replace("_", "").replace("*", "")
            args = ["espeak", "--stdout", "-s", "170"]
            with open("/tmp/bulone.wav", "wb") as fp:
                proc = Popen(args, stdin=PIPE, stdout=fp, stderr=DEVNULL)
                proc.stdin.write(msg.encode())
                proc.stdin.flush()
                proc.stdin.close()
                proc.wait()

            await self.play_audio("/tmp/bulone.wav")
            await asyncio.sleep(min(delay, 2))

        else:
            await self.chn.send(msg)
            await asyncio.sleep(delay)

    async def play_audio(self, path):
        audio = discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=path)
        self.voice_conn.play(audio)
        while self.voice_conn.is_playing():
            await asyncio.sleep(0.6)

    @staticmethod
    def locked():
        path = os.path.join(PARENT, "lock")
        return os.path.isfile(path)

    @staticmethod
    def lock():
        path = os.path.join(PARENT, "lock")
        with open(path, "w") as fp:
            pass

    @staticmethod
    def unlock():
        path = os.path.join(PARENT, "lock")
        if os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def json(name):
        path = os.path.join(PARENT, "data", name+".json")
        with open(path, "r") as fp:
            return json.load(fp)

    @staticmethod
    def rand_piece() -> Tuple[str, str, str]:
        """
        :return: (path, author, title)
        """
        titles = os.listdir(os.path.join(PARENT, "audio"))
        titles = [t.split(".")[0] for t in titles if t.endswith(".mp3")]
        piece = random.choice(titles)

        path = os.path.join(PARENT, "audio", piece+".mp3")
        with open(path+".title", "r") as fp:
            parts = fp.read().strip().split(":")
            author = parts[0].strip()
            title = parts[1].strip()

        return path, author, title
