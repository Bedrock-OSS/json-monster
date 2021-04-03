import json
from json import JSONDecoder
import discord
import json
import os

MIN_MESSAGE_LENGTH = 60
MIN_JSON_RATIO = 0.5

# main()

client = discord.Client()

class ConfigManager():
    CONFIG_PATH = os.path.join(os.getcwd(), "config.json")

    @staticmethod
    def fetch_config():
        with open(ConfigManager.CONFIG_PATH, "r") as f:
            return json.load(f)
    
    @staticmethod
    def save_config(data):
        with open(ConfigManager.CONFIG_PATH, 'w') as f:
            json.dump(data, f, indent=2)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content
    valid = False

    try:
        data = json.loads("{" + text + "}")
        valid = True
    except: pass

    try:
        data = json.loads("[" + text + "]")
        valid = True
    except: pass

    try:
        data = json.loads(text)
        valid = True
    except: pass


    try:
        if valid and len(text) > MIN_MESSAGE_LENGTH:
            data_string = json.dumps(data, indent=2)
            if data_string.startswith("{") or data_string.startswith("["):
                await message.channel.send("**Hey {}, I've formatted your json for you!**\n*Use `?format` for instructions on formatting your own json.*\n```json\n{}```".format(message.author.display_name, data_string))
                await message.delete()
    except Exception as exception:
        print(exception)

client.run(ConfigManager.fetch_config().get("token"))