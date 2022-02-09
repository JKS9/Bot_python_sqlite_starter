import discord
import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()
conn = sqlite3.connect('users.db')

@client.event
async def on_ready():
  print("Bot is ready !")

@client.event
async def on_message(message):
    if (message.author.bot) : return

    channel_id = message.channel.id
    channel = client.get_channel(channel_id)
    IdentityUserSendMessage = message.author.name + '#' + message.author.discriminator

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


client.run(BOT_TOKEN)
