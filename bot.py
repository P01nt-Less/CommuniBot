#imports

import discord
from random import shuffle
import configparser
import random
import requests
import aiohttp
import traceback
import sys
import re
import json
import time
import asyncio
import os
from datetime import datetime
from discord import game
from random import randint
from discord.ext import commands

#bot stuff
bot_prefix = ':', '-', '@CommuniBot ', 'CommuniBot ', '@CommuniBot#4412 ', 'CommuniBot#4412', 'communibot'
bot = commands.Bot(command_prefix=bot_prefix)
bot.remove_command('help')
start_time = time.time()
starttime2 = time.ctime(int(time.time()))
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
config.sections()
Secrets = config['Secrets']


#events   
@bot.event
async def on_ready():
	bot.start_time = time.time()
	print("Online.")
	await bot.change_presence(game=discord.Game(name='on {} servers | -help.'.format(len(bot.servers))), status=discord.Status.online)


#functions
def owner(ctx):
    return ctx.message.author.id == '276043503514025984'
#commands
#owner
@bot.command(pass_context=True)
@commands.check(owner)
async def say(ctx, *, text: str = None):
    """Say something.
    Usage: -say <text>
    Example: -say Potatoes!
    Permission: Bot Owner
    """
    await bot.say(text)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
@commands.check(owner)
async def shutdown(ctx):
    """Shutdown.
    Usage: -shutdown
    Permission: Bot Owner
    """
    await bot.say('Shutting down.')
    await bot.delete_message(ctx.message)
    await bot.logout()

@bot.command(pass_context=True)
@commands.check(owner)
async def servers(ctx):
    """See the list of servers.
    Usage: -servers
    Permission: Bot Owner
    """
    msg = ""
    for server in bot.servers:
        name = str(server) + "\n"
        msg += name
    embed=discord.Embed(description=f'{msg}', color=0x2874A6)
    await bot.delete_message(ctx.message)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
@commands.check(owner)
async def leaveserver(ctx, serverid: str):
    """Leave a server.
    Usage: -leaveserver <Server ID>
    Example: -leaveserver 123456789
    Permission: Bot Owner
    """
    server = bot.get_server(serverid)
    if server:
        await bot.leave_server(server)
        msg = '{} = Left server!'.format(server.name)
    else:
        msg1 = ':x: I could not find the ID of that server or you just forgot to say ID of the server!'
        return await bot.say(msg1)
    await bot.say(msg)

#ping
@bot.command(pass_context=True)
async def ping(ctx):
    '''Check how fast the bot responds.
    Usage: -ping
    '''
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await bot.send_typing(channel)
    t2 = time.perf_counter()
    embed=discord.Embed(description='Pong! {} milliseconds.'.format(round((t2-t1)*1000)), color=0x2874A6)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def prefixes(ctx):
    '''Check all of CommuniBot's prefixes.
    Usage: -prefixes
    '''
    embed=discord.Embed(description='My prefix are: **-**, **:**,**@CommuniBot**, **CommuniBot**, **@CommuniBot#4412**, **CommuniBot#4412** and **communibot**.',color=0x2874A6)
    await bot.say(embed=embed)

#help
@bot.command(pass_context=True)
async def help(ctx):
    '''See all of the commands from here.
    Usage: -help
    '''
    embed=discord.Embed(description='Help\nPrefixes: -prefixes\n-ping - Shows the amount of milliseconds taken to respond.\n-info - Shows information about CommuniBot!\n-uptime - Shows the uptime status of CommuniBot!\n\n\n-jokes + \nShows a list of joke commands.\n\n-actions + \nShows a list of action commands.\n\n-moderation +\nShows a list of moderation commands.\n\n-fun +\nShows a list of fun commands.\n\n-server +\nLists commands about the server.\n\n-utilities +\nShows a list of commands about utilities.', color=0x2874A6)
    await bot.say(embed=embed)

@bot.group(pass_context=True)
async def fun(ctx):
    '''See all of the fun commands from here.
    Usage: -fun
    '''
    if ctx.invoked_subcommand is None:
        embed=discord.Embed(description='Fun commands\n\n\n-coinflip\nThe bot chooses between heads or tails.\n\n-8ball\nUse the magic 8ball!\n\n-comic\nShows a random comic.\n\n-cat\nShows a random cat picture.\n\n-dog\nShows a random dog picture.\n\n-say\nSay anything after the command and it will repeat it back.\n\n-choose\nMake CommuniBot choose over three or more things.\n\n-roll\nRoll any number above one.\n\n-roast\nRoast someone with a burning statement.\n\n-memes\nRandomizes between lots of memes.\n\n-piglatin\nTranslate your text into piglatin.', color=0x2874A6)
        await bot.say(embed=embed)
@bot.command(pass_context=True)
async def coinflip(ctx):
    '''Flip a coin to either land on heads or tails.
    Usage: -coinflip
    '''
    choice = random.choice(['Heads!','Tails!'])
    await bot.say(choice)
@bot.command(name="8ball", pass_context=True, aliases=['eightball'])
async def _8ball(self, *, question : str):
    '''Ask the bot a question and it will answer.
    Usage: -8ball <text>?
    Example: -8ball Is this question a question?
    '''
    responses = [["Signs point to yes.", "Yes.", "Without a doubt.", "As I see it, yes.", "You may rely on it.", "It is decidedly so.", "Yes - definitely.", "It is certain.", "Most likely.", "Outlook good."],
    ["Reply hazy, try again.", "Concentrate and ask again.", "Better not tell you now.", "Cannot predict now.", "Ask again later."],
    ["My sources say no.", "Outlook not so good.", "Very doubtful.", "My reply is no.", "Don't count on it."]]
    if "?" in question:
        await self.bot.say(":8ball:" + random.choice(random.choice(responses)))
    else:
        await self.bot.say("That doesn't look like a question. You need to put a question mark at the end of your sentence.")
@bot.command(pass_context=True, no_pm=True)
async def comic(ctx):
    '''Check out a random comic.
    Usage: -comic
    '''
    api = "https://xkcd.com/{}/info.0.json".format(random.randint(1, 1800))
    async with aiohttp.ClientSession() as session:
        async with session.get(api) as r:
            response = await r.json()
            embed = discord.Embed(title="Comic", description=response["title"], color=0xFF0000)
            embed.set_image(url=response["img"])
            await bot.say(embed=embed)

