#imports

import discord
from random import shuffle
import configparser
import random
import aiohttp
import traceback
import sys
import re
import json
import time
import asyncio
import os
import datetime
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

#commands
#ping
@bot.command(pass_context=True)
async def ping(ctx):
	channel = ctx.message.channel
	t1 = time.perf_counter()
	await bot.send_typing(channel)
	t2 = time.perf_counter()
	embed=discord.Embed(description='Pong! {} milliseconds.'.format(round((t2-t1)*1000)), color=0x2874A6)
	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def prefixes(ctx):
	embed=discord.Embed(description='My prefix are: -, :,@CommuniBot, CommuniBot, @CommuniBot#4412, CommuniBot#4412 and communibot.',color=0x2874A6)
	await bot.say(embed=embed)

#help
@bot.command(pass_context=True)
async def help(ctx):
	embed=discord.Embed(description='Help\nPrefixes: -prefixes\n-ping - Shows the amount of milliseconds taken to respond.\n-info - Shows information about CommuniBot!\n-uptime - Shows the uptime status of CommuniBot!\n\n\n-jokes + \nShows a list of joke commands.\n\n-actions + \nShows a list of action commands.\n\n-memes +\nShows a list of meme commands.\n\n-moderation +\nShows a list of moderation commands.\n\n-fun +\nShows a list of fun commands.\n\n-server +\nLists commands about the server.\n\n-utilities +\nShows a list of commands about utilities.', color=0x2874A6)
	await bot.say(embed=embed)

@bot.group(pass_context=True)
async def fun(ctx):
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Fun commands\n\n\n-coinflip\nThe bot chooses between heads or tails.\n\n-8ball\nUse the magic 8ball!\n\n-comic\nShows a random comic.\n\n-cat\nShows a random cat picture.\n\n-dog\nShows a random dog picture.\n\n-say\nSay anything after the command and it will repeat it back.\n\n-choose\nMake CommuniBot choose over three or more things.\n\n-roll\nRoll any number above one.', color=0x2874A6)
		await bot.say(embed=embed)
@bot.command(pass_context=True)
async def coinflip(ctx):
    choice = random.choice(['Heads!','Tails!'])
    await bot.say(choice)
@bot.command(name="8ball", pass_context=True, aliases=['eightball'])
async def _8ball(self, *, question : str):
    responses = [["Signs point to yes.", "Yes.", "Without a doubt.", "As I see it, yes.", "You may rely on it.", "It is decidedly so.", "Yes - definitely.", "It is certain.", "Most likely.", "Outlook good."],
    ["Reply hazy, try again.", "Concentrate and ask again.", "Better not tell you now.", "Cannot predict now.", "Ask again later."],
    ["My sources say no.", "Outlook not so good.", "Very doubtful.", "My reply is no.", "Don't count on it."]]
    if "?" in question:
        await self.bot.say(":8ball:" + random.choice(random.choice(responses)))
    else:
        await self.bot.say("That doesn't look like a question.")

@bot.command(pass_context=True, no_pm=True)
async def comic(ctx):
        api = "https://xkcd.com/{}/info.0.json".format(random.randint(1, 1800))
        async with aiohttp.ClientSession() as session:
            async with session.get(api) as r:
                response = await r.json()
                embed = discord.Embed(title="Comic", description=response["title"], color=0xFF0000)
                embed.set_image(url=response["img"])
                await bot.say(embed=embed)

@bot.command(pass_context=True)
async def cat(ctx):
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

@bot.command(pass_context=True)
async def say(ctx, *, message: str):
    await bot.say(message)

@bot.command(name='choose', aliases=['select','choice'],pass_context=True)
async def _choose(self, ctx, *args):
    """Make CommuniBot choose between three or more things."""
    choice = random.choice(args)
    await bot.say(f'**`{choice}`**')

@bot.command(pass_context=True)
async def roll(ctx, number: int=100):
    """Rolls random number (between 1 and user choice)
    Defaults to 100."""
    if number > 1:
        await bot.say(f"{ctx.message.author.mention} | :game_die: {randint(1, number)}")
    else:
        await bot.say(f"{ctx.message.author.mention} Please insert a number higher than one.")


