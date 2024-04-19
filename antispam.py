import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@slash.slash(
    name="check_all_members",
    description="Check all members for a profile picture and kick those without one"
)
async def check_all_members(ctx: SlashContext):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You do not have permission to use this command.", hidden=True)
        return
    guild = ctx.guild
    member_count = 0
    for member in guild.members:
        if member.bot:
            continue
        await check_pfp(member)
        member_count += 1
        if member_count % 10 == 0:
            await asyncio.sleep(2)

async def check_pfp(member):
    if member.avatar is None:
        try:
            await member.send(
                "You've been kicked from your server name for not having a profile picture. "
                "If you think this was an error, you can rejoin at https://discord.gg/yourinvite"
            )
        except discord.errors.Forbidden:
            print(f"Can't send DM to {member.name}.")
        try:
            await member.kick(reason="No profile picture")
        except discord.errors.Forbidden:
            print(f"Can't kick {member.name}.")

bot.run('your_token_here')