@bot.command(pass_context=True)
async def cat(ctx):
    '''Check out a random cat.
    Usage: -cat
    '''
    api = 'https://random.cat/meow'
    async with aiohttp.ClientSession() as session:
        async with session.get(api) as r:
            if r.status == 200:
                response = await r.json()
                embed = discord.Embed(title="Cat", description="Here's your random cat image", color=0xFF0000)
                embed.set_author(name=f"{ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
                embed.set_image(url=response['file'])
                await bot.say(embed=embed)
            else:
                await bot.say('Could not access random.cat API!')

@bot.command(pass_context=True)
async def dog(ctx):
    '''Check out a random dog.
    Usage: -dog
    '''
    api = "https://api.thedogapi.co.uk/v2/dog.php"
    async with aiohttp.ClientSession() as session:
        async with session.get(api) as r:
            if r.status == 200:
                response = await r.json()
                embed = discord.Embed(title="Dog", description="Here's your random Dog", color=0xFF0000)
                embed.set_author(name=f"{ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
                embed.set_image(url=response['data'][0]["url"])
                await bot.say(embed=embed)
            else:
                x = "Could not find a dog :sad:!"
                embed = discord.Embed(title='Error', color=colorfail)
                embed.description = x
                await bot.say(embed=embed)

@bot.command(name='choose', aliases=['select','choice'],pass_context=True)
async def choose(self, ctx, *args):
    '''Make the bot choose over two or more things.
    Usage: -choose <one> <two> <three> <etc>
    Example: -choose Potatoes Tomatoes Unicorns Carrots
    '''
    choice = random.choice(args)
    await bot.say(f'**`{choice}`**')

@bot.command(pass_context=True)
async def roll(ctx, number: int=100):
    '''Rolls a random number. If no number is put in, it will choose 100. It must be higher than one.
    Usage: -roll <number>
    Example: -roll 1242
    '''
    if number > 1:
        await bot.say(f"{ctx.message.author.mention} | :game_die: {randint(1, number)}")
    else:
        await bot.say(f"{ctx.message.author.mention} Please insert a number higher than one.")

@bot.command(pass_context=True)
async def roast(ctx, person: discord.Member):
    '''Roast someone.
    Usage: -roast <@person>
    Example: -roast @Pointless
    '''
    roast_possible_responses = ["{}, your ass must be pretty jealous of all the shit that comes out of your mouth.","{}, some day you'll go far, and I hope you stay there.","{}, I'm trying my absolute hardest to see things from your perspective, but I just can't get my head that far up my ass.","{}, I'm not a protocolgist, but I know an asshole when I see one.","{}, Do yourself a favor and ignore anyone who tels you to be yourself. Bad idea in your case.","{}, Everyone's entitled to act stupid once in awhile, but you really abuse the privilege.","{}, Can you die of constipation? I ask because I'm worried about how full of shit you are.","{}, Sorry, I didn't get that. I don't speak bullshit.","{}, There are some remarkably dumb people in this world. Thanks for helping me understand that.","{}, I could eat a bowl of alphabet soup and shit out a smarter statement than whatever you just said.","{}, You always bring me so much joy, as soon as you leave the room.","{}, I'd tell you how I really feel, but I wasn't born with enough middle fingers to express myself in this case.","{}, You have the right to remain silent because whatever you say will probably be stupid anyway.","{}, your family tree must be a cactuss because you're all a bunch of pricks.","{}, You'll never be the man your mom is.","{}, If laughter is the best medicine, your face must be curing the world.","{}, scientists say the universe is made up of neutrons, protons and electrons. They forgot to mention morons, as you are one.","{}, if you really want to know about mistakes, you should ask your parents.","{}, I thought of you today. It reminded me to take the garbage out.","{}, you're such a beautiful, intelligent, wonderful person. Oh I'm sorry, I thought we were having a lying competition.","{}, I may love to shop but I'm not buying your bullshit.","{}, I just stepped in something that was smarter than you, and smelled better too."]
    roast_current_response = random.choice(roast_possible_responses)
    await bot.say(roast_current_response.format(person.mention))

@bot.command(pass_context=True, aliases=['meme'])
async def memes(ctx):
    '''Randomizes between lots of memes
    Usage: -memes
    '''
    memes_possible_responses = ['{} https://upload.wikimedia.org/wikipedia/commons/a/ab/Lolcat_in_folder.jpg','{} https://upload.wikimedia.org/wikipedia/commons/1/1a/Cat_crying_%28Lolcat%29.jpg','{} http://i0.kym-cdn.com/photos/images/original/001/284/242/202.jpg','{} https://i.ytimg.com/vi/6HA2D3LsJQs/hqdefault.jpg','{} http://www.lolcats.com/images/u/11/43/lolcatsdotcomsyucc7vghgeu3ygu.jpg','{} https://shesaid.com/wp-content/uploads/2016/09/7Ak9p.jpg','{} https://i.ytimg.com/vi/Bkco3bE2tg8/hqdefault.jpg','{} https://vignette.wikia.nocookie.net/epicrapbattlesofhistory/images/1/15/LOLCATS-Cloud.jpeg/revision/latest?cb=20140723224315','{} https://i.chzbgr.com/full/9089826560/h07C1DAA9/','{} https://media.mnn.com/assets/images/2012/11/lolcat_main_0.jpg','{} https://i.pinimg.com/736x/aa/3c/0f/aa3c0f3dd59210f9953a5c1c0d46c2d6--funny-pets-funny-animals.jpg','{} https://img.scoop.it/NhznTvgS8CGETQOQgXJ3DDl72eJkfbmt4t8yenImKBVvK0kTmF0xjctABnaLJIm9','{} https://www.oddee.com/wp-content/uploads/_media/imgs/articles2/a97873_rsz_drunkdial.jpg','{} https://i.chzbgr.com/full/9107324928/h0A65249F/','{} https://i.ytimg.com/vi/IaK6EUSUG4I/hqdefault.jpg','{} https://blogs.loc.gov/digitalpreservation/files/2014/07/864385794_40eef8f22b_z1.jpg','{} https://i.chzbgr.com/full/9101861888/h2C7008DC/','{} http://i0.kym-cdn.com/photos/images/facebook/001/031/948/10b.jpg','{} http://i0.kym-cdn.com/photos/images/facebook/000/559/061/d94.png','{} https://pics.me.me/my-cat-made-this-face-when-i-meowed-back-at-8561541.png','{} http://www.lolcats.com/images/u/12/43/lolcatsdotcomnapkin.jpg','{} https://longlivethekitty.com/wp-content/uploads/lolcat_airplane.jpg','{} http://www.lolcats.com/images/u/08/39/lolcatsdotcomly2r5yakozqlbhmn.jpg','{} http://firstmonday.org/ojs/index.php/fm/article/viewFile/5391/4103/40381','{} https://bighugelabs.com/img/lolcat-sample.jpg','{} http://static.wixstatic.com/media/8e31f964a29559e19acfb44ea027ab0c.wix_mp_1024','{} http://www.rationalitynow.com/blog/wp-content/uploads/2009/12/owlcatl.jpg','{} http://i0.kym-cdn.com/photos/images/facebook/000/519/843/833.jpg','{} http://runt-of-the-web.com/wordpress/wp-content/uploads/2017/01/wrong-answer-you-aint-cheat.jpg','{} http://i.imgur.com/yYT55QA.jpg','{} http://i0.kym-cdn.com/photos/images/original/001/209/914/6b4.jpg','{} http://i0.kym-cdn.com/photos/images/original/001/209/916/fe7.jpg','{} https://i.imgur.com/XuFg46x.jpg','{} https://i.imgur.com/vlA7u5k.jpg','{} https://stepcdn.com/assets/2017-02/03/11/8e3r2/trump-twitter-700x.jpg','{} http://runt-of-the-web.com/wordpress/wp-content/uploads/2017/01/adding-salt-to-your-drama.jpg','{} http://i0.kym-cdn.com/photos/images/original/001/211/181/422.jpg','{} https://pics.me.me/when-you-use-furthermore-in-your-essay-im-missing-the-25131584.png','{} https://pics.me.me/when-you-use-furthermore-in-your-essay-sprinkle-dat-extra-16049743.png','{} https://ecdn.teacherspayteachers.com/thumbitem/-Salt-Bae-Meme-Writing-Freebie-2978990-1485278672/original-2978990-1.jpg','{} https://pics.me.me/when-black-parents-add-an-apostrophe-to-their-childs-name-11763958.png','{} http://i0.kym-cdn.com/photos/images/facebook/001/209/136/1ef.png','{} https://pics.me.me/your-head-salt-bae-who-won-the-meme-battle-for-13363207.png','http://runt-of-the-web.com/wordpress/wp-content/uploads/2017/01/Caucasian-on-your-cv.jpg','{} https://lh3.googleusercontent.com/vnCrrk7gvVIoLQsV4HnLiabPXqKA7ls86cm-2Snuk-B9NOup-OtblK8UXYdo3qhBIk7SqtOTUEVpIOMnYmAzJ_H1jKIsJ8ElWPipvAkUthqAxhtwG1ar3ANnuFdC5pTbeNrqb8Q-','{} https://pics.me.me/cheating-lies-deceit-ent-unfaithful-god-when-he-was-creating-11587232.png','{} https://pics.me.me/mexico-autodeciaraodny-autobusas-rapid-a-pre-playas-de-tijuana-ropuerto-11675269.png','{} https://pics.me.me/thedukeofmeines-edukeof-memes-saltbae-911-jetfeul-steelbeams-twintowers-bush-proof-12396857.png','{} https://static.boredpanda.com/blog/wp-content/uploads/2017/01/818286176889085952-png__700.jpg','{} https://i.imgflip.com/vgh66.jpg','{} http://s2.quickmeme.com/img/b0/b0039e31a5f5ff0fbf9336d47e5d3ec2a80232f3e31e10883c15dbc66be3809d.jpg','{} http://weknowmemes.com/generator/uploads/generated/g1365444091774137766.jpg','{} https://i.chzbgr.com/original/1738866432/hC0106396/','{} http://www.imagefully.com/wp-content/uploads/2015/08/I-Dunno-Lol-Dog-Image.jpg','{} http://images4.fanpop.com/image/photos/15900000/lol-dogs-dogs-15905734-500-375.jpg','{} http://4.bp.blogspot.com/-Rny6ymoavqs/UAhodFDkDPI/AAAAAAAAsiU/8nUf9LUjGyw/s1600/funny-dog-pictures-there-there-ugly-bald-puppy.jpg','{} http://images6.fanpop.com/image/photos/37300000/Funny-Dogs-dogs-37339100-421-428.jpg','{} https://ilifejourney.files.wordpress.com/2012/10/dog-and-spiders.jpg','{} https://i1.wp.com/thefunniestpictures.com/wp-content/uploads/2014/08/Funny-Dog-1.jpg?fit=499%2C334&ssl=1','{} https://ci.memecdn.com/722962.jpg','{} https://collarfolk.com/wp-content/uploads/2017/05/8963bb3fdd1f319b0154cc646a0de37a.jpg','{} https://memegenerator.net/img/instances/500x/64586542/oh-por-deus.jpg','{} https://imgfave.azureedge.net/image_cache/1383619315754765.jpg','{} https://www.seabreeze.com.au/Img/Photos/Other/3722545.jpg','{} http://blogs.discovermagazine.com/discoblog/files/2012/10/dog_meme.jpeg','{} https://static.fjcdn.com/pictures/Lol_98ff89_2584253.jpg','{} http://i0.kym-cdn.com/photos/images/facebook/000/151/934/imade40cakes128548225192353750.jpg','{} http://s2.quickmeme.com/img/a7/a70f44decdb833e94ed530c63cce6775182c03a2f8d5f8301114b52f9724ce80.jpg','{} http://funnyanimalphoto.com/wp-content/uploads/2013/10/dog_loves_bacon.jpg?bd03d3','{} http://s2.quickmeme.com/img/fc/fc02f94bf37ff24f18337ac7de31631ef2b35296e87409184aef259c94f53d1d.jpg','{} https://i.imgur.com/u7mM6mE.jpg', '{} https://i.pinimg.com/736x/71/27/71/712771dd7c68cb9c3ccccc69a9f2e953--bit.jpg','{} https://cdn.discordapp.com/attachments/393566779269709824/396739756437929984/doggie.gif\nCredit to @Windfave#5304.']
    memes_current_response = random.choice(memes_possible_responses)
    await bot.say(memes_current_response.format(ctx.message.author.mention))
#info
@bot.command(pass_context=True, aliases=['botinfo','information','botinformation','binfo','boti','binformation'])
async def info(ctx):
    '''Tells you information about the bot.
    Usage: -info
    '''
    member = ctx.message.author
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)

    join = discord.Embed(description= '',title = 'Information about CommuniBot', colour = 0xFFFF);
    join.add_field(name = '__Information__', value = f"This bot was made in discord.py and was created by <@276043503514025984> (Pointless). It is for a bot that has moderation, fun commands, memes and more. It aims to make communities get less bots in total, so it doesn't look like there's too much bots in the Member list.", inline=True);
    join.add_field(name = '__Creator__', value = f"<@276043503514025984> - Created the the bot and all the commands, except for the ones who created some.", inline=True);
    join.add_field(name = '__Helped__', value = f"<@338600456383234058> - Created -say (for owner) and -poll command.", inline=True)
    join.add_field(name = '__Status__', value = f"Uptime: I've been online for %d week(s), %d day(s), %d hour(s), %d minute(s), %d second(s)!" % (week, day, hour, minute, second) + "\nTotal Servers: {} servers.".format(len(bot.servers)), inline=True)
    join.add_field(name = '__Links__', value = f"Invite link for the bot: https://discordapp.com/oauth2/authorize?client_id=406890237604790302&scope=bot&permissions=2146958591\nInvite link for the support server: https://discord.gg/Fz2pKVE\nLink for Discord Bots: https://discordbots.org/bot/406890237604790302\nLink for Github page: https://github.com/P01nt-Less/CommuniBot\nLink for Reddit page: https://www.reddit.com/r/The_Community/", inline=True)

    return await bot.say(embed = join);
    await bot.say(embed=embed)

#actions
@bot.group(Pass_context=True)

async def actions(ctx):
    '''Shows the action commands.
    Usage: -action
    '''
    if ctx.invoked_subcommand is None:
        embed=discord.Embed(description='Action commands\n\n\n-punch\nPunches someone you\'d like to do that to.\n\n-legkick\nKicks anyone you like.\n\n-hug\nHugs anyone you like.\n\n-kiss\nKiss anyone you like.\n\n-uppercut\nUppercut anybody you like.\n\n-wave\nWave at anyone you\'d like to.\n\n-smile\nJust smile.\n\n-frown\nFrown. :(\n\n-slap\nSlap anyone you like.\n\n-stab\nStab people! Muehehehe!\n\n-murder\nMurder someone...\n\n-shoot\nShoot a person! Dun dun dunn!!', color=0x2874A6)
        await bot.say(embed=embed)

@bot.command(pass_context=True)

async def punch(ctx, person: discord.Member): 
    '''Punch someone.
    Usage: -punch <@person>
    Example: -punch @Pointless
    '''
    punch_possible_responses = ["{} punched {} in the face, in the face."]
    punch_current_response = random.choice(punch_possible_responses)
    await bot.say(punch_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)

async def legkick(ctx, person: discord.Member):
    '''Kick someone.
    Usage: -legkick <@person>
    Example: -legkick @Pointless
    '''
    kick_possible_responses = ["{} kicked {} in the leg."]
    kick_current_response = random.choice(kick_possible_responses)
    await bot.say(kick_current_response.format(ctx.message.author.mention, person.mention))	
@bot.command(pass_context=True)

async def hug(ctx, person: discord.Member):
    '''Hug someone.
    Usage: -hug <@person>
    Example: -hug @Pointless
    '''
    hug_possible_responses = ["{} hugged {} tightly."]
    hug_current_response = random.choice(hug_possible_responses)
    await bot.say(hug_current_response.format(ctx.message.author.mention, person.mention))	
@bot.command(pass_context=True)

async def kiss(ctx, person: discord.Member):
    '''Kiss someone.
    Usage: -kiss <@person>
    Example: -kiss @Pointless
    '''
    kiss_possible_responses = ["{} kissed {} on the cheek."]
    kiss_current_response = random.choice(kiss_possible_responses)
    await bot.say(kiss_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)

async def uppercut(ctx, person: discord.Member):
    '''Uppercut someone.
    Usage: -uppercut <@person>
    Example: -uppercut @Pointless
    '''
    uppercut_possible_responses = ["{} uppercut {} and turned {} into a giraffe."]
    uppercut_current_response = random.choice(uppercut_possible_responses)
    await bot.say(uppercut_current_response.format(ctx.message.author.mention, person.mention, person.mention))
@bot.command(pass_context=True)

async def wave(ctx, person: discord.Member):
    '''Wave at someone.
    Usage: -wave <@person>
    Example: -wave @Pointless
    '''
    uppercut_possible_responses = ["{} waved at {} with a smile on their face."]
    uppercut_current_response = random.choice(uppercut_possible_responses)
    await bot.say(uppercut_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)

async def smile(ctx):
    '''Just smile.
    Usage: -smile
    '''
    smile_possible_responses = ["{} smiled."]
    smile_current_response = random.choice(smile_possible_responses)
    await bot.say(smile_current_response.format(ctx.message.author.mention))
@bot.command(pass_context=True)

async def frown(ctx):
    '''Just frown.
    Usage: -frown
    '''
    punch_possible_responses = ["{} frowned."]
    punch_current_response = random.choice(punch_possible_responses)
    await bot.say(punch_current_response.format(ctx.message.author.mention))
@bot.command(pass_context=True)

async def slap(ctx, person: discord.Member):
    '''Slap someone.
    Usage: -slap <@person>
    Example: -slap @Pointless
    '''
    slap_possible_responses = ["{} slapped {}'s face making it red. "]
    slap_current_response = random.choice(slap_possible_responses)
    await bot.say(slap_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)

async def stab(ctx, person: discord.Member):
    '''Stab someone.
    Usage: -stab <@person>
    Example: -stab @Pointless
    '''
    slap_possible_responses = ["{} stabbed {} in the heart making his last feeling pain."]
    slap_current_response = random.choice(slap_possible_responses)
    await bot.say(slap_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)

async def murder(ctx, person: discord.Member):
    '''Murder someone.
    Usage: -murder <@person>
    Example: -murder @Pointless
    '''
    slap_possible_responses = ["{} murdered {} with no one knowing anything that happened."]
    slap_current_response = random.choice(slap_possible_responses)
    await bot.say(slap_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)

async def shoot(ctx, person: discord.Member):
    '''Shoot someone.
    Usage: -shoot <@person>
    Example: -shoot @Pointless
    '''
    slap_possible_responses = ["{} shot {} straight in the head making them collapse onto the floor."]
    slap_current_response = random.choice(slap_possible_responses)
    await bot.say(slap_current_response.format(ctx.message.author.mention, person.mention))

#jokes
@bot.group(pass_context=True)

async def jokes(ctx):
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Joke commands\n\n\n-insovietrussia\nThis command randomizes between lots of "In Soviet Russia" jokes.\n\n-chucknorris\nRandomizes between lots of Chuck Norris jokes/facts.\n\n-dadjoke\nRandomizes between lots of really not funny bad Dad jokes!',color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(pass_context=True)

async def insovietrussia(ctx):
    '''Randomizes between lots of insovietrussia jokes.
    Usage: -insovietrussia
    '''
    insovietrussia_possible_responses = ["In America, you drive a car. In Soviet Russia, a car drives you!",  "In America the president gets assassinated. In soviet Russia, the president assassinates you!", "In America, you throw a grenade! In Soviet Russia, a grenade throws you!", "In America, you eat food. In Soviet Russia, food eats you!", "In America, you write 'R'. In Soviet Russia, you write 'Я'!", "In America, you break the law. In Soviet Russia, the law breaks you!", "Roses are red, Violets are blue, In Soviet Russia, a poem writes you!", "In America, the Grinch steals Christmas. In Soviet Russia, Christmas steals the Grinch!", "In America, you laugh at jokes. In Soviet Russia, jokes laugh at you!", "In America, Jesus sacrifices for you. In Soviet Russia, you sacrifice for Jesus!", "In America, Russians spy on you. In Soviet Russia, you spy on Russians!", "In America, you find Waldo. In Soviet Russia, Waldo finds you!", "In America, you call the police. In Soviet Russia, police calls you!", "In America, you watch TV. In Soviet Russia, the TV watches you!", "In America, you eat a cookie. But in Soviet Russia, the cookie eats you!", "In America, you play games. In Soviet Russia, games play you!"]
    insovietrussia_current_response = random.choice(insovietrussia_possible_responses)
    await bot.say(insovietrussia_current_response)
@bot.command(pass_context=True)

async def chucknorris(ctx):
    '''Randomizes between lots of Chuck Norris jokes.
    Usage: -chucknorris
    '''
    chucknorris_possible_responses = ["Chuck Norris threw a grenade and killed 50 people, then it exploded.", "Chuck Norris can kill two stones with one bird.", "Chuck Norris can pick oranges from an apple tree and make the best lemonade you've ever tasted.", "Once a cobra bit Chuck Norris' leg. After five days of excruciating pain, the cobra died.", "When a zombie apocalypse starts, Chuck Norris doesn't try to survive. The zombies do.", "Chuck Norris can hear sign language.", "Chuck Norris beat the sun in a staring contest.","It is considered a great accomplishment to go down Niagara Falls in a wooden barrel. Chuck Norris can go up Niagara Falls in a cardboard box.", "Chuck Norris was once on Celebrity Wheel of Fortune and was the first to spin. The next 29 minutes of the show consisted of everyone standing around awkwardly, waiting for the wheel to stop.", "Giraffes were created when Chuck Norris uppercut a horse.", "When the Bogeyman goes to sleep every night he checks his closet for Chuck Norris.", "When Chuck Norris was in middle school, his English teacher assigned an essay: \'What is courage?\' He received an A+ for turning in a blank page with only his name at the top.", "Chuck Norris will never have a heart attack... even a heart isn't foolish enough to attack Chuck Norris.", "Chuck Norris can kill your imaginary friends.", "Chuck can set ants on fire with a magnifying glass. At night.", "Chuck Norris once went to mars. Thats why there are no signs of life.", "When Bruce Banner gets mad he turns into the Hulk. When the Hulk gets mad he turns into Chuck Norris. When Chuck Norris gets mad, run.", "Chuck Norris is the reason Waldo is hiding.", "Chuck Norris is the only person that can punch a cyclops between the eye.", "When Chuck Norris enters a room, he doesn't turn the lights on, he turns the dark off.", "M.C. Hammer learned the hard way that Chuck Norris can touch this.", "Chuck Norris can build a snowman out of rain.", "Chuck Norris was once charged with three attempted murders in Boulder County, but the Judge quickly dropped the charges because Chuck Norris does not \'attempt\' murder.", "Leading hand sanitizers claim they can kill 99.9 percent of germs. Chuck Norris can kill 100 percent of whatever the hell he wants.", "Chuck Norris's computer has no \'backspace\' button, Chuck Norris doesn't make mistakes.", "Chuck Norris makes onions cry.", "Chuck Norris tells Simon what to do.", "Chuck Norris plays Russian roulette with a fully loaded revolver... and wins."]
    chucknorris_current_response = random.choice(chucknorris_possible_responses)
    await bot.say(chucknorris_current_response)
@bot.command(pass_context=True)

async def dadjoke(ctx):
    '''Randomizes between lots of terrible Dad jokes.
    Usage: -dadjoke
    '''
    chucknorris_possible_responses = ["What time did the man go to the dentist? Tooth hurt-y.","A ham sandwich walks into a bar and orders a beer. \nBartender says, 'Sorry we don't serve food here.'","Whenever the cashier at the grocery store asks my dad if he would like the milk in a bag he replies, 'No, just leave it in the carton!'","Me: 'Dad, make me a sandwich!' \nDad: 'Poof, You’re a sandwich!'","How do you make a Kleenex dance? Put a little boogie in it!","Two peanuts were walking down the street. One was a salted.","We were getting fast food when the lady at the window said, 'Any condiments?' My dad responded, 'Compliments? You look very nice today!'","My dad’s name is Phil, and whenever I finish eating and say, 'Dad, I’m full,' he always replies, 'No, I’m full; you're Ruby.'","I'm reading a book about anti-gravity. It's impossible to put down!","You're American when you go into the bathroom, and you're American when you come out, but do you know what you are while you're in there? European.","Did you know the first French fries weren't actually cooked in France? They were cooked in Greece.","Want to hear a joke about a piece of paper? Never mind... it's tearable."," I just watched a documentary about beavers. It was the best dam show I ever saw!","Spring is here! I got so excited I wet my plants!","I bought some shoes from a drug dealer. I don't know what he laced them with, but I was tripping all day!","When a dad drives past a graveyard: Did you know that's a popular cemetery? Yep, people are just dying to get in there!","Why did the invisible man turn down the job offer? He couldn't see himself doing it.","I used to have a job at a calendar factory but I got the sack because I took a couple of days off.","How do you make holy water? You boil the hell out of it.","MOM: 'How do I look?' DAD: 'With your eyes.'","What did the horse say after it tripped? 'Help! I’ve fallen and I can’t giddyup!'","Did you hear about the circus fire? It was in tents!","Don't trust atoms. They make up everything!","What do you call a cow with two legs? Lean beef. If the cow has no legs, then it’s ground beef.","How many tickles does it take to make an octopus laugh? Ten-tickles.","I’m only familiar with 25 letters in the English language. I don’t know why.","What's the best part about living in Switzerland? I don't know, but the flag is a big plus.","What do prisoners use to call each other? Cell phones.","Why couldn't the bike standup by itself? It was two tired.","What do you call a dog that can do magic? A Labracadabrador.","The fattest knight at King Arthur’s round table was Sir Cumference. He acquired his size from too much pi."," Did you see they made round bails of hay illegal in Wisconsin? It’s because the cows weren’t getting a square meal.","SERVER: 'Sorry about your wait.' DAD: 'Are you saying I’m fat?'","You know what the loudest pet you can get is? A trumpet.","I was interrogated over the theft of a cheese toastie. Man, they really grilled me.","What do you get when you cross a snowman with a vampire? Frostbite.","What do you call a deer with no eyes? No idea!","Can February March? No, but April May!","Why can't you hear a pterodactyl go to the bathroom? Because the pee is silent."," What does a zombie vegetarian eat? 'GRRRAAAAAIIIINNNNS!'","Why wasn't the woman happy with the velcro she bought? It was a total ripoff.","What do you call someone with no body and no nose? Nobody knows.","You heard of that new band 1023MB? They're good but they haven't got a gig yet.","Why did the crab never share? Because he's shellfish."]
    chucknorris_current_response = random.choice(chucknorris_possible_responses)
    await bot.say(chucknorris_current_response)

#moderation
@bot.group(pass_context=True)

async def moderation(ctx):
    '''Shows a list of moderation commands.
    Usage: -moderation
    '''
    if ctx.invoked_subcommand is None:
	    embed=discord.Embed(description='Moderation commands\n\n-kick\n-kick <username mentioned>\nKick someone.\nNeeds permission kick_members.\n\n-ban\n-ban <mentioned username>\nBan someone.\nNeeds ban_members permission.\n\n-clear\n-clear <2 or over>\nClears the amount of messages you want to be cleared.\nNeeds permission manage_messages.\n\n-mute\n-mute <username mentioned>\nmute someone.\nNeeds permission manage_messages.\n\n-unmute\n-unmute <username mentioned>\nunmute someone.\nNeeds permission manage_messages.\n\n-unban\n-unban <mentioned username>\nUnban someone.\nNeeds ban_members permission.', color=0x2874A6)
	    await bot.say(embed=embed)

@bot.command(pass_context = True)

async def kick(ctx, *, member : discord.Member = None):
    '''Kick someone
    Usage: -kick <@person>
    Example: -kick @Pointless
    Permission: kick_members
    '''
    if not ctx.message.author.server_permissions.kick_members:
        embed=discord.Embed(description=':x: You don\'t have enough permissions for this: kick_members.', color=0xFF0000)
        await bot.delete_message(ctx.message)
        await bot.say(embed=embed)
        return
 
    if not member:
        await bot.delete_message(ctx.message)
        return await bot.say(ctx.message.author.mention + ", specify a user to kick!")
    try:
        await bot.kick(member)
        await bot.delete_message(ctx.message)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            embed = discord.Embed(description = ":x: The person you are trying to ban has high permissions.", color = 0xFF0000)
            await bot.delete_message(ctx.message)
            return await bot.say(embed = embed)
 
    embed = discord.Embed(description =f"**%s** has been kicked!"%member.name, color = 0xFF0000)
    await bot.delete_message(ctx.message)
    return await bot.say(embed = embed)

@bot.command(pass_context = True)

async def ban(ctx, *, member : discord.Member = None, reason:str=None):
	'''Ban someone.
	Usage: -ban <@person>
	Example: -ban @Pointless
    Permission: ban_members
	'''
	if not ctx.message.author.server_permissions.ban_members:
		embed=discord.Embed(description=':x: You don\'t have enough permissions for this: ban_members.', color=0xFF0000)
		await bot.say(embed=embed)
		await bot.delete_message(ctx.message)
		return
 
	if not member:
		await bot.delete_message(ctx.message)
		return await bot.say(ctx.message.author.mention + ", specify a user to ban!")
	try:
		await bot.ban(member)
		await bot.delete_message(ctx.message)
	except Exception as e:
		if 'Privilege is too low' in str(e):
			embed = discord.Embed(description = ":x: The person you are trying to ban has high permissions.", color = 0xFF0000)
			await bot.delete_message(ctx.message)
			return await bot.say(embed = embed)
 
	embed = discord.Embed(description = "**%s** has been banned!"%member.name, color = 0xFF0000)
	await bot.delete_message(ctx.message)
	return await bot.say(embed = embed)

@bot.command(pass_context = True, aliases=['uban'])
async def unban(ctx, *, member : discord.Member = None):
	'''Unban someone.
	Usage: -unban <@person>
	Example: -unban @Pointless
    Permission: ban_members
	'''
	if not ctx.message.author.server_permissions.ban_members:
		embed=discord.Embed(description=':x: You don\'t have enough permissions for this: ban_members.', color=0xFF0000)
		await bot.say(embed=embed)
		await bot.delete_message(ctx.message)
		return
 
	if not member:
		return await bot.say(ctx.message.author.mention + ", specify a user to unban!")
		await bot.delete_message(ctx.message)
	try:
		await bot.unban(member)
		await bot.delete_message(ctx.message)
	except Exception as e:
		if 'Privilege is too low' in str(e):
			embed = discord.Embed(description = ":x: The person you are trying to ban has high permissions.", color = 0xFF0000)
			await bot.delete_message(ctx.message)
			return await bot.say(embed = embed)
 
	embed = discord.Embed(description = "**%s** has been unbanned!"%member.name, color = 0xFF0000)
	await bot.delete_message(ctx.message)
	return await bot.say(embed = embed)

@bot.command(pass_context=True, aliases=['purge','prune'])  
async def clear(ctx, amount:int):
    '''Clear messages of over 2 or more.
    Usage: -clear <number>
    Example: -clear 15
    Permission: manage_messages
    '''
    if not ctx.message.author.server_permissions.manage_messages:
        embed=discord.Embed(description=':x: You don\'t have enough permissions for this: manage_messages.', color=0xFF0000)
        await bot.say(embed=embed)
        await bot.delete_message(ctx.message)
        return
    deleted = await bot.purge_from(ctx.message.channel, limit=amount)
    await asyncio.sleep(0.1)
    try:
        deleted_message = await bot.say("{}, I have deleted {} messages.".format(ctx.message.author.mention, len(deleted)))
        await asyncio.sleep(5)
        await bot.delete_message(deleted_message)
    except:
        pass

@bot.command(pass_context=True, no_pm=True)

async def mute(ctx, *, member : discord.Member, reason:str=None):
    '''Mute someone.
    Usage: -mute <@person>
    Example: -mute @Pointless
    Permission: manage_messages
    '''
    if not ctx.message.author.server_permissions.manage_messages:
        embed1 = discord.Embed(description = f"**{ctx.message.author}, I added the role %s to %s.**", color = 0xFF0000, set_footer = f'Command executed by: {ctx.message.author}')
        await bot.delete_message(ctx.message)
        return await bot.say(embed = embed1)
    else:  
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)
        await bot.delete_message(ctx.message)

    embed = discord.Embed(description = "**%s** has been muted!"%member.name, color = 0xFF0000)
    await bot.delete_message(ctx.message)
    return await bot.say(embed = embed)

