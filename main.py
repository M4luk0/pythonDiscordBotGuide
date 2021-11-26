# Documentación discord bot https://discordpy.readthedocs.io/en/stable/

# Dónde aprendí: https://www.youtube.com/channel/UCwBjRPUuOefh6iFvG6zLhrg

# Antes de nada ponemos py -3 -m pip install -U discord.py

# Importamos las librerías necesarias.
import discord # Librería de discord.
from discord import Member
from discord import embeds # Librería para kick, bans y tal.
from discord.ext import commands # Librería de discord.
from discord.ext.commands import has_permissions, MissingPermissions # Librería para kick, bans y tal.
from discord.utils import get # Librería para roles.
from discord import FFmpegPCMAudio # Librería para reproducir sonidos.

# Configuramos los intents para tener en cuenta a los miembros, salidas y entradas del servidor.
intents = discord.Intents.default()
intents.members = True

# Diccionario para guardar la cola de audio.
queues = {}

# Check para ver si la lista está vacía para hacer el play.
def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

# Inicializamos la configuración del bot.
client = commands.Bot(command_prefix = '!', intents=intents)

# Iniciación del bot.
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('mandar flexiones.'))
    print("The bot is now ready for use!")
    print("-----------------------------")

# Reacciona a un mensaje en específico.
@client.event
async def on_message(message):
    if message.content == "flexiones":
        await message.delete()
        await message.channel.send("Muchas flexiones para todos!")

# Al unirse un miembro, nos lo comunicará.
@client.event
async def on_member_join(member):
    channel = client.get_channel(882453811262787665)
    await channel.send("Buenas " + str(member.mention))

# Al irse un miembro, nos lo comunicará.
@client.event
async def on_member_remove(member):
    channel = client.get_channel(882453811262787665)
    await channel.send("Adiós " + str(member.mention))


# Al borrar una reacción.
@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await channel.send(user.name + " removed: " + reaction.emoji)

# Que el bot reaccione a un mensaje.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if ("happy") in message.content:
        emoji = '😂' # emojis: https://apps.timwhitlock.info/emoji/tables/unicode
        await message.add_reaction(emoji)

# Al escribir el comando nos responderá.
@client.command()
async def hola(ctx):
    await ctx.send("Gil te quedan 3500 flexiones.")

# Se mete en el canal de voz y reproduce un sonido (para hacerlo primero hay que poner pip install -U discord.py[voice] ...
# ... también instalar FFmpeg que viene en este video https://www.youtube.com/watch?v=M_6_GbDc39Q&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=4).
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('music.wav')
        player = voice.play(source)
    else:
        await ctx.send("Metete en un canal de voz antes.")

# Se sale del canal de voz (para hacerlo primero hay que poner pip install -U discord.py[voice]).
@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Hasta luego.")
    else:
        await ctx.send("No estoy en ningún canal de voz.")

# Pausa el audio que está reproduciendo.
@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No estoy reproduciendo ná maquina.")

# Reanuda el audio pausado.
@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("No hay ninguna canción pausada.")

# Quita el audio.
@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

# Reproduce el audio que pasemos por argumento.
@client.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))

# Pone en cola los audios.
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

    await ctx.send("Añadida a la cola.")

# Kickear un usuario (para hacerlo ponemos @usuario).
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Usuario {member} kickeado.')

# Si no tienes permiso para kick.
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos para kickear.")

# Banear un usuario (para hacerlo ponemos @usuario).
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Usuario {member} baneado.')

# Si no tienes permiso para ban.
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos para banear.")

# Desbanear.
@client.command()
@has_permissions(administrator=True)
async def unban(ctx, member: discord.Member, *, reason=None):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Desbaneado {user.mention}')
            return

# Si no tienes permiso para desbanear.
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos para desbanear!")

# Un mini banner por así decirlo (se le pueden meter muchas cosas).
@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Dog", url="https://google.com", description="Amamos a los perros.", color=0x4dff4d)
    embed.set_author(name="Almagosi", url="https://comandoomega.es", icon_url="https://comandoomega.es/uploads/monthly_2020_12/logoomega.png.6ece64417c0c301503f63529c78f65f9.png")
    embed.set_thumbnail(url="https://comandoomega.es/uploads/monthly_2020_12/logoomega.png.6ece64417c0c301503f63529c78f65f9.png")
    embed.add_field(name="Labradores", value="Los putos amos", inline=False)
    embed.add_field(name="Husky", value="Demasiado bonitos", inline=False)
    embed.set_footer(text="Gracias por leer.")
    await ctx.send(embed=embed)

# DM
@client.command()
async def message(ctx, user: discord.Member, *, message=None):
    message = "Bienvenido al server de bravo ghost!"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

# Al reaccionar a un mensaje.
@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await channel.send(user.name + " added: " + reaction.emoji)

# Añadir roles.
@client.command(pass_context = True)
@commands.has_permissions(manage_roles = True)
async def addRole(ctx, user: discord.Member, *, role: discord.Role):
    if role in user.roles:
        await ctx.send(f"{user.mention} ya tiene el rol {role}!")
    else:
        await user.add_roles(role)
        await ctx.send(f"{user.mention} ha obtenido el rol {role}")

# Si no tienes permiso para roles.
@addRole.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos para añadir roles.")

# Quitar roles.
@client.command(pass_context = True)
@commands.has_permissions(manage_roles = True)
async def removeRole(ctx, user: discord.Member, *, role: discord.Role):
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"{user.mention} ya no tiene el rol {role}!")
    else:
        await ctx.send(f"El usuario {user.mention} no tiene el rol {role}")

# Si no tienes permiso para roles.
@removeRole.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos para quitar roles.")

# Ejecutamos el bot con el token correspondiente.
client.run('TOKEN')
