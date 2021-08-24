import os
import discord
import requests 
#requests module helps us to make http requests
import json
import random
from replit import db


#creating instance for client using methods from discord.py library
client = discord.Client() 

sad_words = [
  "sad", "not feeling good", "feeling weird", "depressed", "anxious",
  "deperssing",  "brokenhearted", "dejected", "down", "gloomy", "heartbroken","heavyhearted", "joyless", "low", "miserable", "mournful", "unhappy"
]

starter_encouragements =[
 "Hang in there.", "Don’t give up.", "Keep pushing.", "Keep fighting!",
 "Stay strong.", "Never give up.", "Come on! You can do it!."
 "Follow your dreams.", "Reach for the stars.", "Do the impossible.", "Believe in yourself.", "The sky is the limit."
]

#helper function
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")

  json_data = json.loads(response.text)

  quote = json_data[0]['q'] + " -"+ json_data[0]['a']
  return(quote)


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
  
#using client.event decorator to register an event
@client.event

#this is a asynchronous library, events are done with call backs. Call Back function is a function that is excuted when command is given

async def on_ready():
  print('We have logged in as {0.user}'.format(client)) 
  #0 gets replaced by client


@client.event

#function is from the discord.py library
async def on_message(message):
  if message.author == client.user:
    return 
  
  msg = message.content
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options.extend(db["encouragements"])

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouragement added.")


client.run(os.getenv('Token'))