#info
@bot.command(pass_context=True, aliases=['botinfo'])
async def info(ctx):
    member = ctx.message.author
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)

    join = discord.Embed(description= '',title = 'Information about CommuniBot', colour = 0xFFFF);
    join.add_field(name = '__Information__', value = f"This bot was made in discord.py and was created by <@276043503514025984> (Pointless). It is for a bot that has moderation, fun commands, memes and more. It aims to make communities get less bots in total, so it doesn't look like there's too much bots in the Member list.", inline=True);
    join.add_field(name = '__Creator__', value = f"<@276043503514025984> - Created the the bot and all the commands, except for the ones who created some.", inline=True);
    join.add_field(name = '__Helped__', value = f"<@338600456383234058> - Created -say, -poll and -embed command.", inline=True)
    join.add_field(name = '__Bot Invite Link__', value = f"Invite link for the bot: https://discordapp.com/oauth2/authorize?client_id=406890237604790302&scope=bot&permissions=2146958591", inline=True)
    join.add_field(name = '__Support Server Invite Link__', value = f"Invite link for the support server: https://discord.gg/Fz2pKVE", inline=True)
    join.add_field(name = '__Discord Bots Link__', value = f"Link for Discord Bots: https://discordbots.org/bot/406890237604790302", inline=True)
    join.add_field(name = '__Github Link__', value = f"Link for Github page: https://github.com/P01nt-Less/CommuniBot", inline=True)
    join.add_field(name = '__Uptime Status__', value = f"I've been online for %d week(s), %d day(s), %d hour(s), %d minute(s), %d second(s)!" % (week, day, hour, minute, second), inline=True)
    return await bot.say(embed = join);
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def uptime():
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    await bot.say("I've been online for %d week(s), %d day(s), %d hour(s), %d minute(s), %d second(s)!" % (week, day, hour, minute, second))


#actions
@bot.group(pass_context=True)
async def actions(ctx):
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Action commands\n\n\n-punch\nPunches someone you\'d like to do that to.\n\n-legkick\nKicks anyone you like.\n\n-hug\nHugs anyone you like.\n\n-kiss\nKiss anyone you like.\n\n-uppercut\nUppercut anybody you like.\n\n-wave\nWave at anyone you\'d like to.\n\n-smile\nJust smile.\n\n-frown\nFrown. :(\n\n-slap\nSlap anyone you like.\n\n-stab\nStab people! Muehehehe!\n\n-murder\nMurder someone...\n\n-shoot\nShoot a person! Dun dun dunn!!\n\n-heil\nHeil someone!', color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(pass_context=True)
async def punch(ctx, person: discord.Member): 
    punch_possible_responses = ["{} punched {} in the face, in the face."]
    punch_current_response = random.choice(punch_possible_responses)
    await bot.say(punch_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)
async def legkick(ctx, person: discord.Member):
    kick_possible_responses = ["{} kicked {} in the leg."]
    kick_current_response = random.choice(kick_possible_responses)
    await bot.say(kick_current_response.format(ctx.message.author.mention, person.mention))	
@bot.command(pass_context=True)
async def hug(ctx, person: discord.Member):
    hug_possible_responses = ["{} hugged {} tightly."]
    hug_current_response = random.choice(hug_possible_responses)
    await bot.say(hug_current_response.format(ctx.message.author.mention, person.mention))	
@bot.command(pass_context=True)
async def kiss(ctx, person: discord.Member):
    kiss_possible_responses = ["{} kissed {} on the cheek."]
    kiss_current_response = random.choice(kiss_possible_responses)
    await bot.say(kiss_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)
async def uppercut(ctx, person: discord.Member):
    uppercut_possible_responses = ["{} uppercut {} and turned {} into a giraffe."]
    uppercut_current_response = random.choice(uppercut_possible_responses)
    await bot.say(uppercut_current_response.format(ctx.message.author.mention, person.mention, person.mention))
@bot.command(pass_context=True)
async def wave(ctx, person: discord.Member):
    uppercut_possible_responses = ["{} waved at {} with a smile on their face."]
    uppercut_current_response = random.choice(uppercut_possible_responses)
    await bot.say(uppercut_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)
async def smile(ctx):
    smile_possible_responses = ["{} smiled."]
    smile_current_response = random.choice(smile_possible_responses)
    await bot.say(smile_current_response.format(ctx.message.author.mention))
