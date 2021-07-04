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
            
@client.event
async def on_connect():
    db = sqlite3.connect('main.db')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main(
        name TEXT,
        id TEXT,
        yn TEXT,
        stime TEXT
        )
    ''')
    print("출퇴근봇 ONLINE")
    game = discord.Game('!명령어')
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    achannel = 859075763403227136


    if message.content == '!명령어':
        embed = discord.Embed(title='명령어', description='!출근\n!퇴근\n!등록여부\n!등록 @유저')
        await message.channel.send(embed=embed)
        
    if message.content.startswith("!등록") and not message.content == '!등록여부':
        if message.author.guild_permissions.administrator:
            try:
                target = message.mentions[0]
            except:
                await message.channel.send('유저가 지정되지 않았습니다')

            try:
                db = sqlite3.connect('main.db')
                cursor = db.cursor()
                cursor.execute(f'SELECT yn FROM main WHERE id = {target.id}')
                result = cursor.fetchone()
                if result is None:
                    sql = 'INSERT INTO main(name, id, yn, stime) VALUES(?,?,?,?)'
                    val = (str(target), str(target.id), str('0'), str('0'))
                else:
                    embed = discord.Embed(title='❌  등록 실패', description='이미 등록된 유저입니다', color=0xFF0000)
                    await message.channel.send(embed=embed)
                    return
                cursor.execute(sql, val)
                db.commit()
                db.close()

                embed = discord.Embed(title='✅  등록 성공', description=f'등록을 성공하였습니다', colour=discord.Colour.green())
                embed.set_author(name=target, icon_url=target.avatar_url)
                await message.channel.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title='❌  오류', description=f'오류가 발생하였습니다\n`{str(e)}`', color=0xFF0000)
                await message.channel.send(embed=embed)
        else:
            await message.channel.send(f'{message.author.mention} 권한이 부족합니다')

    if message.content == '!등록여부':
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        cursor.execute(f'SELECT yn FROM main WHERE id = {message.author.id}')
        result = cursor.fetchone()
        if result is None:
            await message.channel.send(f'**{message.author}**님은 등록되지 않았습니다')
        else:
            await message.channel.send(f'**{message.author}**님은 등록되어 있습니다')

    if message.content == "!출근":
        try:
            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f'SELECT yn FROM main WHERE id = {message.author.id}')
            result = cursor.fetchone()
            if result is None:
                await message.channel.send(f'{message.author.mention} 등록되지 않은 유저입니다')
                return
            if "y" in result:
                await message.channel.send(f'{message.author.mention} 이미 출근 상태입니다')
                return
            else:
                sql = f'UPDATE main SET yn = ? WHERE id = {message.author.id}'
                val = (str('y'),)
                cursor.execute(sql, val)
                sql = f'UPDATE main SET stime = ? WHERE id = {message.author.id}'
                val = (str(time.time()),)
                cursor.execute(sql, val)
            db.commit()
            db.close()

            embed = discord.Embed(title='', description=f'**{message.author.mention}** 님이 출근하였습니다',
                                  color=discord.Colour.green())
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text='출근시간: ' + time.strftime('%m-%d %H:%M'))
            await client.get_channel(int(achannel)).send(embed=embed)
            await message.channel.send(f'{message.author.mention} 출근완료')
        except Exception as e:
            embed = discord.Embed(title='❌  오류', description=f'오류가 발생하였습니다\n`{str(e)}`', color=0xFF0000)
            await message.channel.send(embed=embed)

    if message.content == "!퇴근":
        try:
            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f'SELECT yn FROM main WHERE id = {message.author.id}')
            result = cursor.fetchone()
            if result is None:
                await message.channel.send(f'{message.author.mention} 등록되지 않은 유저입니다')
                return
            else:
                if not "y" in result:
                    await message.channel.send(f'{message.author.mention} 출근상태가 아닙니다')
                    return
                elif "y" in result:
                    sql = f'UPDATE main SET yn = ? WHERE id = {message.author.id}'
                    val = (str('n'),)
                    cursor.execute(sql, val)

                    cursor.execute(f'SELECT stime FROM main WHERE id = {message.author.id}')
                    result = cursor.fetchone()
                    result = str(result).replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                    result = result.split(".")[0]
                    result = int(result)

                    cctime = round(time.time()) - result
            db.commit()
            db.close()

            if cctime >= 3600:
                worktime = round(cctime / 3600)
                danwe = '시간'
            elif cctime < 3600:
                worktime = round(cctime / 60)
                danwe = '분'

            embed = discord.Embed(title='', description=f'**{message.author.mention}** 님이 퇴근하였습니다',
                                  color=discord.Colour.red())
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text='퇴근시간: ' + time.strftime('%m-%d %H:%M') + '\n' + '근무시간: ' + str(worktime) + str(danwe))
            await client.get_channel(int(achannel)).send(embed=embed)
            await message.channel.send(f'{message.author.mention} 퇴근완료')
        except Exception as e:
                embed = discord.Embed(title='❌  오류', description=f'오류가 발생하였습니다\n`{str(e)}`', color=0xFF0000)
                await message.channel.send(embed=embed)
                
access_token = os.environ["BOT_TOKEN"]
client.run("ODU4Njc1MjM2MTM1ODk1MDcz.YNhloQ.ZHEyktzAHAcbwlKDkxPXmpRbtXQ")
