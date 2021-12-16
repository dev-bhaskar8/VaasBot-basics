import discord
import os
import pandas as pd
import requests
import concurrent.futures
from keep_alive import keep_alive
import time
from datetime import datetime
import random


vaas_wordlist = ["""
Why doesn’t Vaas go to strip clubs? 

Because they already have all the booty!
​""",
"""
Why did pirate capt Vaas confuse all of his Tinder dates?

They couldn't figure out if he was blinking or winking.
""",
"""
The famous pirate Blackbeard walks into a bar and he has a ship's wheel stuck to his crotch region. "Ooh Arrr, give me a pint of ye finest ale!" he says.

Vaas, checks out Blackbeard and asks him "what happened? why have you got a ship's wheel stuck to your pants?"

"Me ship was a'tossin in the storm! Things got outta control and I snagged 'er  on me jolly rogers."

Concerned Vaas, is a helpful man and says, "Well let me help you there" and he grabs the wheel and started twisting it to help get it off.

"Aaaaaar!" screams Blackbeard "yer driving me nuts!"

""",
"""
Why did Vaas get a gym membership?

So he could improve his pirate booty and his treasured chest.
​""",
"""
Did you hear about the pirate drug addict Capt Vaas?

He was completely hooked.
​""",
"""
What did the first mate see down the toilet? 

The Captain Vaas's log!
""",
"""
Captain hook is now dead. Do you know how he was killed?

He wiped his bum with the wrong hand.
​""",
"""
What is a gay pirates favourite hobby?

Sailing the 7 D's.
""",
"""
What did Capt Vaas say to the flying hooker?

Land ho.​"""]

vaas_one_liners=["Prepare to be boarded!",
"Permission to fire my cannon through your portholes?",
"Aye, Pirate! Is that a hornpipe in your pocket or are ye happy to me?",
"I know where you can bury your treasure.",
"Wanna see the world’s best pirate booty?",
"Your Jolly Roger ain’t the only thing ye’ll be raisin’ tonight.",
"Arrrrrrrrre ye free tonight, after bedtime?",
"Care if my parrot watches while ye board me ship, matey?",
"Lookin’ for booty? Mine’s ready for pillaging.",
"Yo ho ho! I’ve got a bottle of rum and a penchant for making drunken mistakes.",
"Can I help making your roger a little more jolly?",
"Let’s head back to me ship and rock the boat.",
"A good captain goes down with his ship, wanna go down with me?",
"I must be huntin' treasure, 'cause I'm diggin' yer chest!",
"I've sailed the seven seas, and you're the sleekest schooner I've ever sighted.",
"That's some treasure chest you've got there.",
"Yer guilty of being a hot wench. I sentence you to walking my plank!"
]

