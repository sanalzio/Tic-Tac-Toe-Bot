# --------------------- Main --------------------- #
# * Imports
import disnake as discord
import modules.PyDB as PyDB
import asyncio
# import os
# from keep_alive import keep_alive

# * Vars
# Bot Vars
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
hembed=discord.Embed(title="Tic-Tac-Toe Bot help", color=0x349F4F, )
hembed.add_field(name="Commands:",value="__`xox play`__ play with ai or use `xox play easy` to play in easy mode\n\n__`xox help`__ view this menu or use `xox?`", inline=False)
hembed.set_thumbnail(url="https://repository-images.githubusercontent.com/707530353/e59ca42a-750b-470b-8207-9f6c807fd251")
# Config Vars
config = PyDB.pydb("database/config")

async def replytxt(messagevar, msg):
    return await messagevar.reply(msg, mention_author=True)




# * Game
import random
from bgm import *

mybgm=bgm()
mybgm.loadmodel("xox")

async def inp(thismsg, msg, txt=""):
    if txt!="": await replytxt(msg, txt)
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=lambda r, u: r.message.id==thismsg.id and u.id != client.user.id)
        if reaction:
            await reaction.message.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji)=="❌":
                await replytxt(msg, "The game is ending.")
                return 0
            return str(reaction.emoji).replace("1️⃣", "1").replace("2️⃣", "2").replace("3️⃣", "3").replace("4️⃣", "4").replace("5️⃣", "5").replace("6️⃣", "6").replace("7️⃣", "7").replace("8️⃣", "8").replace("9️⃣", "9")
    except asyncio.TimeoutError:
        await replytxt(msg, "The game is ending as 1 minute has elapsed.")
        return 0
    """while db.control(str(msg.author.id)+"input")==False:
        pass
    data=db.getData(str(msg.author.id)+"input")
    db.removeData(str(msg.author.id)+"input")
    return data"""

def board2msg(board):
    i = 0
    bo="```\n"
    while i < 9:
        bo+=board[i]+" "+board[i+1]+" "+board[i+2]+"\n"
        i += 3
    bo+="```"
    return bo


async def get_player_move(board, player, msg, tmsg, simple):
    if player == "X":
        move = await inp(tmsg, msg)
        if move==0:
            return "stop"
        while move not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            move = await inp(tmsg, msg)
        while board[int(move)-1] != "-":
            move = await inp(tmsg, msg, "That section is already full, please make a valid move.")
        return int(move) - 1
    else:
        if simple:
            move = random.randint(0, 8)
            while board[move] != "-":
                move = random.randint(0, 8)
            return move
        move=mybgm.getprediction(board)
        if move!=None:
            return int(move)-1
        move = random.randint(0, 8)
        while board[move] != "-":
            move = random.randint(0, 8)
        return move


def make_move(board, player, move):
    board[move] = player


def check_winner(board):
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != "-":
            return board[i]
    for i in range(3):
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] != "-":
            return board[i * 3]
    if board[0] == board[4] == board[8] != "-":
        return board[0]
    if board[2] == board[4] == board[6] != "-":
        return board[2]
    return None


def is_full(board):
    for cell in board:
        if cell == "-":
            return False
    return True


async def main(msg, tmsg, simple=False):
    board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    player=random.randint(1,2)
    player = "X" if player==1 else "O"
    while True:
        if player=="X": await tmsg.edit(content=board2msg(board))
        move = await get_player_move(board, player, msg, tmsg, simple)
        if move=="stop":
            return
        make_move(board, player, move)
        winner = check_winner(board)
        if winner is not None:
            await tmsg.edit(content=board2msg(board))
            await replytxt(msg, "You won!" if winner=="X" else "You loss!")
            break
        player = "O" if player == "X" else "X"
        if is_full(board):
            await tmsg.edit(content=board2msg(board))
            await replytxt(msg, "Draw!")
            break



# * Index
# On Ready Function
@client.event
async def on_ready():
    activity = discord.Activity(
        name=config.status, type=eval("discord.ActivityType." + config.ActivityType)
    )
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("I'm Ready")

# On Message Function
@client.event
async def on_message(message):
    prefix = "xox "
    if message.content.lower()=="xox?": await message.reply(embed=hembed); return
    try:
        arg = message.content.split(" ")[1:]
        cmd= message.content.split(" ")[1]
    except IndexError: pass
    if message.author.id == client.user.id: return
    if not message.content.lower().startswith(prefix): return
    if cmd.lower()=="play":
        new_msg = await message.reply(board2msg(["-", "-", "-", "-", "-", "-", "-", "-", "-"]), mention_author=True)
        await new_msg.add_reaction("1️⃣")
        await new_msg.add_reaction("2️⃣")
        await new_msg.add_reaction("3️⃣")
        await new_msg.add_reaction("4️⃣")
        await new_msg.add_reaction("5️⃣")
        await new_msg.add_reaction("6️⃣")
        await new_msg.add_reaction("7️⃣")
        await new_msg.add_reaction("8️⃣")
        await new_msg.add_reaction("9️⃣")
        await new_msg.add_reaction("❌")
        if len(arg)>1:
            if arg[1].lower()=="easy":
                await main(message, new_msg, True)
        else: await main(message, new_msg)
    if cmd.lower()=="help": await message.reply(embed=hembed)

# On Reaction Function
'''@client.event
async def on_raw_reaction_add(payload):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await client.fetch_user(payload.user_id)
    emoji = payload.emoji
    if user.id==client.user.id:
        return
    #await message.remove_reaction(emoji, user)
    """if db.control(str(user.id)+"input"):
        db.setData(str(user.id)+"input", str(emoji).replace("1️⃣", "1").replace("2️⃣", "2").replace("3️⃣", "3").replace("4️⃣", "4").replace("5️⃣", "5").replace("6️⃣", "6").replace("7️⃣", "7").replace("8️⃣", "8").replace("9️⃣", "9"))
    else:
        db.addData(str(user.id)+"input", str(emoji).replace("1️⃣", "1").replace("2️⃣", "2").replace("3️⃣", "3").replace("4️⃣", "4").replace("5️⃣", "5").replace("6️⃣", "6").replace("7️⃣", "7").replace("8️⃣", "8").replace("9️⃣", "9"))
"""
'''

# * Run Bot
# keep_alive()
# TOKEN = os.environ.get("TOKEN")
client.run(config.token)
