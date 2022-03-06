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
from context import Context


async def readwrite(ctx: Context):
    await ctx.send("Read and", 3)
    if random.randint(0, 3) == 3:
        await ctx.send("Let's try that again. Remember, it needs to be like the breaks on a car. "
            "If they don't work, the car will crash, just like your Java program.", 2)
        await ctx.send("Read and", 3)
    await ctx.send("Write", 4)

async def start(ctx: Context):
    await ctx.send("BuloneBot: The Bulone experience on Discord.", 4)
    await readwrite(ctx)
