#Import library Dispord.py // https://discordpy.readthedocs.io/en/stable/
import discord

#Import livrary Sqlite // https://pypi.org/project/pysqlite3/
import sqlite3

#Import livrary for environment variables
import os
from dotenv import load_dotenv

load_dotenv()
#Set environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

#Set Discord client
client = discord.Client()

#Connect to DB "mdkir users.db"
conn = sqlite3.connect('users.db')

#A dit function informs you when the bot is ready
@client.event
async def on_ready():
  print("Bot is ready !")

#A function to manage commands sent to the bot
@client.event
async def on_message(message):
    #Verify is command is send by bot
    if (message.author.bot) : return

    #Set data user
    channel_id = message.channel.id
    channel = client.get_channel(channel_id)
    IdentityUserSendMessage = message.author.name + '#' + message.author.discriminator

    #The different possible commands and an example CRUD for the interaction with the database

    if (message.content == "!register"):
      c = conn.cursor()
      c.execute("INSERT INTO users (discordIdentity) VALUES (?)", (IdentityUserSendMessage,))
      conn.commit()

      text = "User " + IdentityUserSendMessage + " Registed !"
      await channel.send(text)

    if (message.content == "!init"):
      c = conn.cursor()
      c.execute('''CREATE TABLE users (discordIdentity)''')
      conn.commit()

      text = "Succefull Init !"
      await channel.send(text)

    if (message.content == "!list-user"):
      c = conn.cursor()
      c.execute('SELECT * FROM users')
      result = c.fetchall()
      print(result)
      conn.commit()

      await channel.send(result)

    if (message.content == "!delete"):
      c = conn.cursor()
      delete = await c.execute('DELETE FROM users WHERE discordIdentity=?', (IdentityUserSendMessage,))
      print(delete)
      conn.commit()

#Starting the discord bot with the identification token obtained on the Discord dashboard linked to the bot
client.run(BOT_TOKEN)
