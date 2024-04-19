import discord
from discord.ext import commands
from discord import Intents, app_commands
import asyncio

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        self.tree.add_command(check_all_members, guild=None)
        await self.tree.sync()

intents = Intents.default()
intents.members = True

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@app_commands.command(name="check_all_members", description="Check all members for a profile picture and kick those without one")
async def check_all_members(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    guild = interaction.guild
    member_count = 0
    for member in guild.members:
        if member.bot:
            continue
        await check_pfp(member)
        member_count += 1
        if member_count % 10 == 0:
            await asyncio.sleep(2)

async def check_pfp(member):
    if member.display_avatar.url == member.default_avatar.url:
        try:
            await member.send(
                "You've been kicked from Your Server Name for not having a profile picture. "
                "If you think this was an error, you can rejoin at https://discord.gg/yourinvite"
            )
        except discord.errors.Forbidden:
            print(f"Can't send DM to {member.name}.")
        try:
            await member.kick(reason="No profile picture")
        except discord.errors.Forbidden:
            print(f"Can't kick {member.name}.")

bot.run('your_token_here')
