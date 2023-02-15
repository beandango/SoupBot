from keep_alive import keep_alive
import discord
from discord.ext import commands
import os
from pymongo import MongoClient
from datetime import date
import time

keep_alive()

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='', intents=intents)

mongo = MongoClient(os.environ['MONGO_URL'])
db = mongo['Soup']
feedings = db['feedings']
weights = db['weights']
sheds = db['sheds']
poops = db['poops']

# turning the bot on lol


@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online,
                               activity=discord.Game('with Soup!'))
  print('hi im soup')
  try:
    synced = await client.tree.sync(guild=discord.Object(
      id=os.environ['GUILD']))
    print(f'synced {len(synced)} command(s)')
  except Exception as e:
    print(e)


# basically a ping command to see if bot's alive


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$hi'):
    print(f'i saw the message "{message.content}"')
    await message.reply('hi, im soup')


@client.tree.command(name="hello",
                     guild=discord.Object(id=os.environ['GUILD']))
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message('hi, im soup lol')


# feed logging


@client.tree.command(name="feed",
                     description="Log a feeding success/failure!",
                     guild=discord.Object(id=os.environ['GUILD']))
async def feed(interaction: discord.Interaction, type: str):
  #  fedAlready = feedings.find_one({"date": str(date.today())})
  #  if fedAlready == None:
  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)
  log = {"date": str(date.today()), "feeding": type, "time": current_time}
  db.feedings.insert_one(log)
  if type == 'yes':
    success = 'successful'
  if type == 'no':
    success = 'unsuccessful'
  await interaction.response.send_message(
    f'Logged {success} feeding for {str(date.today())}.')


#  else:
#    await interaction.response.send_message(
#      'Hey, you already logged a feeding today!')

# show feeding data


@client.tree.command(name="showfeedings",
                     description="show the last 10 feedings",
                     guild=discord.Object(id=os.environ['GUILD']))
async def showfeedings(interaction: discord.Interaction):
  feeds = db.feedings.find({}, sort=[("date", -1)], limit=10)
  data = "**Last 10 Feedings:**\n---------------------------\n"
  for index, feeding in enumerate(feeds):
    data += f"{feeding.get('date')}: {feeding.get('feeding')}\n"

  embed = discord.Embed(description=data, title='Feeding Data')

  yesses = db.feedings.count_documents({'feeding': 'yes'})
  noes = db.feedings.count_documents({'feeding': 'no'})
  # for editing later (pie): https://quickchart.io/chart-maker/edit/zm-487e20c7-c76f-45a8-bcdc-fdb792aab5c3

  urlPie = "https://quickchart.io/chart/render/zm-b29806d1-0ae2-4d02-b973-0ee6d29a669e"
  title = "?title=Does%20Soup%20Eat%20Her%20Rats?"
  labels = "&labels=Yes,No"
  data = f"&data1={yesses},{noes}"

  urlPie += title
  urlPie += labels
  urlPie += data

  embed.set_image(url=urlPie)
  embed.set_thumbnail(
    url="https://em-content.zobj.net/source/skype/289/rat_1f400.png")

  await interaction.response.send_message(embed=embed)


# clear feeding data


@client.tree.command(name="clearfeedingdata",
                     description="WARNING: this will CLEAR the feeding data",
                     guild=discord.Object(id=os.environ['GUILD']))
async def clearfeedingdata(interaction: discord.Interaction):
  feedings.delete_many({})
  await interaction.response.send_message('Cleared all feeding data')


# weight logging


@client.tree.command(name="weight",
                     description="Log Soup's weight in grams",
                     guild=discord.Object(id=os.environ['GUILD']))
async def weight(interaction: discord.Interaction, grams: int):
  weighedAlready = weights.find_one({"date": str(date.today())})
  if weighedAlready == None:
    log = {"date": str(date.today()), "g": grams}
    db.weights.insert_one(log)
    await interaction.response.send_message(
      f'Logged {grams}g for {str(date.today())}.')
  else:
    await interaction.response.send_message(
      'Hey, you already logged a weight today!')


# show weights


@client.tree.command(name="showweights",
                     description="show weight data",
                     guild=discord.Object(id=os.environ['GUILD']))
async def showweights(interaction: discord.Interaction):
  w = db.weights.find({})
  data = ""
  for index, weight in enumerate(w):
    data += f"{weight.get('date')}: {weight.get('g')}\n"
  embed = discord.Embed(description=data, title='Weight Data')
  await interaction.response.send_message(embed=embed)


# clear weight data


@client.tree.command(name="clearweightdata",
                     description="WARNING: this will CLEAR the weight data",
                     guild=discord.Object(id=os.environ['GUILD']))
async def clearweightdata(interaction: discord.Interaction):
  weights.delete_many({})
  await interaction.response.send_message('Cleared all weight data')


# Log Shed


@client.tree.command(name="shed",
                     description="Found a shed! Log quality [good/bad]",
                     guild=discord.Object(id=os.environ['GUILD']))