@bot.command(pass_context=True)
async def frown(ctx):
    punch_possible_responses = ["{} frowned."]
    punch_current_response = random.choice(punch_possible_responses)
    await bot.say(punch_current_response.format(ctx.message.author.mention))
@bot.command(pass_context=True)
async def slap(ctx, person: discord.Member):
    slap_possible_responses = ["{} slapped {}'s face making it red. "]
    slap_current_response = random.choice(slap_possible_responses)
    await bot.say(slap_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)
async def stab(ctx, person: discord.Member):
    slap_possible_responses = ["{} stabbed {} in the heart making his last feeling pain."]
    slap_current_response = random.choice(slap_possible_responses)
    await bot.say(slap_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)
async def murder(ctx, person: discord.Member):
    slap_possible_responses = ["{} murdered {} with no one knowing anything that happened."]
    slap_current_response = random.choice(slap_possible_responses)
    await bot.say(slap_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)
async def shoot(ctx, person: discord.Member):
    slap_possible_responses = ["{} shot {} straight in the head making them collapse onto the floor."]
    slap_current_response = random.choice(slap_possible_responses)
    await bot.say(slap_current_response.format(ctx.message.author.mention, person.mention))
@bot.command(pass_context=True)
async def heil(ctx, person: discord.Member):
    slap_possible_responses = ["{} heiled {}. HEIL {}!"]
    slap_current_response = random.choice(slap_possible_responses)
    await bot.say(slap_current_response.format(ctx.message.author.mention, person.mention, person.mention))

#jokes
@bot.group(pass_context=True)
async def jokes(ctx):
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Joke commands\n\n\n-insovietrussia\nThis command randomizes between lots of "In Soviet Russia" jokes.\n\n-chucknorris\nRandomizes between lots of Chuck Norris jokes/facts.\n\n-dadjoke\nRandomizes between lots of really not funny bad Dad jokes!',color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(pass_context=True)
async def insovietrussia(ctx):
	insovietrussia_possible_responses = ["In America, you drive a car. In Soviet Russia, a car drives you!",  "In America the president gets assassinated. In soviet Russia, the president assassinates you!", "In America, you throw a grenade! In Soviet Russia, a grenade throws you!", "In America, you eat food. In Soviet Russia, food eats you!", "In America, you write 'R'. In Soviet Russia, you write 'Я'!", "In America, you break the law. In Soviet Russia, the law breaks you!", "Roses are red, Violets are blue, In Soviet Russia, a poem writes you!", "In America, the Grinch steals Christmas. In Soviet Russia, Christmas steals the Grinch!", "In America, you laugh at jokes. In Soviet Russia, jokes laugh at you!", "In America, Jesus sacrifices for you. In Soviet Russia, you sacrifice for Jesus!", "In America, Russians spy on you. In Soviet Russia, you spy on Russians!", "In America, you find Waldo. In Soviet Russia, Waldo finds you!", "In America, you call the police. In Soviet Russia, police calls you!", "In America, you watch TV. In Soviet Russia, the TV watches you!", "In America, you eat a cookie. But in Soviet Russia, the cookie eats you!", "In America, you play games. In Soviet Russia, games play you!"]
	insovietrussia_current_response = random.choice(insovietrussia_possible_responses)
	await bot.say(insovietrussia_current_response)