@bot.command(pass_context=True, no_pm=True, aliases=['umute'])

async def unmute(ctx, *, member : discord.Member):
    '''Unmute someone.
    Usage: -unmute <@person>
    Example: -unmute @Pointless
    Permission: manage_messages
    '''
    if not ctx.message.author.server_permissions.manage_messages:
        embed1 = discord.Embed(description = f"**{ctx.message.author}, You do not have the manage_messages permission.**", color = 0xFF0000, set_footer = f'Command executed by: {ctx.message.author}')
        await bot.delete_message(ctx.message)
        return await bot.say(embed = embed1)
    else:
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)
        await bot.delete_message(ctx.message)

    embed = discord.Embed(description = "**%s** has been unmuted!"%member.mention, color = 0xFF0000)
    await bot.delete_message(ctx.message)
    return await bot.say(embed = embed)
@bot.command(pass_context = True, aliases=['sban'])

async def softban(ctx, *, member : discord.Member = None):
    '''Softban someone.
    Usage: -softban <@person>
    Example: -softban @Pointless
    Permission: ban_members
    '''
    if not ctx.message.author.server_permissions.ban_members:
        embed1 = discord.Embed(description = f"**{ctx.message.author}, You do not have the ban_members permission.**", color = 0xFF0000, set_footer = f'Command executed by: {ctx.message.author}')
        await bot.delete_message(ctx.message)
        return await bot.say(embed = embed1)
 
    if not member:
        embed2 = discord.Embed(description = f"**{ctx.message.author}, Specify a user to ban next time you use this command.**", color = 0xFF0000, set_footer = f'Command executed by: {ctx.message.author}')
        await bot.delete_message(ctx.message)
        return await bot.say(embed = embed2)
    try:
        await bot.ban(member)
        await bot.unban(member.server,member)
        await bot.delete_message(ctx.message)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            embed3 = discord.Embed(description = f"**{ctx.message.author}, The person you are trying to soft-ban has high permissions.**", color = 0xFF0000, set_footer = f'Command executed by: {ctx.message.author}')
            await bot.delete_message(ctx.message)
            return await bot.say(embed = embed3)
 
    embed3 = discord.Embed(description = "**%s** has been soft-banned!"%member.name, color = 0xFF0000)
    await bot.delete_message(ctx.message)
    return await bot.say(embed = embed3)
    
		
