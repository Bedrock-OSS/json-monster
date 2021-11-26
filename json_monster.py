import discord, os, commentjson, asyncio, time ##Time is used for a slight wait for message deletion and comment json is used to accept json using comments
 
MIN_MESSAGE_LENGTH = 60
MIN_JSON_RATIO = 0.5

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

    text = message.content.rstrip(',')## Removes trailing commas which break the json formatting making it be wrapped in []
    text = text.replace("```", "") ##This may cause issues if someone has a name like `````` but i doubt that would happen and it would break formatting anyways so ¯\_(ツ)_/¯
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
            data_string = commentjson.dumps(data, indent=2) ## CommentJson allows json with commas to be processed works exact same as normal json module
            if data_string.startswith("{") or data_string.startswith("["):
                channel = message.channel
                ## Variable send is the message sent, we are looking for reactions and delete the message if we detect the correct reaction from the correct user
                send = await message.channel.send(
                    "**{},**\n To delete this message react with a 🚫.\n```json\n{}``` \n ".format(
                        message.author.display_name, data_string))
                send
                await send.add_reaction('🚫') #Adds reaction for message deletion
                time.sleep(0.2)
                await message.delete()
                def check_reactions(reaction, user) -> bool:
                    return user.id==message.author.id and reaction.emoji=='🚫' and reaction.message.id==send.id
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check_reactions)
                except asyncio.TimeoutError:
                    await send.clear_reactions()
                    await send.edit(content="**{}:**\n```json\n{}``` \n ".format(
        message.author.display_name, data_string))
                    return
                else:
                    await send.delete()
    except Exception as exception:
        print(exception)


client.run(ConfigManager.fetch_config().get("token"))
