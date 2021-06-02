# libs
import os
import sys
import asyncio
from discord.ext import commands

# vars
userlimit = int(input("Enter needed messages count:\n "))
extcoords = str(input("Do you want to extract minecraft coordinates from all DM? (y/n)\n "))
mode = ""
if extcoords == "y":
    mode = str(input("Mode for coord-extracting (Special/Normal <recommended>):\n "))
    if mode != "normal" and mode != "Normal" and mode != "special" and mode != "Special":
        # exit if invalid argument
        sys.exit("Invalid argument!")
    if mode == "special" or "Special":
        cwords = ['незер','оверворлд','овер','мир','ад','магистрал','+x','-x','+z','-z','x','z','энд']
    elif mode == "normal" or "Normal":
        cwords = ['незер','оверворлд','овер','мир','ад','магистрал','энд','-','+','0к','1к','2к','3к','4к','5к','6к','7к','8к','9к','nether','overworld','highway','high-way','high way','over-world','over-world','end','ender']
if extcoords != "y" and extcoords != "n":
    # exit if invalid argument
    sys.exit("Invalid argument!")
# discord client settings
client = commands.Bot(self_bot=True)

# on ready event
@client.event
async def on_ready():
    # making new dirs and files if it doesnt exists
    if not os.path.exists('DMs'):
        os.makedirs('DMs')
    if extcoords == "y":
        if not os.path.exists('Coords'):
            os.makedirs('Coords')
            coordsfile = open("Coords/result.txt",'a', encoding='UTF-8')
        else:
            if os.path.exists('Coords/result.txt'):
                os.remove('Coords/result.txt')
                coordsfile = open("Coords/result.txt",'a', encoding='UTF-8')
    # getting all private channels (DMs)
    for ch in client.private_channels:
        print(f"Please wait, getting DMs... ({ch})")
        # getting private channel history
        messages = await ch.history(limit=userlimit).flatten()
        # creating name for file (Channel name.txt (without \, /, :, *, ?, ', <, >, |))
        wchname = str(ch).replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','')+".txt"
        dmfile = open("DMs/"+wchname,'a', encoding='UTF-8')
        # getting message from private channel history (messages reversed for normal message list - from bottom to top)
        for msg in messages[::-1]:
            print(f"Please wait, getting {ch} history...")
            dmfile.write(f"{msg.author} {str(msg.created_at)[:-7]}: {msg.content}\n")
            # extracting minecraft coordinates from private channels
            if extcoords == "y":
                print("OK! Exporting DMs completed!\nStarting coord-extracting.")
                print(f"Please wait, extracting minecraft coordinates from {ch}...")
                if mode == "Special" or "special":
                    for cwrd in cwords:
                        if cwrd in msg.content:
                            coordsfile.write(f"{msg.author} {str(msg.created_at)[:-7]}: {msg.content}\n")
                elif mode == "Normal" or "normal":
                    for word in msg.content:
                        if word.isdigit():
                            if msg.content not in coordsfile:
                                coordsfile.write(f"{msg.content}")
                            else:
                                pass
    await asyncio.sleep(1)
    print("Successful DMs exporting!")

# run
token = str(input("Token: "))
client.run(token, bot=False)