@bot.command(pass_context=True, no_pm=True)
async def removerole(ctx, user: discord.Member, *, role):
    '''Remove a role from someone.
    Usage: -removerole <@person> <role>
    Example: -removerole @Pointless Memer
    Permission: manage_roles
    '''
    if ctx.message.author.server_permissions.manage_roles:
        await bot.remove_roles(user, discord.utils.get(ctx.message.server.roles, name=role))
        embed1 = discord.Embed(description = f"**{ctx.message.author},**I removed the role {role} from {user.mention}.**", color = 0xFF0000, set_footer = f'Command executed by: {ctx.message.author}')
        return await bot.say(embed = embed1)
        await bot.delete_message(ctx.message)
    else:
        embed2 = discord.Embed(description = f"**{ctx.message.author}, You do not have the manage_roles permission.**", color = 0xFF0000, set_footer = f'Command executed by: {ctx.message.author}')
        return await bot.say(embed = embed2)

@bot.command(pass_context=True, no_pm=True)
async def addrole(ctx, user: discord.Member, *, role):
    '''Add a role to someone.
    Usage: -addrole <@person> <role>
    Example: -addrole @Pointless Memer
    Permission: manage_roles
    '''
    if ctx.message.author.server_permissions.manage_roles:
        await bot.add_roles(user, discord.utils.get(ctx.message.server.roles, name=role))
        embed1 = discord.Embed(description = f"**{ctx.message.author}, I added the role {role} to {user.mention}.**", color = 0xFF0000, set_footer = f'Command executed by: {ctx.message.author}')
        return await bot.say(embed = embed1)
        await bot.delete_message(ctx.message)
    else:
        embed2 = discord.Embed(description = f"**{ctx.message.author}, You do not have the manage_roles permission.**", color = 0xFF0000, set_footer = f'Command executed by: {ctx.message.author}')
        return await bot.say(embed = embed2)
        await bot.delete_message(ctx.message)