sheetId = "1fXu7oRQoApJ0E5mg-5p1U07dWJ8lQSYVmqldK9Sx6ek"
sheetName = "AxieAccount"
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
sheetURL = f"https://docs.google.com/spreadsheets/d/{sheetId}/gviz/tq?tqx=out:csv&sheet={sheetName}"

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$slur'):
      try:
        await message.channel.send(requests.get('https://pirate.monkeyness.com/api/insult').text+'  ☠️')
      except:
        await message.channel.send('Aaaarrrrgggghhhh!')
    if message.content.startswith('$vaas'):
      await message.channel.send(random.choice(vaas_one_liners)+'  😘')
    if message.content.startswith('$capt'):
      await message.channel.send(random.choice(vaas_wordlist)+'\nAaaarrrrgggghhhh! 🏴‍☠️ 🦜')
    if message.content.startswith('$mmr'):
      await message.channel.send('Loading ser..... it takes upto 1 minute.  👻')
      managerName=message.content.split('$mmr ',1)[1]
      index = 0
      df = pd.read_csv(sheetURL)
      pd.set_option('display.max_rows', None)

      df = df[['Address' , 'Manager', 'Scholar Username' , 'Index']]
      df.set_index('Manager',inplace=True)
      try:
        df = df.loc[managerName]
      except:
        await message.channel.send('Please enter a valid manager name and try again ser. 🥱')
        return
      df.reset_index(inplace=True)
      df = df[['Address','Scholar Username','Index']]
      data = {
          "scholar_no":[],
          "name":[],
          "mmr":[]
      }
      def mmr(address):
        return(requests.get(f"https://game-api.axie.technology/mmr/{address}",headers=headers))

      with concurrent.futures.ThreadPoolExecutor() as executor:
        mmrs = list(executor.map(mmr,list(df['Address'])))

      for i in range(index,df.shape[0]):
        name = df.iloc[i][1]
        scholar_no = df.iloc[i][2]
        try:
          mmr = mmrs[i].json()[0]['items'][1]['elo']
        except:
          mmr = 0
        data["mmr"].append(mmr)
        data["name"].append(name)
        data["scholar_no"].append(scholar_no)
        index+=1
      scholars = pd.DataFrame(data)
      
      scholars.set_index('scholar_no',inplace=True)
      scholars=scholars.dropna()
      print('Done')
      await message.channel.send('```Scholar ID        Name        MMR```')
      for i in range(0,scholars.shape[0]):
        if i%35 == 0:
          await message.channel.send("```"+str(scholars.iloc[i:i+35])[60:]+"```")



    if message.content.startswith('$slp'):
      await message.channel.send('Loading ser..... it takes upto 1 minute.  👻')
      managerName=message.content.split('$slp ',1)[1]
      index = 0
      df = pd.read_csv(sheetURL)
      pd.set_option('display.max_rows', None)
      pd.set_option('display.max_columns', None)

      df = df[['Address' , 'Manager', 'Scholar Username' , 'Index','Scholar ID']]
      df.set_index('Manager',inplace=True)
      try:
        df = df.loc[managerName]
      except:
        await message.channel.send('Please enter a valid manager name and try again ser. 🥱')
        return
      df.reset_index(inplace=True)
      df = df[['Address','Scholar Username','Index','Scholar ID']]
      data = {
          "scholar_no":[],
          "name":[],
          "average":[],
          "total":[],
          "last_claimed":[]
      }
      def call(address):
        return(requests.get(f"https://game-api.skymavis.com/game-api/clients/{address}/items/1",headers=headers))

      with concurrent.futures.ThreadPoolExecutor() as executor:
        responses = list(executor.map(call,list(df['Address'])))

      for i in range(index,df.shape[0]):
        name = df.iloc[i][1]
        scholar_no = df.iloc[i][2]
        response = responses[i].json()
        if response['success']==True:
          total_slp = response['total']
          last_calimed = datetime.fromtimestamp(response['last_claimed_item_at'])
          now = datetime.fromtimestamp(time.time())
          days = now - last_calimed
          days = int(days.days)+1
          average_slp = total_slp // (days+1)
          data["name"].append(name)
          data["last_claimed"].append(days)
          data["total"].append(total_slp)
          data["average"].append(average_slp)
          data["scholar_no"].append(scholar_no)
          index+=1
      scholars = pd.DataFrame(data)
      scholars.set_index('scholar_no',inplace=True)
      scholars=scholars.dropna()
      scholars = scholars.sort_values(by=['average'],ascending=False)
      print('Done')
      await message.channel.send('```Scholar ID        Name         Avg SLP  Total SLP  Last Claimed```')
      for i in range(0,scholars.shape[0]):
        if i%20 == 0:
          await message.channel.send("```"+str(scholars.iloc[i:i+20])[90:]+"```")

    if message.content.startswith('$total'):
      await message.channel.send('Loading ser..... it takes upto 1 minute.  👻')
      managerName=message.content.split('$total ',1)[1]
      index = 0
      df = pd.read_csv(sheetURL)
      pd.set_option('display.max_rows', None)
      pd.set_option('display.max_columns', None)

      df = df[['Address' , 'Manager', 'Scholar Username' , 'Index','Scholar ID']]
      df.set_index('Manager',inplace=True)
      try:
        df = df.loc[managerName]
      except:
        await message.channel.send('Please enter a valid manager name and try again ser. 🥱')
        return
      df.reset_index(inplace=True)
      df = df[['Address','Scholar Username','Index','Scholar ID']]
      data = {
          "scholar_no":[],
          "name":[],
          "total":[],
          "last_claimed":[]
      }
      def call(address):
        return(requests.get(f"https://game-api.skymavis.com/game-api/clients/{address}/items/1",headers=headers))

      with concurrent.futures.ThreadPoolExecutor() as executor:
        responses = list(executor.map(call,list(df['Address'])))

      for i in range(index,df.shape[0]):
        name = df.iloc[i][1]
        scholar_no = df.iloc[i][2]
        response = responses[i].json()
        if response['success']==True:
          total_slp = response['total']
          last_calimed = datetime.fromtimestamp(response['last_claimed_item_at'])
          now = datetime.fromtimestamp(time.time())
          days = now - last_calimed
          days = int(days.days)+1
          data["name"].append(name)
          data["last_claimed"].append(days)
          data["total"].append(total_slp)
          data["scholar_no"].append(scholar_no)
          index+=1
      scholars = pd.DataFrame(data)
      
      scholars.set_index('scholar_no',inplace=True)
      scholars=scholars.dropna()
      print('Done')
      await message.channel.send('```Scholar ID        Name       Total SLP  Last Claimed```')
      for i in range(0,scholars.shape[0]):
        if i%20 == 0:
          await message.channel.send("```"+str(scholars.iloc[i:i+20])[90:]+"```")


keep_alive()
client.run(os.getenv("TOKEN"))
