import discord
import os
from discord.ext import commands

TOKEN = os.environ["BOT_TOKEN"]
GUILD_ID = 1076555902917816480
CHANNEL_ID = 1076571503040139285
ADMIN_ROLE_ID = 1531476634043940897
CHECK_EMOJI = "✅"
KEYWORD = "훈련"

MAX_POINT = 40

ROLE_IDS = {
    1: 1332280422914199616,
    2: 1332280429184815145,
    3: 1332280429641994277,
    4: 1332280430740901888,
    5: 1332280431235694643,
    6: 1332280431953055774,
    7: 1332280432569483294,
    8: 1332280433148297216,
    9: 1332280434817634334,
    10: 1332280436335972403,
    11: 1332280436344487957,
    12: 1332280437397131264,
    13: 1332281039153922080,
    14: 1332281044640202772,
    15: 1332281044950585415,
    16: 1332281045780926525,
    17: 1332281046540222596,
    18: 1332281047249063957,
    19: 1332281048108892171,
    20: 1332281048968593481,
    21: 1526221121484099674,
    22: 1526221160067629276,
    23: 1526221196583243827,
    24: 1526221225230073947,
    25: 1526221265202053230,
    26: 1526221320440909854,
    27: 1526221339470463077,
    28: 1526221378674491533,
    29: 1526221402880081940,
    30: 1526221429190692874,
    31: 1526221460937638082,
    32: 1526221489169502379,
    33: 1526221742668779570,
    34: 1526221780640075856,
    35: 1526221802077163521,
    36: 1526221826525761568,
    37: 1526221849824858123,
    38: 1526221876832112751,
    39: 1526221900739514521,
    40: 1526221924223418468,
}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)


def get_point(member: discord.Member) -> int:
    owned = {r.id for r in member.roles}
    for point, rid in ROLE_IDS.items():
        if rid in owned:
            return point
    return 0


async def add_point(member: discord.Member, amount: int):
    current = get_point(member)
    if current >= MAX_POINT:
        return
    new_point = min(current + amount, MAX_POINT)
    guild = member.guild
    old_role = guild.get_role(ROLE_IDS[current]) if current in ROLE_IDS else None
    new_role = guild.get_role(ROLE_IDS[new_point])
    if old_role:
        await member.remove_roles(old_role)
    if new_role:
        await member.add_roles(new_role)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if str(payload.emoji) != CHECK_EMOJI or payload.guild_id != GUILD_ID:
        return
    if payload.channel_id != CHANNEL_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return
    if ADMIN_ROLE_ID not in {r.id for r in member.roles}:
        return

    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if KEYWORD not in message.content:
        return
    if any(r.me for r in message.reactions if str(r.emoji) == CHECK_EMOJI):
        return

    await add_point(message.author, 2)
    for user in message.mentions:
        if user.id == message.author.id:
            continue
        await add_point(user, 1)

    await message.add_reaction(CHECK_EMOJI)


bot.run(TOKEN)