@bot.command(pass_context = True, no_pm = True)
async def announce(ctx, *, text: str):
    '''Announce something.
    Usage: -announce <text>
    Example: -announce I like potatoes!
    Permission: Administrator
    '''
    if not ctx.message.author.server_permissions.administrator:
        embed1 = discord.Embed(description = f"**{ctx.message.author}, You do not have the administrator permission.**", color = 0xFF0000, footer = f'Command executed by: {ctx.message.author}')
        return await bot.say(embed = embed1)
    else:
        embed=discord.Embed(title = "__Announcement__", description=text, color = 0xFF0000, footer = f'Announcement by: {ctx.message.author}.')
        await bot.delete_message(ctx.message)
        await bot.say(embed = embed)


#server
@bot.group(pass_context=True)

async def server(ctx):
	'''Shows a list of server commands.
	Usage: -server
	Example: -server
	'''
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Server commands\n\n-serverinfo\nCheck the info about the server.\n\n-bans\nLists the banned people on the server.\n\n-userinfo\nCheck info about you or other users.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(pass_context = True)

async def serverinfo(ctx):
    '''Shows information about the server.
    Usage: -serverinfo
    '''
    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #if theres too much roles
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];

    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', colour = 0xFFFF);
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id, inline=True);
    join.add_field(name = '__ID__', value = str(server.id), inline=True)
    join.add_field(name = '__Member Count__', value = str(server.member_count), inline=True);
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz), inline=True);
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles, inline=True);
    join.add_field(name = '__Region__', value = str(server.region), inline=True)
    join.add_field(name = '__AFK Timeout__', value = str(server.afk_timeout), inline=True)
    join.add_field(name = '__AFK Channel__', value = str(server.afk_channel), inline=True)
    join.add_field(name = '__Verification Level__', value = str(server.verification_level), inline=True)
    join.add_field(name = '__Custom Emotes__', value=len(server.emojis), inline=True)
    join.add_field(name = '__Channels__', value=len(server.channels), inline=True)
    join.add_field(name = '__Features:__', value=ctx.message.server.features, inline=True)
    join.set_footer(text ='Created at: %s'%time);

    return await bot.say(embed = join);

