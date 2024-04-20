import discord
from discord.ext import commands

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.slash_command(name="check_all_members", description="Check all members for a profile picture and kick those without one")
@commands.has_permissions(administrator=True)
async def check_all_members(ctx: discord.ApplicationContext):
    guild = ctx.guild
    total_members = sum(1 for member in guild.members if not member.bot)
    message = await ctx.respond(f"Checking members: 0/{total_members}", ephemeral=True)

    member_count = 0
    for member in guild.members:
        if member.bot:
            continue
        await check_pfp(member, ctx)
        member_count += 1
        if member_count % 10 == 0 or member_count == total members:
            await message.edit_original_response(content=f"Checking members: {member_count}/{total_members}")

async def check_pfp(member, ctx):
    if any(role.name == 'Server Booster' for role in member.roles):
        print(f"Skipping {member.name}, a server booster.")
        return

    if member.display_avatar.url == member.default_avatar.url:
        try:
            await member.send(
                "You've been kicked from Your Server Name for not having a profile picture. "
                "If you think this was an error, you can rejoin at https://discord.gg/yourinvite"
            )
        except discord.Forbidden:
            print(f"Can't send DM to {member.name}.")

        try:
            await member.kick(reason="No profile picture")
        except discord.Forbidden:
            print(f"Can't kick {member.name}.")

bot.run('your_token_here')