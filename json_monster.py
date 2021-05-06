import discord, os, commentjson

MIN_MESSAGE_LENGTH = 60
MIN_JSON_RATIO = 0.5

# main()

client = discord.Client()


class ConfigManager():
    CONFIG_PATH = os.path.join(os.getcwd(), "config.json")

    @staticmethod
    def fetch_config():
        with open(ConfigManager.CONFIG_PATH, "r") as f:
            return commentjson.load(f)

    @staticmethod
    def save_config(data):
        with open(ConfigManager.CONFIG_PATH, 'w') as f:
            commentjson.dump(data, f, indent=2)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(name='your JSON', type=discord.ActivityType.watching))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content
    valid = False

    try:

        data = commentjson.loads("{" + text + "}")
        valid = True
    except:
        pass

    try:
        data = commentjson.loads("[" + text + "]")
        valid = True
    except:
        pass

    try:
        data = commentjson.loads(text)
        valid = True
    except:
        pass

    try:
        if valid and len(text) > MIN_MESSAGE_LENGTH:
            data_string = commentjson.dumps(data, indent=2)
            if data_string.startswith("{") or data_string.startswith("["):
                channel = message.channel
                await message.delete()
                send = await message.channel.send(
                    "**Hey {}, I've formatted your json for you!**\n*Use `?format` for instructions on formatting your own json.*\n```json\n{}``` \n to delete this message react with a 🗑️".format(
                        message.author.display_name, data_string))
                send

                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) == '🗑️'

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    return
                else:
                    await send.delete()
    except Exception as exception:
        print(exception)


client.run(ConfigManager.fetch_config().get("token"))