@bot.command(pass_context = True, aliases=['banlist'])

async def bans(ctx):
    '''Shows a list of bans.
    Usage: -bans
    '''
    x = await bot.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    xc = len(x)
    if xc == 0:
        x = 'No one is banned.'
    embed = discord.Embed(title = "List of banned people:", description = x, color = 0xFFFFF)
    return await bot.say(embed = embed)

@bot.command(pass_context=True)

async def userinfo(ctx, user: discord.Member = None):
    '''Shows information about a user.
    Usage: -userinfo <@person>
    Example: -userinfo @Pointless
    '''
    member = discord.User
    if not user:
          user = ctx.message.author
    join = discord.Embed(description= '%s '%(str(user)),title = '__Full Name__', colour = 0xFFFF);
    join.set_thumbnail(url = user.avatar_url);
    join.add_field(name = '__Name__', value = str(user.name),inline=True);
    join.add_field(name = '__ID__', value = str(user.id),inline=True);
    join.add_field(name = '__Nickname__', value = str(user.nick),inline=True);
    join.add_field(name = '__Account Created At__', value = str(user.created_at),inline=True);
    join.add_field(name = '__Joined Server At__', value = str(user.joined_at),inline=True);
    join.add_field(name = '__Game__', value = str(user.game),inline=True);
    join.add_field(name = '__Roles__', value = str("%s") % ", ".join([role.name for role in user.roles if role.name != "@everyone"]),inline=True);
    join.add_field(name = '__Avatar URL__', value = str(user.avatar_url),inline=True);
    join.add_field(name = '__Status__', value = str(user.status),inline=True);
    join.add_field(name = '__Highest Role__', value = str(user.top_role),inline=True);
    return await bot.say(embed = join);

