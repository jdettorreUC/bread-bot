from discord.ext import commands
import discord
import random

reading_judgement = []
judgement_list = []
judgement_dict = {}

# Contains the token allowing you to run the code onto the discord bot, file not availble in this repo for obvious reasons
with open("key.txt") as file:
    key = file.readline()

# Text file contains a bunch of bread related jokes, simple for loop to put them into a list
with open("bread_jokes.txt") as file:
    joke_list = [line.rstrip() for line in file]

# Leading int in the text file is being used as weight (how rare/common you want each judgement to be) and adds the imgur link to a list that many times
# Also makes a dictionary with the image link as a key and the corresponding description as the data
with open("bread_judgements.txt") as file:
    for line in file:
        reading_judgement = (line.strip()).split("#")
        judgement_dict[reading_judgement[1]] = reading_judgement[2]
        for i in range(0, int(reading_judgement[0])):
            judgement_list.append(reading_judgement[1])

# Leading int is the cutoff level until you upgrade to the next stage of bread
# Creates list of lists containing the cutoff, image link, and bread stage
with open("rolls.txt") as file:
    rolls = [(line.strip()).split(",") for line in file]

# Assign the client variable to the result of discord.Client().
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = discord.Bot(intents=intents)

# Define an async function under the client event parameter.
# This function will print the bot user's client ID to our console
# once the async function has returned that we have logged in sucessfully.
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Picks a random joke from the list and sends it to the chat
@bot.slash_command(name="joke", description='Tells a bread-related joke')
async def joke(ctx):
    joke_numb = random.randint(0, len(joke_list))
    await ctx.respond(joke_list[joke_numb])

# Sends a gif of the canned bread gag from Spongebob to the chat
@bot.slash_command(name="cannedbread", description='Wow, they have it!')
async def cannedbread(ctx):
    await ctx.respond("https://tenor.com/view/canned-bread-spongebob-squidward-funny-gif-9683242")

# Sends a random "judgement" to judge the current situation. Similar to Magic 8-Ball
@bot.slash_command(name="judgement", description='BreadBot judges the situation')
async def judgement(ctx):
    embed=discord.Embed(title="Bread Bot says...")
    selection = 0
    selection = random.randint(0, len(judgement_list) - 1)
    embed.description = judgement_dict[judgement_list[selection]]
    embed.set_image(url=judgement_list[selection])
    await ctx.respond(embed=embed)

# Rolls a random "level" and outputs the corresponding level of bread. Very silly, but addicting
@bot.slash_command(name="bread-roll", description= 'How powerful will your bread be?')
async def bread_roll(ctx):
    level = random.randint(1, 999)
    for i in range (0, len(rolls)):
        if level <= int(rolls[i][0]):
            roll_index = i
            break
    
    embed=discord.Embed(title=ctx.user.display_name + " rolled...")
    if (int(rolls[roll_index][0]) <= 99):
        embed.description = "A level " + str(level) + " " + rolls[roll_index][2] + "..."
    elif (int(rolls[roll_index][0]) <= 998):
        embed.description = "A level " + str(level) + " " + rolls[roll_index][2] + "!"
    else:
        print("THE LEGENDARY LEVEL 999 EVERYTHING BAGEL!!!")
    
    embed.set_thumbnail(url=ctx.user.display_avatar)
    embed.set_image(url=rolls[roll_index][1])
    await ctx.respond(embed=embed)


bot.run(key)