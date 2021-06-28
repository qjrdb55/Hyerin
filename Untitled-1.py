import discord, asyncio, datetime, pytz

client = discord.Client()

@client.event
async def on_ready():
    print("bot start")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("주인님께 조련당하는 중"))

@client.event
async def on_message(message):
    if message.content == "테스트":
        await message.channel.send ("{} | {}, Hello".format(message.author, message.author.mention))
        await message.author.send ("{} | {}, User, Hello".format(message.author, message.author.mention))

    if message.content == "test":
        ch = client.get_channel(859072254959812648)
        await ch.send ("{} | {}, User, Hello".format(ch.author, ch.author.mention))

    if message.content.startswith ("!공지"):
        await message.channel.purge(limit=1)
        i = (message.author.guild_permissions.administrator)
        if i is True:
            notice = message.content[4:]
            channel = client.get_channel(859075763403227136)
            embed = discord.Embed(title="**ANNOUNCEMENT**", description="\n\n\n{}\n\n--------------------------------------------------------------".format(notice),timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00ff00)
            embed.set_footer(text="Powered by Hyerin Chae | 담당 관리자 : jeremyyy#1234".format(message.author), icon_url="https://cdn.discordapp.com/attachments/855365831265222666/858686703509438474/unknown.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/855365831265222666/858687900409397268/unknown.png")
            await channel.send ("@everyone", embed=embed)
            await message.author.send("*[ BOT 자동 알림 ]* | 정상적으로 공지가 채널에 작성이 완료되었습니다 : )\n\n[ 기본 작성 설정 채널 ] : {}\n[ 공지 발신자 ] : {}\n\n[ 내용 ]\n{}".format(channel, message.author, notice))
 
        if i is False:
            await message.channel.send("{}, 당신은 관리자가 아닙니다".format(message.author.mention))
            
access_token = os.environ["BOT_TOKEN"]
client.run('ODU4Njc1MjM2MTM1ODk1MDcz.YNhloQ.1IFq_60bUS4nE42iwEbO7I1PXMI')