#utilities
@bot.group(pass_context=True)

async def utilities(ctx):
	'''Shows a list of utility commands.
	Usage: -utilities
	'''
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Utility commands\n\n\n-avatar\nGet the avatar link of a user.\n\n-poll\nCreate a poll with the thumbs up, shrug and thumbs down reaction.\n\n-embed\nEmbed a message so CommuniBot can say what you wanted.\n\n-translate\nTranslate from one language to another. Supported list of languages: https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/#languages \n\n-urbandict\nSearch definitions in the Urban Dictionary.\n\n-math +\nShows a list of mathematic commands.\n\n-conversion +\nShows a list of conversion commands.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True)

async def avatar(ctx, member : discord.Member = None):
    '''Get the avatar of a member.
    Usage: -avatar <@person>
    Example: -avatar @Pointless
    '''
    channel = ctx.message.channel
    if member is None:
        member = ctx.message.author
    await bot.say(member.avatar_url)

@bot.command(pass_context=True)

async def poll(ctx,*, message: str):
    '''Creates a poll.
    Usage: -poll <text>
    Example: -poll Do you like CommuniBot?
    '''
    
    embed = discord.Embed(color = ctx.message.author.color, timestamp = datetime.utcnow())
    embed.set_author(name = "Poll", icon_url = ctx.message.author.avatar_url)
    embed.description = (message)
    embed.set_footer(text = ctx.message.author.name)
    x = await bot.say(embed = embed)
    await bot.add_reaction(x, "👍")
    await bot.add_reaction(x, "🤷")
    await bot.add_reaction(x, "👎")

@bot.command(pass_context=True, aliases=['tr'])

async def translate(ctx, tl, *words: str):
    '''Translate something. Supported list of languages: https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/#languages
    Usage: translate <from>-<to>
    Example: translate en-pl sandwich
    '''
    words = ' '.join(words)
    answer = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20170315T092303Z.ece41a1716ebea56.a289d8de3dc45f8ed21e3be5b2ab96e378f684fa&text={0}&lang={1}".format(words,tl)).json()
    await bot.say("{0} {1}".format(ctx.message.author.mention, str(answer["text"])[2:-2]))

@bot.command(pass_context=True, aliases=['urbandictionary','urbandict','udict','udictionary','udefine','urbandefine'])

async def urban(ctx,*msg):
    word = ' '.join(msg)
    api = "http://api.urbandictionary.com/v0/define"
    response = requests.get(api, params=[("term", word)]).json()
    
    if len(response["list"]) == 0: return await client.say("Could not find that word!")
    
    embed = discord.Embed(title = ":mag: Search Word", description = word, color = 0xFFF00)
    embed.add_field(name = "Top definition:", value = response['list'][0]['definition'])
    embed.add_field(name = "Examples:", value = response['list'][0]["example"])
    embed.set_footer(text = "Tags: " + ', '.join(response['tags']))

    await bot.say(embed = embed)

@bot.command(name='_-', pass_context=True)
async def _correction(ctx):
    '''-_- Correction.
    '''
    return


@bot.group(pass_context=True, aliases=['maths','mathematics','mathematic','calculation'])

async def math(ctx):
	'''Shows a list of math commands.
	Usage: -math
	'''
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Math commands\n\n\n-add\nAdd two numbers together.\n\n-subtract\nSubtract two numbers.\n\n-multiply\nMultiply two numbers together.\n\n-divide\nDivide two numbers together\n\n-modulo\nFind the remainder of a number when divided together.\n\n-exponent\nFind a number to the power of another number.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(pass_context=True, aliases=['addition'])

async def add(ctx, number1: int, number2: int):
    '''Add two numbers together.
    Usage: -add <a> <b>
    Example: -add 2 2
    '''
    await bot.say(number1 + number2)

@bot.command(pass_context=True, aliases=['subtraction','minus'])

async def subtract(ctx, number1: int, number2: int):
    '''Subtract two numbers.
    Usage: -subtract <a> <b>
    Example: -subtract 4 2
    '''
    await bot.say(number1 - number2)

@bot.command(pass_context=True, aliases=['times','multiplication'])

