import os
import requests
from random import randint
import sys
import discord
from discord.ext import commands
from py3pin.Pinterest import Pinterest

# Check arguments
if len(sys.argv) < 4:
    print("Usage: python3 bot.py <bot_token>  <pinterst_username> <pinterst_email> <pinterst_password>")
    sys.exit(1)


# Utils
def get_random_meme_url():
    # Get random pin
    pin = pins[randint(0, len(pins) - 1)]
    # Get pin's image url
    pin_info = pinterest.load_pin(pin_id=pin.get('id'))
    print(pin_info)
    image_url = pin_info.get('images').get('orig').get('url')
    print("Meme: " + image_url)
    return image_url


def download_image(url):
    image = requests.get(url)
    # Save image
    with open('meme.jpg', 'wb') as f:
        f.write(image.content)
        f.close()
    return open('meme.jpg', 'rb')


# Initialize pinterest
pinterest = Pinterest(email=sys.argv[3],
                      password=sys.argv[4],
                      username=sys.argv[2],
                      cred_root='cred_root')
pinterest.login()

# Get meme board id
memes_board_id = ""
for board in pinterest.boards():
    if board['name'] == 'Memes':
        memes_board_id = board['id']
        break
print("Memes board id: " + memes_board_id)

# Create bot
bot = commands.Bot(command_prefix='!')

bot.activity = discord.Game(name="!eh")

# Getting all the pins from the board.
pins = pinterest.board_feed(board_id=memes_board_id)


# Commands
@bot.command()
async def eh(ctx):
    meme = download_image(get_random_meme_url())
    await ctx.send(file=discord.File(meme, 'meme.jpg'))
    os.remove('meme.jpg')


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def eh_help(ctx):
    await ctx.send("!eh - Get a random meme\n!ping - Pong!\n!eh_dev - about developer\n"
                   "!eh_src - get source code\n!eh_help - help")


@bot.command()
async def eh_dev(ctx):
    await ctx.send("Anas Elgarhy - https://github.com/anas-elgarhy")


@bot.command()
async def eh_src(ctx):
    await ctx.send("https://github.com/anas-elgarhy/eh")

# Run bot
bot.run(sys.argv[1])