@bot.command(pass_context=True)
async def chucknorris(ctx):
    chucknorris_possible_responses = ["Chuck Norris threw a grenade and killed 50 people, then it exploded.", "Chuck Norris can kill two stones with one bird.", "Chuck Norris can pick oranges from an apple tree and make the best lemonade you've ever tasted.", "Once a cobra bit Chuck Norris' leg. After five days of excruciating pain, the cobra died.", "When a zombie apocalypse starts, Chuck Norris doesn't try to survive. The zombies do.", "Chuck Norris can hear sign language.", "Chuck Norris beat the sun in a staring contest.","It is considered a great accomplishment to go down Niagara Falls in a wooden barrel. Chuck Norris can go up Niagara Falls in a cardboard box.", "Chuck Norris was once on Celebrity Wheel of Fortune and was the first to spin. The next 29 minutes of the show consisted of everyone standing around awkwardly, waiting for the wheel to stop.", "Giraffes were created when Chuck Norris uppercut a horse.", "When the Bogeyman goes to sleep every night he checks his closet for Chuck Norris.", "When Chuck Norris was in middle school, his English teacher assigned an essay: \'What is courage?\' He received an A+ for turning in a blank page with only his name at the top.", "Chuck Norris will never have a heart attack... even a heart isn't foolish enough to attack Chuck Norris.", "Chuck Norris can kill your imaginary friends.", "Chuck can set ants on fire with a magnifying glass. At night.", "Chuck Norris once went to mars. Thats why there are no signs of life.", "When Bruce Banner gets mad he turns into the Hulk. When the Hulk gets mad he turns into Chuck Norris. When Chuck Norris gets mad, run.", "Chuck Norris is the reason Waldo is hiding.", "Chuck Norris is the only person that can punch a cyclops between the eye.", "When Chuck Norris enters a room, he doesn't turn the lights on, he turns the dark off.", "M.C. Hammer learned the hard way that Chuck Norris can touch this.", "Chuck Norris can build a snowman out of rain.", "Chuck Norris was once charged with three attempted murders in Boulder County, but the Judge quickly dropped the charges because Chuck Norris does not \'attempt\' murder.", "Leading hand sanitizers claim they can kill 99.9 percent of germs. Chuck Norris can kill 100 percent of whatever the hell he wants.", "Chuck Norris's computer has no \'backspace\' button, Chuck Norris doesn't make mistakes.", "Chuck Norris makes onions cry.", "Chuck Norris tells Simon what to do.", "Chuck Norris plays Russian roulette with a fully loaded revolver... and wins."]
    chucknorris_current_response = random.choice(chucknorris_possible_responses)
    await bot.say(chucknorris_current_response)
@bot.command(pass_context=True)
async def dadjoke(ctx):
    chucknorris_possible_responses = ["What time did the man go to the dentist? Tooth hurt-y.","A ham sandwich walks into a bar and orders a beer. \nBartender says, 'Sorry we don't serve food here.'","Whenever the cashier at the grocery store asks my dad if he would like the milk in a bag he replies, 'No, just leave it in the carton!'","Me: 'Dad, make me a sandwich!' \nDad: 'Poof, You’re a sandwich!'","How do you make a Kleenex dance? Put a little boogie in it!","Two peanuts were walking down the street. One was a salted.","We were getting fast food when the lady at the window said, 'Any condiments?' My dad responded, 'Compliments? You look very nice today!'","My dad’s name is Phil, and whenever I finish eating and say, 'Dad, I’m full,' he always replies, 'No, I’m full; you're Ruby.'","I'm reading a book about anti-gravity. It's impossible to put down!","You're American when you go into the bathroom, and you're American when you come out, but do you know what you are while you're in there? European.","Did you know the first French fries weren't actually cooked in France? They were cooked in Greece.","Want to hear a joke about a piece of paper? Never mind... it's tearable."," I just watched a documentary about beavers. It was the best dam show I ever saw!","Spring is here! I got so excited I wet my plants!","I bought some shoes from a drug dealer. I don't know what he laced them with, but I was tripping all day!","When a dad drives past a graveyard: Did you know that's a popular cemetery? Yep, people are just dying to get in there!","Why did the invisible man turn down the job offer? He couldn't see himself doing it.","I used to have a job at a calendar factory but I got the sack because I took a couple of days off.","How do you make holy water? You boil the hell out of it.","MOM: 'How do I look?' DAD: 'With your eyes.'","What did the horse say after it tripped? 'Help! I’ve fallen and I can’t giddyup!'","Did you hear about the circus fire? It was in tents!","Don't trust atoms. They make up everything!","What do you call a cow with two legs? Lean beef. If the cow has no legs, then it’s ground beef.","How many tickles does it take to make an octopus laugh? Ten-tickles.","I’m only familiar with 25 letters in the English language. I don’t know why.","What's the best part about living in Switzerland? I don't know, but the flag is a big plus.","What do prisoners use to call each other? Cell phones.","Why couldn't the bike standup by itself? It was two tired.","What do you call a dog that can do magic? A Labracadabrador.","The fattest knight at King Arthur’s round table was Sir Cumference. He acquired his size from too much pi."," Did you see they made round bails of hay illegal in Wisconsin? It’s because the cows weren’t getting a square meal.","SERVER: 'Sorry about your wait.' DAD: 'Are you saying I’m fat?'","You know what the loudest pet you can get is? A trumpet.","I was interrogated over the theft of a cheese toastie. Man, they really grilled me.","What do you get when you cross a snowman with a vampire? Frostbite.","What do you call a deer with no eyes? No idea!","Can February March? No, but April May!","Why can't you hear a pterodactyl go to the bathroom? Because the pee is silent."," What does a zombie vegetarian eat? 'GRRRAAAAAIIIINNNNS!'","Why wasn't the woman happy with the velcro she bought? It was a total ripoff.","What do you call someone with no body and no nose? Nobody knows.","You heard of that new band 1023MB? They're good but they haven't got a gig yet.","Why did the crab never share? Because he's shellfish."]
    chucknorris_current_response = random.choice(chucknorris_possible_responses)
    await bot.say(chucknorris_current_response)

