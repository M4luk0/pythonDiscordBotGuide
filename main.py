# Discord Bot Documentation https://discordpy.readthedocs.io/en/stable/

# We import the necessary libraries.
import discord # Discord library.
from discord import Member # Discord library.
from discord import embeds # Library for kick, bans, etc.
from discord.ext import commands # Discord library.
from discord.ext.commands import has_permissions, MissingPermissions # Library for kick, bans, etc.
from discord.utils import get # Role library.
from discord import FFmpegPCMAudio # Library to reproduce sounds.

# We configure the intents to take into account the members, exits and entrances of the server.
intents = discord.Intents.default()
intents.members = True

# Dictionary to save the audio queue.
queues = {}

# Check to see if the list is empty to make the play.
def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

# Initialize the bot configuration.
client = commands.Bot(command_prefix = '!', intents=intents)

# Bot initiation.
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Game'))
    print("The bot is now ready for use!")
    print("-----------------------------")

# Reacts to a specific message.
@client.event
async def on_message(message):
    if message.content == "ping":
        await message.delete()
        await message.channel.send("pong")

# When a member joins, the bot will inform us.
@client.event
async def on_member_join(member):
    channel = client.get_channel(882453811262787665) # This number is the ID of the voice channel that to get it we must set the dev mode of discord.
    await channel.send("Hello " + str(member.mention))

# When a member leaves, the bot will inform us.
@client.event
async def on_member_remove(member):
    channel = client.get_channel(882453811262787665) # This number is the ID of the voice channel that to get it we must set the dev mode of discord.
    await channel.send("Bye " + str(member.mention))

# When deleting a reaction.
@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await channel.send(user.name + " removed: " + reaction.emoji)

# Let the bot react to a message.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if ("happy") in message.content:
        emoji = '😂' # emojis: https://apps.timwhitlock.info/emoji/tables/unicode
        await message.add_reaction(emoji)

# When typing the command you will get the following response.
@client.command()
async def hello(ctx):
    await ctx.send("Hello my friend.")

# It enters the voice channel and plays a sound.
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('music.wav')
        player = voice.play(source)
    else:
        await ctx.send("Get in a voice channel.")

# Out of the voice channel.
@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("See you later.")
    else:
        await ctx.send("I am not on any voice channel.")

# Pause the currently playing audio.
@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("I am not reproducing anything machine.")

# Resume paused audio.
@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("There is no paused song.")

# Remove audio.
@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

# Plays the audio we pass by argument.
@client.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))

# Queues audios.
@client.command(pass_context = True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]

    await ctx.send("Added to queue.")

# Kick an user (to do it we put @usuario).
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} kicked.')

# If you do not have permission to kick.
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permissions to kickear.")

# Ban a user (to do so, type @user).
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} banned.')

# If you do not have permission to ban.
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to ban.")

# Unban.
@client.command()
@has_permissions(administrator=True)
async def unban(ctx, member: discord.Member, *, reason=None):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# If you do not have permission to unban.
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have unban permissions!")

# Mini banner.
@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Dog", url="https://test.com", description="We love dogs.", color=0x4dff4d)
    embed.set_author(name="Doge", url="https://test.com", icon_url="https://logo.png")
    embed.set_thumbnail(url="https://logo.png")
    embed.add_field(name="Labradors", value="Good", inline=False)
    embed.add_field(name="Husky", value="Cute", inline=False)
    embed.set_footer(text="Thanks for read.")
    await ctx.send(embed=embed)

# DM
@client.command()
async def message(ctx, user: discord.Member, *, message=None):
    message = "Welcome to the server!"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

# When reacting to a message.
@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await channel.send(user.name + " added: " + reaction.emoji)

# Add roles.
@client.command(pass_context = True)
@commands.has_permissions(manage_roles = True)
async def addRole(ctx, user: discord.Member, *, role: discord.Role):
    if role in user.roles:
        await ctx.send(f"{user.mention} already have this role {role}!")
    else:
        await user.add_roles(role)
        await ctx.send(f"{user.mention} has obteined a role {role}")

# If you do not have role permission.
@addRole.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permissions to add roles.")

# Remove roles.
@client.command(pass_context = True)
@commands.has_permissions(manage_roles = True)
async def removeRole(ctx, user: discord.Member, *, role: discord.Role):
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"{user.mention} no longer has the role {role}!")
    else:
        await ctx.send(f"The user {user.mention} does not have the role {role}")

# If you do not have role permission.
@removeRole.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to remove roles.")

# Ejecutamos el bot con el token correspondiente.
client.run('TOKEN')