async def multiply(ctx, number1: int, number2: int):
    '''Multiply two numbers together.
    Usage: -multiply <a> <b>
    Example: -multiply 2 2
    '''
    await bot.say(number1 * number2)

@bot.command(pass_context=True, aliases=['division','share'])

async def divide(ctx, number1: int, number2: int):
    '''Divide two numbers.
    Usage: -divide <a> <b>
    Example: -divide 10 5
    '''
    await bot.say(number1 / number2)

@bot.command(pass_context=True, aliases=['remainder','modulus'])

async def modulo(ctx, number1: int, number2: int):
    '''Find the remainder of when you divide two numbers together.
    Usage: -modulo <a> <b>
    Example: -modulo 7 3
    '''
    await bot.say(number1 % number2)

@bot.command(pass_context=True, aliases=['power'])

async def exponent(ctx, number1: int, number2: int):
    '''Find the power of a number how many times you like.
    Usage: -exponent <a> <b>
    Example: -exponent 4 2
    '''
    await bot.say(number1 ** number2)

@bot.group(pass_context=True, aliases=['convert'])

async def conversion(ctx):
	'''Shows a list of commands that converts from one unit of whatever to another.
	Usage: -conversion
	'''
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Conversion commands\n\n\n-temperature +\nShows a list of temperature conversion commands.', color=0x2874A6)
		await bot.say(embed=embed)
    
@bot.group(pass_context=True)

async def temperature(ctx):
	'''Shows a list of temperature conversion commands.
	Usage: -temperature
	'''
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Temperature Conversion commands\n\n\n-centigrade +\nShows a list of centigrade commands.\n\n-kelvin +\nShows a list of Kelvin commands.\n\n-fahrenheit +\nShows a list of Fahrenheit commands.\n\n-rankine +\nShows a list of Rankine commands.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.group(pass_context=True)

async def centigrade(ctx):
	'''Shows a list of centigrade conversion commands.
	Usage: -centigrade
	'''
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Centigrade Conversion commands\n\n\n-centigrade-fahrenheit\nConverts Centigrade to Fahrenheit.\n\n-centigrade-kelvin\nConverts Centigrade to Kelvin.\n\n-centigrade-rankine\nConverts Centigrade to Rankine.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.group(pass_context=True)

async def kelvin(ctx):
	'''Shows a list of Kelvin conversion commands.
	Usage: -kelvin
	'''
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Kelvin Conversion commands\n\n\n-kelvin-fahrenheit\nConverts Kelvin to Fahrenheit.\n\n-kelvin-centigrade\nConverts Kelvin to Centigrade.\n\n-kelvin-rankine\nConverts Kelvin to Rankine.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.group(pass_context=True)

async def fahrenheit(ctx):
	'''Shows a list of Fahrenheit conversion commands.
	Usage: -fahrenheit
	'''
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Fahrenheit Conversion commands\n\n\n-fahrenheit-centigrade\nConverts Fahrenheit to Centigrade.\n\n-fahrenheit-kelvin\nConverts Fahrenheit to Kelvin.\n\n-fahrenheit-rankine\nConverts Fahrenheit to Rankine.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.group(pass_context=True)

async def rankine(ctx):
	'''Shows a list of Rankine conversion commands.
	Usage: -rankine
	'''
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Rankine Conversion commands\n\n\n-rankine-fahrenheit\nConverts Rankine to Fahrenheit.\n\n-rankine-kelvin\nConverts Rankine to Kelvin.\n\n-rankine-centigrade\nConverts Rankine to Centigrade..', color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(name='centigrade-fahrenheit',pass_context=True)

async def centigrade_fahrenheit(ctx, number: int):
    '''Convert Centigrade to Fahrenheit
    Usage: -centigrade-fahrenheit <number>
    Example: -centigrade-fahrenheit 10
    '''
    await bot.say(str((number * 1.8) + 32) + '°F')

@bot.command(name='centigrade-kelvin',pass_context=True)

async def centigrade_kelvin(ctx, number: int):
    '''Convert Centigrade to Kelvin
    Usage: -centigrade-kelvin <number>
    Example: -centigrade-kelvin 10
    '''
    await bot.say(str(number + 273.15) + '°K')

@bot.command(name='centigrade-rankine',pass_context=True)

async def centigrade_rankine(ctx, number: int):
    '''Convert Centigrade to Rankine
    Usage: -centigrade-rankine <number>
    Example: -centigrade-rankine 10
    '''
    await bot.say(str((number + 273.15) * (9/5)) + '°R')

@bot.command(name='fahrenheit-centigrade',pass_context=True)

async def fahrenheit_centigrade(ctx, number: int):
    '''Convert Fahrenheit to Centigrade
    Usage: -fahrenheit-centigrade <number>
    Example: -fahrenheit-centigrade 10
    '''
    await bot.say(str((number - 32) / 1.8) + '°C')

@bot.command(name='fahrenheit-kelvin',pass_context=True)

async def fahrenheit_kelvin(ctx, number: int):
    '''Convert Fahrenheit to Kelvin
    Usage: -fahrenheit-kelvin <number>
    Example: -fahrenheit-kelvin 10
    '''
    await bot.say(str((number - 32) / 1.8) + '°K')

@bot.command(name='fahrenheit-rankine',pass_context=True)

async def fahrenheit_rankine(ctx, number: int):
    '''Convert Fahrenheit to Rankine
    Usage: -fahrenheit-rankine <number>
    Example: -fahrenheit-rankine 10
    '''
    await bot.say(str(number + 459.67) + '°R')

@bot.command(name='kelvin-fahrenheit',pass_context=True)

async def kelvin_fahrenheit(ctx, number: int):
    '''Convert Kelvin to Fahrenheit
    Usage: -kelvin-fahrenheit <number>
    Example: -kelvin-fahrenheit 10
    '''
    await bot.say(str((number * (9/5)) - 459.67) + '°F')

@bot.command(name='kelvin-centigrade',pass_context=True)

async def kelvin_centigrade(ctx, number: int):
    '''Convert Kelvin to Centigrade
    Usage: -kelvin-Centigrade <number>
    Example: -kelvin-Centigrade 10
    '''
    await bot.say(str(number - 273.15 ) + '°C')

@bot.command(name='kelvin-rankine',pass_context=True)

async def kelvin_rankine(ctx, number: int):
    '''Convert Kelvin to Rankine
    Usage: -kelvin-rankine <number>
    Example: -kelvin-rankine 10
    '''
    await bot.say(str(number * (9/5)) + '°R')

@bot.command(name='rankine-fahrenheit',pass_context=True)

async def rankine_fahrenheit(ctx, number: int):
    '''Convert Rankine to Fahrenheit
    Usage: -rankine-fahreneheit <number>
    Example: -rankine-fahrenheit 10
    '''
    await bot.say(str(number - 459.67) + '°F')

@bot.command(name='rankine-centigrade',pass_context=True)

async def rankine_centigrade(ctx, number: int):
    '''Convert Rankine to Centigrade
    Usage: -rankine-centigrade <number>
    Example: -rankine-centigrade 10
    '''
    await bot.say(str((number - 491.67) * (5/9)) + '°C')

@bot.command(name='rankine-kelvin',pass_context=True)

async def rankine_kelvin(ctx, number: int):
    '''Convert Rankine to Kelvin
    Usage: -rankine-kelvin <number>
    Example: -rankine-kelvin 10
    '''
    await bot.say(str(number * (5/9)) + '°K')

#token
bot.run(Secrets['Token'])