#memes
@bot.group(pass_context=True)
async def memes(ctx):
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Meme commands\n\n\n-lolcat\nSHOWS PICTUREZ OV LOLCATS!!\n\n-saltbae\nShows pictures of the salt bae meme.\n\n-loldog\nSHOWS PICTUREZ OV LOLDOGS!!', color=0x2874A6)
		await bot.say(embed=embed)
@bot.command(pass_context=True)
async def lolcat(ctx):
    lolcat_possible_responses = ['{} https://upload.wikimedia.org/wikipedia/commons/a/ab/Lolcat_in_folder.jpg','{} https://upload.wikimedia.org/wikipedia/commons/1/1a/Cat_crying_%28Lolcat%29.jpg','{} http://i0.kym-cdn.com/photos/images/original/001/284/242/202.jpg','{} https://i.ytimg.com/vi/6HA2D3LsJQs/hqdefault.jpg','{} http://www.lolcats.com/images/u/11/43/lolcatsdotcomsyucc7vghgeu3ygu.jpg','{} https://shesaid.com/wp-content/uploads/2016/09/7Ak9p.jpg','{} https://i.ytimg.com/vi/Bkco3bE2tg8/hqdefault.jpg','{} https://vignette.wikia.nocookie.net/epicrapbattlesofhistory/images/1/15/LOLCATS-Cloud.jpeg/revision/latest?cb=20140723224315','{} https://i.chzbgr.com/full/9089826560/h07C1DAA9/','{} https://media.mnn.com/assets/images/2012/11/lolcat_main_0.jpg','{} https://i.pinimg.com/736x/aa/3c/0f/aa3c0f3dd59210f9953a5c1c0d46c2d6--funny-pets-funny-animals.jpg','{} https://img.scoop.it/NhznTvgS8CGETQOQgXJ3DDl72eJkfbmt4t8yenImKBVvK0kTmF0xjctABnaLJIm9','{} https://www.oddee.com/wp-content/uploads/_media/imgs/articles2/a97873_rsz_drunkdial.jpg','{} https://i.chzbgr.com/full/9107324928/h0A65249F/','{} https://i.ytimg.com/vi/IaK6EUSUG4I/hqdefault.jpg','{} https://blogs.loc.gov/digitalpreservation/files/2014/07/864385794_40eef8f22b_z1.jpg','{} https://i.chzbgr.com/full/9101861888/h2C7008DC/','{} http://i0.kym-cdn.com/photos/images/facebook/001/031/948/10b.jpg','{} http://i0.kym-cdn.com/photos/images/facebook/000/559/061/d94.png','{} https://pics.me.me/my-cat-made-this-face-when-i-meowed-back-at-8561541.png','{} http://www.lolcats.com/images/u/12/43/lolcatsdotcomnapkin.jpg','{} https://longlivethekitty.com/wp-content/uploads/lolcat_airplane.jpg','{} http://www.lolcats.com/images/u/08/39/lolcatsdotcomly2r5yakozqlbhmn.jpg','{} http://firstmonday.org/ojs/index.php/fm/article/viewFile/5391/4103/40381','{} https://bighugelabs.com/img/lolcat-sample.jpg','{} http://static.wixstatic.com/media/8e31f964a29559e19acfb44ea027ab0c.wix_mp_1024','{} http://www.rationalitynow.com/blog/wp-content/uploads/2009/12/owlcatl.jpg','{} http://i0.kym-cdn.com/photos/images/facebook/000/519/843/833.jpg']
    lolcat_current_response = random.choice(lolcat_possible_responses)
    await bot.say(lolcat_current_response.format(ctx.message.author.mention))