async def shed(interaction: discord.Interaction, quality: str):
  if quality == 'good' or quality == 'bad':
    log = {"date": str(date.today()), "quality": quality}
    db.sheds.insert_one(log)
    await interaction.response.send_message(
      f'Logged {quality} quality shed for {str(date.today())}.')
  else:
    await interaction.response.send_message('invalid format')


# show sheds


@client.tree.command(name="showsheds",
                     description="show shed data",
                     guild=discord.Object(id=os.environ['GUILD']))
async def showsheds(interaction: discord.Interaction):
  s = db.sheds.find({})
  data = ""
  for index, shed in enumerate(s):
    data += f"{shed.get('date')}: {shed.get('quality')}\n"
  embed = discord.Embed(description=data, title='Shed Data')
  await interaction.response.send_message(embed=embed)


# clear shed data


@client.tree.command(name="clearsheddata",
                     description="WARNING: this will CLEAR the shed data",
                     guild=discord.Object(id=os.environ['GUILD']))
async def clearsheddata(interaction: discord.Interaction):
  sheds.delete_many({})
  await interaction.response.send_message('Cleared all shed data')


# Log poop


@client.tree.command(name="poop",
                     description="Found a poop!",
                     guild=discord.Object(id=os.environ['GUILD']))
async def poop(interaction: discord.Interaction):
  log = {
    "date": str(date.today()),
  }
  db.poops.insert_one(log)
  await interaction.response.send_message(
    f'Logged SOUP POOP for {str(date.today())}!')


# show poops


@client.tree.command(name="showpoops",
                     description="show poop data",
                     guild=discord.Object(id=os.environ['GUILD']))
async def showpoops(interaction: discord.Interaction):
  p = db.poops.find({})
  data = ""
  for index, poop in enumerate(p):
    data += f"{poop.get('date')}\n"
  embed = discord.Embed(description=data, title='Poop Data')
  await interaction.response.send_message(embed=embed)


# clear poop data


@client.tree.command(name="clearpoopdata",
                     description="WARNING: this will CLEAR the poop data",
                     guild=discord.Object(id=os.environ['GUILD']))
async def clearpoopdata(interaction: discord.Interaction):
  poops.delete_many({})
  await interaction.response.send_message('Cleared all poop data :(')


# clear EVERYTHING


@client.tree.command(name='clearall',
                     description="clear ALL soup data",
                     guild=discord.Object(id=os.environ['GUILD']))
async def clearall(interaction: discord.Interaction):
  feedings.delete_many({})
  weights.delete_many({})
  sheds.delete_many({})
  poops.delete_many({})
  await interaction.response.send_message('Cleared all data :(')


# show EVERYTHING


@client.tree.command(name='showall',
                     description='Show all data at once',
                     guild=discord.Object(id=os.environ['GUILD']))
async def showall(interaction: discord.Interaction):

  feeds = db.feedings.find({})
  data = ""
  for index, feeding in enumerate(feeds):
    data += f"{feeding.get('date')}: {feeding.get('feeding')}\n"
  embed = discord.Embed(description=data, title='Feeding Data')
  await interaction.response.send_message(embed=embed)

  w = db.weights.find({})
  data4 = ""
  for index, weight in enumerate(w):
    data4 += f"{weight.get('date')}: {weight.get('g')} grams\n"
  embed4 = discord.Embed(description=data4, title='Weight Data')
  await interaction.channel.send(embed=embed4)

  p = db.poops.find({})
  data2 = ""
  for index, poop in enumerate(p):
    data2 += f"{poop.get('date')}\n"
  embed2 = discord.Embed(description=data2, title='Poop Data')
  await interaction.channel.send(embed=embed2)

  s = db.sheds.find({})
  data3 = ""
  for index, shed in enumerate(s):
    data3 += f"{shed.get('date')}: {shed.get('quality')}\n"
  embed3 = discord.Embed(description=data3, title='Shed Data')
  await interaction.channel.send(embed=embed3)


@client.tree.command(name='foodchart',
                     description='show a pie chart of feedings',
                     guild=discord.Object(id=os.environ['GUILD']))
async def foodchart(interaction: discord.Interaction):
  yesses = db.feedings.count_documents({'feeding': 'yes'})
  noes = db.feedings.count_documents({'feeding': 'no'})
  # for editing later (pie): https://quickchart.io/chart-maker/edit/zm-487e20c7-c76f-45a8-bcdc-fdb792aab5c3

  urlPie = "https://quickchart.io/chart/render/zm-b29806d1-0ae2-4d02-b973-0ee6d29a669e"
  title = "?title=Does%20Soup%20Eat%20Her%20Rats?"
  labels = "&labels=Yes,No"
  data = f"&data1={yesses},{noes}"

  urlPie += title
  urlPie += labels
  urlPie += data

  await interaction.response.send_message(urlPie)


client.run(os.environ['TOKEN'])