@bot.command(pass_context=True)
async def saltbae(ctx):
	saltbae_possible_responses = ['{} http://runt-of-the-web.com/wordpress/wp-content/uploads/2017/01/wrong-answer-you-aint-cheat.jpg','{} http://i.imgur.com/yYT55QA.jpg','{} http://i0.kym-cdn.com/photos/images/original/001/209/914/6b4.jpg','{} http://i0.kym-cdn.com/photos/images/original/001/209/916/fe7.jpg','{} https://i.imgur.com/XuFg46x.jpg','{} https://i.imgur.com/vlA7u5k.jpg','{} https://stepcdn.com/assets/2017-02/03/11/8e3r2/trump-twitter-700x.jpg','{} http://runt-of-the-web.com/wordpress/wp-content/uploads/2017/01/adding-salt-to-your-drama.jpg','{} http://i0.kym-cdn.com/photos/images/original/001/211/181/422.jpg','{} https://pics.me.me/when-you-use-furthermore-in-your-essay-im-missing-the-25131584.png','{} https://pics.me.me/when-you-use-furthermore-in-your-essay-sprinkle-dat-extra-16049743.png','{} https://ecdn.teacherspayteachers.com/thumbitem/-Salt-Bae-Meme-Writing-Freebie-2978990-1485278672/original-2978990-1.jpg','{} https://pics.me.me/when-black-parents-add-an-apostrophe-to-their-childs-name-11763958.png','{} http://i0.kym-cdn.com/photos/images/facebook/001/209/136/1ef.png','{} https://pics.me.me/your-head-salt-bae-who-won-the-meme-battle-for-13363207.png','http://runt-of-the-web.com/wordpress/wp-content/uploads/2017/01/Caucasian-on-your-cv.jpg','{} https://lh3.googleusercontent.com/vnCrrk7gvVIoLQsV4HnLiabPXqKA7ls86cm-2Snuk-B9NOup-OtblK8UXYdo3qhBIk7SqtOTUEVpIOMnYmAzJ_H1jKIsJ8ElWPipvAkUthqAxhtwG1ar3ANnuFdC5pTbeNrqb8Q-','{} https://pics.me.me/cheating-lies-deceit-ent-unfaithful-god-when-he-was-creating-11587232.png','{} https://pics.me.me/mexico-autodeciaraodny-autobusas-rapid-a-pre-playas-de-tijuana-ropuerto-11675269.png','{} https://pics.me.me/thedukeofmeines-edukeof-memes-saltbae-911-jetfeul-steelbeams-twintowers-bush-proof-12396857.png','{} https://static.boredpanda.com/blog/wp-content/uploads/2017/01/818286176889085952-png__700.jpg']
	saltbae_current_response = random.choice(saltbae_possible_responses)
	await bot.say(saltbae_current_response.format(ctx.message.author.mention))
@bot.command(pass_context=True)
async def loldog(ctx):
	saltbae_possible_responses = ['{} https://i.imgflip.com/vgh66.jpg','{} http://s2.quickmeme.com/img/b0/b0039e31a5f5ff0fbf9336d47e5d3ec2a80232f3e31e10883c15dbc66be3809d.jpg','{} http://weknowmemes.com/generator/uploads/generated/g1365444091774137766.jpg','{} https://i.chzbgr.com/original/1738866432/hC0106396/','{} http://www.imagefully.com/wp-content/uploads/2015/08/I-Dunno-Lol-Dog-Image.jpg','{} http://images4.fanpop.com/image/photos/15900000/lol-dogs-dogs-15905734-500-375.jpg','{} http://4.bp.blogspot.com/-Rny6ymoavqs/UAhodFDkDPI/AAAAAAAAsiU/8nUf9LUjGyw/s1600/funny-dog-pictures-there-there-ugly-bald-puppy.jpg','{} http://images6.fanpop.com/image/photos/37300000/Funny-Dogs-dogs-37339100-421-428.jpg','{} https://ilifejourney.files.wordpress.com/2012/10/dog-and-spiders.jpg','{} https://i1.wp.com/thefunniestpictures.com/wp-content/uploads/2014/08/Funny-Dog-1.jpg?fit=499%2C334&ssl=1','{} https://ci.memecdn.com/722962.jpg','{} https://collarfolk.com/wp-content/uploads/2017/05/8963bb3fdd1f319b0154cc646a0de37a.jpg','{} https://memegenerator.net/img/instances/500x/64586542/oh-por-deus.jpg','{} https://imgfave.azureedge.net/image_cache/1383619315754765.jpg','{} https://www.seabreeze.com.au/Img/Photos/Other/3722545.jpg','{} http://blogs.discovermagazine.com/discoblog/files/2012/10/dog_meme.jpeg','{} https://static.fjcdn.com/pictures/Lol_98ff89_2584253.jpg','{} http://i0.kym-cdn.com/photos/images/facebook/000/151/934/imade40cakes128548225192353750.jpg','{} http://s2.quickmeme.com/img/a7/a70f44decdb833e94ed530c63cce6775182c03a2f8d5f8301114b52f9724ce80.jpg','{} http://funnyanimalphoto.com/wp-content/uploads/2013/10/dog_loves_bacon.jpg?bd03d3','{} http://s2.quickmeme.com/img/fc/fc02f94bf37ff24f18337ac7de31631ef2b35296e87409184aef259c94f53d1d.jpg','{} https://i.imgur.com/u7mM6mE.jpg', '{} https://i.pinimg.com/736x/71/27/71/712771dd7c68cb9c3ccccc69a9f2e953--bit.jpg','{} https://cdn.discordapp.com/attachments/393566779269709824/396739756437929984/doggie.gif\nCredit to @Windfave#5304.']
	saltbae_current_response = random.choice(saltbae_possible_responses)
	await bot.say(saltbae_current_response.format(ctx.message.author.mention))


#moderation
@bot.group(pass_context=True)
async def moderation(ctx):
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Moderation commands\n\n-kick\n-kick <username mentioned>\nKick someone.\nNeeds permission kick_members.\n\n-ban\n-ban <mentioned username>\nBan someone.\nNeeds ban_members permission.\n\n-clear\n-clear <2 or over>\nClears the amount of messages you want to be cleared.\nNeeds permission manage_messages.\n\n-mute\n-mute <username mentioned>\nmute someone.\nNeeds permission manage_messages.\n\n-unmute\n-unmute <username mentioned>\nunmute someone.\nNeeds permission manage_messages.\n\n-unban\n-unban <mentioned username>\nUnban someone.\nNeeds ban_members permission.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(pass_context = True)
async def kick(ctx, *, member : discord.Member = None):
	if not ctx.message.author.server_permissions.kick_members:
		embed=discord.Embed(description=':x: You don\'t have enough permissions for this: kick_members.', color=0xFF0000)
		await bot.say(embed=embed)
		return
 
	if not member:
		return await bot.say(ctx.message.author.mention + ", specify a user to kick!")
	try:
		await bot.kick(member)
	except Exception as e:
		if 'Privilege is too low' in str(e):
			embed = discord.Embed(description = ":x: The person you are trying to ban has high permissions.", color = 0xFF0000)
			return await bot.say(embed = embed)
 
	embed = discord.Embed(description =f"**%s** has been kicked!"%member.name, color = 0xFF0000)
	return await bot.say(embed = embed)

@bot.command(pass_context = True)
async def ban(ctx, *, member : discord.Member = None, reason:str=None):
	if not ctx.message.author.server_permissions.ban_members:
		return
 
	if not member:
		return await bot.say(ctx.message.author.mention + ", specify a user to ban!")
	try:
		await bot.ban(member)
	except Exception as e:
		if 'Privilege is too low' in str(e):
			embed = discord.Embed(description = ":x: The person you are trying to ban has high permissions.", color = 0xFF0000)
			return await bot.say(embed = embed)
 
	embed = discord.Embed(description = "**%s** has been banned!"%member.name, color = 0xFF0000)
	return await bot.say(embed = embed)

@bot.command(pass_context = True, aliases=['uban'])
async def unban(ctx, *, member : discord.Member = None):
	if not ctx.message.author.server_permissions.ban_members:
		return
 
	if not member:
		return await bot.say(ctx.message.author.mention + ", specify a user to unban!")
	try:
		await bot.unban(member)
	except Exception as e:
		if 'Privilege is too low' in str(e):
			embed = discord.Embed(description = ":x: The person you are trying to ban has high permissions.", color = 0xFF0000)
			return await bot.say(embed = embed)
 
	embed = discord.Embed(description = "**%s** has been unbanned!"%member.name, color = 0xFF0000)
	return await bot.say(embed = embed)

@bot.command(pass_context=True, aliases=['purge','prune'])       
async def clear(ctx, amount:int):
    if not ctx.message.author.server_permissions.manage_messages:
        return
    deleted = await bot.purge_from(ctx.message.channel, limit=amount)
    await asyncio.sleep(10)
    try:
        deleted_message = await bot.say("{}, I have deleted {} messages.".format(ctx.message.author.mention, len(deleted)))
        await bot.delete_message(deleted_message)
    except:
        pass

@bot.command(pass_context=True, no_pm=True)
async def mute(ctx, *, member : discord.Member, reason:str=None):
    if not ctx.message.author.server_permissions.manage_messages:
        return
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)

    embed = discord.Embed(description = "**%s** has been muted!"%member.name, color = 0xFF0000)
    return await bot.say(embed = embed)

@bot.command(pass_context=True, no_pm=True, aliases=['umute'])
async def unmute(ctx, *, member : discord.Member):
    if not ctx.message.author.server_permissions.manage_messages:
        return
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)

    embed = discord.Embed(description = "**%s** has been unmuted!"%member.mention, color = 0xFF0000)
    return await bot.say(embed = embed)
@bot.command(pass_context = True, aliases=['sban'])
async def softban(ctx, *, member : discord.Member = None):
	if not ctx.message.author.server_permissions.ban_members:
		return
 
	if not member:
		return await bot.say(ctx.message.author.mention + ", specify a user to ban!")
	try:
		await bot.ban(member)
		await bot.unban(member.server,member)
	except Exception as e:
		if 'Privilege is too low' in str(e):
			embed = discord.Embed(description = ":x: The person you are trying to ban has high permissions.", color = 0xFF0000)
			return await bot.say(embed = embed)
 
	embed = discord.Embed(description = "**%s** has been soft-banned!"%member.name, color = 0xFF0000)
	return await bot.say(embed = embed)

		

#server
@bot.group(pass_context=True)
async def server(ctx):
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Server commands\n\n-serverinfo\nCheck the info about the server.\n\n-bans\nLists the banned people on the server.\n\n-userinfo\nCheck info about you or other users.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(pass_context = True)
async def serverinfo(ctx):

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #if theres too much roles lol
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
    x = await bot.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    xc = len(x)
    if xc == 0:
        x = 'No one is banned.'	
    embed = discord.Embed(title = "List of banned people:", description = x, color = 0xFFFFF)
    return await bot.say(embed = embed)

@bot.command(pass_context=True)
async def userinfo(ctx, user: discord.Member = None):
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
	if ctx.invoked_subcommand is None:
		embed=discord.Embed(description='Utility commands\n\n\n-avatar\nGet the avatar link of a user.\n\n-poll\nCreate a poll with the thumbs up, shrug and thumbs down reaction.\n\n-embed\nEmbed a message so CommuniBot can say what you wanted.', color=0x2874A6)
		await bot.say(embed=embed)

@bot.command(pass_context=True, no_pm=True)
async def avatar(ctx, member : discord.Member = None):
    channel = ctx.message.channel
    if member is None:
        member = ctx.message.author
    await bot.say(member.avatar_url)

@bot.command(pass_context=True)
async def poll(ctx,*, message: str):
    "Creates a poll"
    
    embed = discord.Embed(color = ctx.message.author.color, timestamp = datetime.datetime.utcnow())
    embed.set_author(name = "Poll", icon_url = ctx.message.author.avatar_url)
    embed.description = (message)
    embed.set_footer(text = ctx.message.author.name)
    x = await bot.say(embed = embed)
    await bot.add_reaction(x, "👍")
    await bot.add_reaction(x, "🤷")
    await bot.add_reaction(x, "👎")

@bot.command(pass_context=True)
async def embed(ctx,*, message: str):
    "embeds a message"
    
    embed = discord.Embed(color = ctx.message.author.color, timestamp = datetime.datetime.utcnow())
    embed.set_author(name = f"{ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    embed.description = (message)
    embed.set_footer(text = ctx.message.author.name)
    await bot.say(embed=embed)

bot.run(Secrets['Token'])