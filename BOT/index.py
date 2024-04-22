from discord import user
from discord_components import DiscordComponents, ComponentsBot, Select, SelectOption, Button, ButtonStyle, ActionRow
import discord, sqlite3, datetime, randomstring, os, setting, random
from discord_components.ext.filters import user_filter
import asyncio, requests, json
from setting import admin_id, domain, bot_name, license_master_ids
from datetime import timedelta
from discord_webhook import DiscordEmbed, DiscordWebhook
from discord_buttons_plugin import ButtonType
from asyncio import futures
from functools import partial
import time
    
bot = discord.Client()
charginguser = []
buyinguser = []
bankchanginguser = []
total_master_ids = [569847826708955146]

def get_roleid(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT roleid FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    if (str(data).isdigit()):
        return int(data)
    else:
        return data

def get_logwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT logwebhk FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    return data

def get_buylogwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT buylogwebhk FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    return data

def add_time(now_days, add_days):
    ExpireTime = datetime.datetime.strptime(now_days, '%Y-%m-%d %H:%M')
    ExpireTime_STR = (ExpireTime + timedelta(days=add_days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def is_expired(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        return False
    else:
        return True


def now_time():
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    return nowDatetime

def get_logwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT logwebhk FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    return data

def make_expiretime(days):
    ServerTime = datetime.datetime.now()
    ExpireTime = ServerTime + timedelta(days=days)
    ExpireTime_STR = (ServerTime + timedelta(days=days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def nowstr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"[!] 봇 이름 : {bot.user.name}\n[!] 봇 아이디 : {bot.user.id}\n[!] 참가 중인 서버 : {len(bot.guilds)}개")
    while True:
        await bot.change_presence(activity=discord.Game(f"KA | {len(bot.guilds)}서버 사용"),status=discord.Status.online)
        await asyncio.sleep(3)

@bot.event
async def on_message(message):

    if message.channel.id == 951759000268075018:
        await message.add_reaction('💗')

    if message.channel.id == 951759100809715722:
        await message.add_reaction('💗')

    if message.content == "!백업시작":
        if message.author.id == 569847826708955146:
            channel = bot.get_channel(951758424335605790)
            embed = discord.Embed(color=0x5c6bdf, title=f"KA Vending DataBase", description=f"DB 백업이 시작되었습니다.")
            await channel.send(embed=embed)

    if message.content == "!백업종료":
        if message.author.id == 569847826708955146:
            channel = bot.get_channel(951758424335605790)
            embed = discord.Embed(color=0x5c6bdf, title=f"KA Vending DataBase", description=f"DB 백업이 종료되었습니다.")
            await channel.send (embed=embed)

    if message.content.startswith('!생성 '):
        if message.author.id in license_master_ids:
            if not isinstance(message.channel, discord.channel.DMChannel):
                try:
                    amount = int(message.content.split(" ")[1])
                except:
                    await message.channel.send("올바른 생성 개수를 입력해주세요.")
                    return
                if 1 <= amount <= 50:
                    try:
                        license_length = int(message.content.split(" ")[2])
                    except:
                        await message.channel.send("올바른 생성 기간을 입력해주세요.")
                        return
                    else:
                        codes = []
                        for _ in range(amount):
                            code = "KA-" + randomstring.pick(20)
                            codes.append(code)
                            con = sqlite3.connect("../DB/" + "license.db")
                            cur = con.cursor()
                            cur.execute("INSERT INTO license Values(?, ?, ?, ?, ?);", (code, license_length, 0, "None", 0))
                            con.commit()
                            con.close()
                            generated_key = "\n".join(codes)
                        await message.channel.send(embed=discord.Embed(title="생성 성공", description="디엠을 확인해주세요.", color=0x5c6cdf))
                        await message.author.send("\n".join(codes))
                        webhook = DiscordWebhook(username="KA Button", avatar_url="https://cdn.discordapp.com/attachments/783489649985060904/937736166961184768/KA_Vending.png", url="https://ptb.discord.com/api/webhooks/951760056892915743/lwcQ6z5JpsQGhqrKd3sRxZ1TRAsryY5VpNt6MP90AkdbNC2aU7LAvqKxUImq8EfdpqRN")
                        eb = DiscordEmbed(title='라이센스 생성 로그', description=f'```유저 : {message.author.name}#{message.author.discriminator} ({message.author.id})\n개수 : {message.content.split(" ")[1]} 개\n기간 : {message.content.split(" ")[2]} 일\n라이센스 : {generated_key}```', color=0x5c6cdf)
                        webhook.add_embed(eb)
                        webhook.execute()
                else:
                    await message.channel.send(embed=discord.Embed(title="생성 실패", description="최대 50개까지 생성 가능합니다.", color=0xff0000))

    if (message.content.startswith("!서버리스트")):
        if message.author.id in total_master_ids:
            guild_list = bot.guilds
            for i in guild_list:
                await message.channel.send("서버 ID: {} / 서버 이름: {}".format(i.id, i.name))

    if message.content == "!초기화 문상":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET mm = ?", (0,))
                con.commit()
                con.close
                await message.channel.send(embed=discord.Embed(title="초기화 성공", description="문화상품권 누적 충전 금액이 0원으로 수정되었습니다.", color=0x5c6cdf))

    if message.content == "!초기화 계좌":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET bankm = ?", (0,))
                con.commit()
                con.close
                await message.channel.send(embed=discord.Embed(title="초기화 성공", description="계좌이체 누적 충전 금액이 0원으로 수정되었습니다.", color=0x5c6cdf))

    if message.content == "!초기화 전체":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET totalm = ?", (0,))
                con.commit()
                con.close
                await message.channel.send(embed=discord.Embed(title="초기화 성공", description="총 충전 금액이 0원으로 수정되었습니다.", color=0x5c6cdf))

    if message.content.startswith('!등록 '):
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            license_key = message.content.split(" ")[1]
            con = sqlite3.connect("../DB/" + "license.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
            search_result = cur.fetchone()
            con.close()
            if (search_result != None):
                if (search_result[2] == 0):
                    if not (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                        con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                        cur = con.cursor()
                        cur.execute("CREATE TABLE serverinfo (id TEXT, expiredate TEXT, cultureid TEXT, culturepw TEXT, pw TEXT, roleid TEXT, logwebhk TEXT, buylogwebhk TEXT, culture_fee TEXT, bank TEXT, normaloff INTEGER, vipoff INTEGER, vvipoff INTEGER, reselloff INTEGER, color TEXT, chargeban INTEGER, vipautosetting INTEGER, vvipautosetting INTEGER, buyusernamehide TEXT, viproleid INTEGER, vviproleid INTEGER, webhookprofile TEXT, webhookname TEXT, notice TEXT, sms INTEGER, least INTEGER, bankm TEXT, mm TEXT, totalm TEXT);")
                        con.commit()
                        first_pw = randomstring.pick(10)
                        cur.execute("INSERT INTO serverinfo VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (message.guild.id, make_expiretime(int(sqlite3.connect("../DB/" + "license.db").cursor().execute("SELECT * FROM license WHERE code == ?;", (license_key,)).fetchone()[1])), "", "", first_pw, 0, "", "", 0, "", 0, 0, 0, 0, "검정", 3, 999999999999, 9999999999999, "N", 0, 0, "https://cdn.discordapp.com/attachments/569848215353032704/962372967612960828/Roy_Vending.png", "KA Button", "공지사항", 0, 0, 0, 0, 0))
                        con.commit()
                        cur.execute("CREATE TABLE users (id INTEGER, money INTEGER, bought INTEGER, warnings INTEGER, rank TEXT, buycount INTEGER, sms INTEGER, tag INTERGER, ban INTEGER);")
                        con.commit()
                        cur.execute("CREATE TABLE products (name INTEGER, money INTEGER, stock TEXT, produrl TEXT);")
                        con.commit()
                        cur.execute("CREATE TABLE banklog (id INTEGER, name TEXT, money INTEGER);")
                        con.commit()
                        cur.execute("CREATE TABLE bankwait (day TEXT, user TEXT, id TEXT, name TEXT, amount INTEGER);")
                        con.commit()
                        con.close()
                        con = sqlite3.connect("../DB/log.db")
                        cur = con.cursor()
                        cur.execute("INSERT INTO webhook VALUES(?, ?);", (message.guild.id, ""))
                        con.commit()
                        con.close()
                        con = sqlite3.connect("../DB/" + "license.db")
                        cur = con.cursor()
                        cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;", (1, nowstr(), message.guild.id, license_key))
                        con.commit()
                        con.close()
                        con = sqlite3.connect("../DB/" + "license.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
                        await message.author.send(embed=discord.Embed(title="서버 등록 성공", description=f"서버가 성공적으로 등록되었습니다.\n라이센스 기간: `{search_result[1]}`일\n만료일: `" + make_expiretime(int(sqlite3.connect("../DB/" + "license.db").cursor().execute("SELECT * FROM license WHERE code == ?;", (license_key,)).fetchone()[1])) + f"`\n웹패널: {domain}\n아이디: `" +str(message.guild.id) + "`\n비밀번호: `" + first_pw + "`", color=0x4461ff),
                            components = [
                                ActionRow(
                                    Button(style=ButtonType().Link,label = "웹패널",url=domain),
                                )
                            ]
                        )
                        await message.channel.send(embed=discord.Embed(title="서버 등록 성공", description="서버가 성공적으로 등록되었습니다.", color=0x5c6cdf))
                        webhook = DiscordWebhook(username="KA Button", avatar_url="https://cdn.discordapp.com/attachments/783489649985060904/937736166961184768/Roy_Vending.png", url="https://canary.discord.com/api/webhooks/969682032147984435/on3GYsITrPtUAzT8f5nAcCb-7TQhUbLgVWganKib-Cgskt9qcaL6Xnftp0fIeiFQcXSq")
                        eb = DiscordEmbed(title='서버 등록 로그', description=f'```유저 : {message.author.name}#{message.author.discriminator} ({message.author.id})\n서버 이름 : {message.guild.name}\n서버 아이디 : {message.guild.id}\n라이센스 : {license_key}```', color=0x5c6cdf)
                        webhook.add_embed(eb)
                        webhook.execute()
                        con.close()
                    else:
                        await message.channel.send(embed=discord.Embed(title="서버 등록 실패", description="이미 등록된 서버이므로 등록할 수 없습니다.\n기간 추가를 원하신다면 !라이센스 명령어를 이용해주세요.", color=0x5c6cdf))
                else:
                    await message.channel.send(embed=discord.Embed(title="서버 등록 실패", description="이미 사용된 라이센스입니다.\n관리자에게 문의해주세요.", color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="서버 등록 실패", description="존재하지 않는 라이센스입니다.", color=0x5c6cdf))
    
    if message.content.startswith("!서버 이전 "):
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if not (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                try:
                    server_id = message.content.split(" ")[2].split(" ")[0]
                    webpanel_pw = message.content.split(" ")[3]
                except:
                    await message.channel.send(embed=discord.Embed(title="서버 이전 실패", description="서버 아이디와 웹패널 비밀번호를 확인해주세요.", color=0xff0000))
                if (os.path.isfile("../DB/" + server_id + ".db")):
                    con = sqlite3.connect("../DB/" + server_id + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM serverinfo;", ())
                    server_info = cur.fetchone()
                    con.close()
                    if server_info[4] == webpanel_pw:
                        con = sqlite3.connect("../DB/" + server_id + ".db")
                        cur = con.cursor()
                        cur.execute("UPDATE serverinfo SET id = ?;", (str(message.guild.id),))
                        con.commit()
                        con.close()
                        os.rename("../DB/" + server_id + ".db", "../DB/" + str(message.guild.id) + ".db")
                        con = sqlite3.connect("../DB/log.db")
                        cur = con.cursor()
                        cur.execute(f"UPDATE webhook SET server = ? WHERE server = '{server_id}';", (str(message.guild.id),))
                        con.commit()
                        con.close()
                        con = sqlite3.connect("../DB/charge_log.db")
                        cur = con.cursor()
                        cur.execute(f"UPDATE log SET server_id = ? WHERE server_id = '{server_id}';", (str(message.guild.id),))
                        con.commit()
                        con.close()
                        con = sqlite3.connect("../DB/buy_log.db")
                        cur = con.cursor()
                        cur.execute(f"UPDATE log SET server_id = ? WHERE server_id = '{server_id}';", (str(message.guild.id),))
                        con.commit()
                        con.close()
                        await message.author.send(embed=discord.Embed(title="서버 이전 성공", description="만료일: `" + server_info[1] + f"`\n웹패널: {domain}\n아이디: `" +str(message.guild.id) + "`\n비밀번호: `" + server_info[4] + "`", color=0x4461ff),
                        components = [
                            ActionRow(
                                Button(style=ButtonType().Link,label = "웹패널",url=domain),
                            )
                        ]
                    )
                        await message.channel.send(embed=discord.Embed(title="서버 이전 성공", description="서버가 성공적으로 이전되었습니다", color=0x5c6cdf))
                    else:
                        await message.channel.send(embed=discord.Embed(title="서버 이전 실패", description="웹패널 비밀번호를 확인해주세요.", color=0xff0000))
                else:
                    await message.channel.send(embed=discord.Embed(title="서버 이전 실패", description="올바른 서버 아이디를 입력해주세요.", color=0xff0000))
            else:
                await message.channel.send(embed=discord.Embed(title="서버 이전 실패", description="이미 서버가 등록되어 있습니다.", color=0xff0000))

    if message.content == '!디비출력':
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                try:
                    await message.delete()
                except:
                    pass
                embed = discord.Embed(title=bot_name, description='원하시는 버튼을 클릭해주세요.', color=0x5c6cdf)
                await message.channel.send(
                    embed=embed,
                    components = [
                        ActionRow(
                            Button(style=ButtonStyle.blue,label = "데이터베이스 출력",custom_id="디비백업"),

                        )
                    ]
                )

    if message.content.startswith("!컬쳐등록 "):
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                try:
                    await message.delete()
                except:
                    pass
                cid = message.content.split(" ")[1]
                cpw = message.content.split(" ")[2]
                con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET cultureid = ?, culturepw = ?;", (cid, cpw,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 컬쳐랜드 계정이 변경되었습니다.\n설정한 값 : {cid}, {cpw}", color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다, 다시 시도해주세요.", color=0xff0000))

    if message.content == "!수정 컬쳐아이디":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="컬쳐아이디 변경", description="원하시는 아이디를 입력해주세요.",color=0x5c6cdf))
                def check(cultureid):
                    return (cultureid.author.id == message.author.id)
                cultureid = await bot.wait_for("message", timeout=60, check=check)
                cultureid = cultureid.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET cultureid = ?",(cultureid,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 컬쳐랜드 아이디가 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 컬쳐비번":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="컬쳐비번 변경", description="원하시는 비밀번호를 입력해주세요.",color=0x5c6cdf))
                def check(culturepw):
                    return (culturepw.author.id == message.author.id)
                culturepw = await bot.wait_for("message", timeout=60, check=check)
                culturepw = culturepw.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET culturepw = ?",(culturepw,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 컬쳐랜드 비밀번호가 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))


    if message.content == "!수정 웹훅이름":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="웹훅 이름 변경", description="원하시는 웹훅 이름을 입력해주세요.",color=0x5c6cdf))
                def check(webhookname):
                    return (webhookname.author.id == message.author.id)
                webhookname = await bot.wait_for("message", timeout=60, check=check)
                webhookname = webhookname.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET webhookname = ?",(webhookname,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 웹훅 이름이 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 웹훅프사":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="웹훅프사 변경", description="원하시는 프로필 사진 URL을 입력해주세요.",color=0x5c6cdf))
                def check(webhookprofile):
                    return (webhookprofile.author.id == message.author.id)
                webhookprofile = await bot.wait_for("message", timeout=60, check=check)
                webhookprofile = webhookprofile.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET webhookprofile = ?",(webhookprofile,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 웹훅 프로필 사진이 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 익명여부":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="익명 여부 변경", description="원하시는 익명 여부를 입력해주세요. **(Y = 익명 / N = 노익명)**",color=0x5c6cdf))
                def check(buyusernamehide):
                    return (buyusernamehide.author.id == message.author.id)
                buyusernamehide = await bot.wait_for("message", timeout=60, check=check)
                buyusernamehide = buyusernamehide.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET buyusernamehide = ?",(buyusernamehide,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 구매로그 익명 여부가 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 수수료":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="수수료 변경", description="원하시는 수수료를 입력해주세요.",color=0x5c6cdf))
                def check(culture_fee):
                    return (culture_fee.author.id == message.author.id)
                culture_fee = await bot.wait_for("message", timeout=60, check=check)
                culture_fee = culture_fee.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET culture_fee = ?",(culture_fee,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 수수료가 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 구매로그웹훅":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="구매로그 웹훅 변경", description="원하시는 웹훅을 입력해주세요.",color=0x5c6cdf))
                def check(buylogwebhk):
                    return (buylogwebhk.author.id == message.author.id)
                buylogwebhk = await bot.wait_for("message", timeout=60, check=check)
                buylogwebhk = buylogwebhk.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET buylogwebhk = ?",(buylogwebhk,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 구매로그 웹훅이 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 관리자로그웹훅":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="관리자 로그 웹훅 변경", description="원하시는 웹훅을 입력해주세요.",color=0x5c6cdf))
                def check(logwebhk):
                    return (logwebhk.author.id == message.author.id)
                logwebhk = await bot.wait_for("message", timeout=60, check=check)
                logwebhk = logwebhk.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET logwebhk = ?",(logwebhk,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 관리자 로그 웹훅이 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 충전차단수":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="충전 차단 수 변경", description="원하시는 충전 차단 수를 입력해주세요.",color=0x5c6cdf))
                def check(chargeban):
                    return (chargeban.author.id == message.author.id)
                chargeban = await bot.wait_for("message", timeout=60, check=check)
                chargeban = chargeban.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET chargeban = ?",(chargeban,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 충전 차단 수가 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 색깔":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="색깔 변경", description="원하시는 색깔을 입력해주세요. **( 파랑, 빨강, 초록, 회색, 검정 )**",color=0x5c6cdf))
                def check(color):
                    return (color.author.id == message.author.id)
                color = await bot.wait_for("message", timeout=60, check=check)
                if color.content == "파랑" or color.content == "빨강" or color.content == "초록" or color.content == "회색" or color.content == "검정": 
                    color = color.content
                    con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                    cur = con.cursor()
                    cur.execute("UPDATE serverinfo SET color = ?",(color,))
                    con.commit()
                    cur.execute("SELECT * FROM serverinfo;")
                    server_info = cur.fetchone()
                    con.close()
                    await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 버튼 및 임베드 색깔이 변경되었습니다.",color=0x5c6cdf))
                else:
                    await message.channel.send(embed=discord.Embed(title='변경 실패', description='색깔은 **파랑**, **빨강**, **초록**, **회색**, **검정**만 지정 가능합니다.', color=0xff0000))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 공지사항":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="공지사항 변경", description="원하시는 공지사항을 입력해주세요.",color=0x5c6cdf))
                def check(notice):
                    return (notice.author.id == message.author.id)
                notice = await bot.wait_for("message", timeout=60, check=check)
                notice = notice.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET notice = ?",(notice,))
                con.commit()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 공지사항이 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 최소금액":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="최소 충전 금액 변경", description="최소 충전 금액을 숫자로만 입력해주세요.",color=0x5c6cdf))
                def check(least):
                    return (least.author.id == message.author.id)
                least = await bot.wait_for("message", timeout=60, check=check)
                least = least.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET least = ?",(least,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 최소 충전 금액이 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!수정 웹패널비번":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="웹패널비번 변경", description="원하시는 비밀번호를 입력해주세요.",color=0x5c6cdf))
                def check(pw):
                    return (pw.author.id == message.author.id)
                pw = await bot.wait_for("message", timeout=60, check=check)
                pw = pw.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET pw = ?",(pw,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 웹패널 비밀번호가 변경되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!제품삭제":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="제품 삭제", description="삭제를 원하시는 제품명을 입력해주세요.",color=0x5c6cdf))
                def check(pname):
                    return (pname.author.id == message.author.id)
                pname = await bot.wait_for("message", timeout=60, check=check)
                pname = pname.content
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("DELETE FROM products WHERE name == ?", (pname,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 제품이 삭제되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))

    if message.content == "!제품생성":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="제품 생성", description="제품명을 입력해주세요.",color=0x5c6cdf))
                def check(msg):
                    return (not isinstance(msg.channel, discord.channel.DMChannel) and (message.author.id == msg.author.id))
                try:
                    pname = await bot.wait_for("message", timeout=60, check=check)
                    pname = pname.content
                except asyncio.TimeoutError:
                    try:
                        await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                    except:
                        pass
                    return None
                await message.channel.send(embed=discord.Embed(title="제품 생성", description="제품 가격을 입력해주세요.",color=0x5c6cdf))
                try:
                    pprice = await bot.wait_for("message", timeout=60, check=check)
                    pprice = pprice.content
                except asyncio.TimeoutError:
                    try:
                        await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                    except:
                        pass
                con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM products WHERE name == ?;", (message.guild.id,))
                prod = cur.fetchone()
                if (prod == None):
                    con = sqlite3.connect("../DB/" + str(message.guild.id) +".db")
                    cur = con.cursor()
                    cur.execute("INSERT INTO products VALUES(?, ?, ?, ?);", (pname, pprice, "", ""))
                    con.commit()
                    con.close()
                await message.channel.send(embed=discord.Embed(title="추가 성공", description=f"성공적으로 제품 생성이 완료되었습니다.",color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="추가 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))
    
    if message.content.startswith("!차단 "):
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if not (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))
                return

                try:
                    await message.delete()
                except:
                    pass
            try:
                userId = message.mentions[0].id
            except:
                userId = int(message.content.split(" ")[1])
            try:
                ban = message.content.split(" ")[2]
            except:
                return await message.channel.send(embed=discord.Embed(title="변경 실패", description="`!차단 (@유저) (숫자)`으로 입력해주세요.", color=0x5c6cdf))
            con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (userId,))
            user_info = cur.fetchone()
            if not user_info:
                cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (userId, 0, 0, 0, "일반", 0, 0, message.author.name, 0,))
                con.commit()
                con.close()
            cur.execute("UPDATE users SET ban = ? WHERE id == ?;", (ban, userId))
            con.commit()
            await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 유저의 계좌이체 차단 여부가 변경되었습니다.\n설정한 값 : {ban}", color=0x5c6cdf))

    if message.content.startswith("!경고수 "):
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if not (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.",color=0xff0000))
                return
                try:
                    await message.delete()
                except:
                    pass
            try:
                userId = message.mentions[0].id
            except:
                userId = int(message.content.split(" ")[1])
            try:
                warning = message.content.split(" ")[2]
            except:
                return await message.channel.send(embed=discord.Embed(title="변경 실패", description="`!경고수 (@유저) (숫자)`으로 입력해주세요.", color=0xff0000))
            con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (userId,))
            user_info = cur.fetchone()
            if not user_info:
                cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (userId, 0, 0, 0, "일반", 0, 0, message.author.name, 0))
                con.commit()
                con.close()
            cur.execute("UPDATE users SET warnings = ? WHERE id == ?;", (warning, userId))
            con.commit()
            await message.channel.send(embed=discord.Embed(title="변경 성공", description=f"성공적으로 유저 경고 수가 변경되었습니다.\n설정한 값 : {warning}", color=0x5c6cdf))

    if message.content == "!구매메시지":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if not isinstance(message.channel, discord.channel.DMChannel):
                if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                    await message.delete()
                    title = await message.channel.send(embed=discord.Embed(title="구매 메시지", description="제품 이름을 입력해주세요.", color=0x5c6cdf))
                    def check(msg):
                        return (not isinstance(msg.channel, discord.channel.DMChannel) and (message.author.id == msg.author.id))
                    try:
                        product_name = await bot.wait_for("message", timeout=60, check=check)
                        await title.delete()
                        await product_name.delete()
                    except asyncio.TimeoutError:
                        try:
                            await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                        except:
                            pass
                        return None
                    pdes = await message.channel.send(embed=discord.Embed(title="구매 메시지", description="제품 설명을 입력해주세요.",color=0x5c6cdf))
                    try:
                        product_content = await bot.wait_for("message", timeout=60, check=check)
                        await pdes.delete()
                        await product_content.delete()
                    except asyncio.TimeoutError:
                        try:
                            await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                        except:
                            pass
                        return None
                    bdes = await message.channel.send(embed=discord.Embed(title="구매 메시지", description="버튼 내용을 입력해주세요.",color=0x5c6cdf))
                    try:
                        button_content = await bot.wait_for("message", timeout=60, check=check)
                        await bdes.delete()
                        await button_content.delete()
                    except asyncio.TimeoutError:
                        try:
                            await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                        except:
                            pass
                        return None
                    await message.channel.send(embed=discord.Embed(title=product_name.content, description=product_content.content, color=0x5c6cdf),
                    components = [
                        ActionRow(
                            Button(style=ButtonStyle.blue,label=button_content.content,custom_id="구매")
                        )
                    ])

    if message.content == "!바로가기":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if not isinstance(message.channel, discord.channel.DMChannel):
                if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                    await message.delete()
                    title = await message.channel.send(embed=discord.Embed(title="바로가기 설정", description="제목을 입력해주세요.", color=0x5c6cdf))
                    def check(msg):
                        return (not isinstance(msg.channel, discord.channel.DMChannel) and (message.author.id == msg.author.id))
                    try:
                        product_name = await bot.wait_for("message", timeout=60, check=check)
                        await title.delete()
                        await product_name.delete()
                    except asyncio.TimeoutError:
                        try:
                            await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                        except:
                            pass
                        return None
                    des = await message.channel.send(embed=discord.Embed(title="바로가기 설정", description="내용을 입력해주세요.",color=0x5c6cdf))
                    try:
                        product_content = await bot.wait_for("message", timeout=60, check=check)
                        await des.delete()
                        await product_content.delete()
                    except asyncio.TimeoutError:
                        try:
                            await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                        except:
                            pass
                        return None
                    link = await message.channel.send(embed=discord.Embed(title="바로가기 설정", description="바로가기 링크를 입력해주세요.",color=0x5c6cdf))
                    try:
                        link_content = await bot.wait_for("message", timeout=60, check=check)
                        await link.delete()
                        await link_content.delete()
                    except asyncio.TimeoutError:
                        try:
                            await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                        except:
                            pass
                        return None
                    but = await message.channel.send(embed=discord.Embed(title="바로가기 설정", description="버튼 내용을 입력해주세요.",color=0x5c6cdf))
                    try:
                        button_content = await bot.wait_for("message", timeout=60, check=check)
                        await but.delete()
                        await button_content.delete()
                    except asyncio.TimeoutError:
                        try:
                            await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                        except:
                            pass
                        return None
                    await message.channel.send(embed=discord.Embed(title=product_name.content, description=product_content.content, color=0x5c6cdf),
                    components = [
                        ActionRow(
                            Button(style=ButtonType().Link,label=button_content.content,url=link_content.content)
                        )
                    ])

    if message.content == "!임베드":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if not isinstance(message.channel, discord.channel.DMChannel):
                if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                    await message.delete()
                    title = await message.channel.send(embed=discord.Embed(title="임베드 설정", description="제목을 입력해주세요.", color=0x5c6cdf))
                    def check(msg):
                        return (not isinstance(msg.channel, discord.channel.DMChannel) and (message.author.id == msg.author.id))
                    try:
                        product_name = await bot.wait_for("message", timeout=60, check=check)
                        await title.delete()
                        await product_name.delete()
                    except asyncio.TimeoutError:
                        try:
                            await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                        except:
                            pass
                        return None
                    des = await message.channel.send(embed=discord.Embed(title="임베드 설정", description="내용을 입력해주세요.",color=0x5c6cdf))
                    try:
                        product_content = await bot.wait_for("message", timeout=60, check=check)
                        await des.delete()
                        await product_content.delete()
                    except asyncio.TimeoutError:
                        try:
                            await message.channel.send(embed=discord.Embed(description="시간 초과",color=0x5c6cdf))
                        except:
                            pass
                        return None
                    await message.channel.send(embed=discord.Embed(title=product_name.content, description=product_content.content, color=0x5c6cdf))

    if message.content.startswith("!명령어"):
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            await message.channel.send(embed=discord.Embed(title="버튼자판기 명령어", description="!컬쳐등록 (아이디) (비번) / 컬쳐랜드 계정을 수정합니다.\n!수정 컬쳐아이디 / 컬쳐랜드 아이디를 수정합니다.\n!수정 컬쳐비번 / 컬쳐랜드 비밀번호를 수정합니다.\n!수정 웹훅이름 / 웹훅 이름을 수정합니다.\n!수정 웹훅프사 / 웹훅 프로필 사진을 수정합니다.\n!수정 익명여부 / 구매로그 익명 여부를 수정합니다.\n!수정 수수료 / 문화상품권 수수료를 수정합니다.\n!수정 구매로그웹훅 / 구매로그 웹훅을 수정합니다.\n!수정 관리자로그웹훅 / 관리자 로그 웹훅을 수정합니다.\n!수정 충전차단수 / 문화상품권 충전 정지 수를 수정합니다.\n!수정 색깔 / 버튼 및 임베드 색깔을 수정합니다.\n!수정 공지사항 / 공지사항을 수정합니다.\n!수정 최소금액 / 계좌이체 최소 충전 금액을 수정합니다.\n!수정 웹패널비번 / 웹패널 비밀번호를 수정합니다.\n!제품생성 / 제품을 생성합니다.\n!제품삭제 / 제품을 삭제합니다.\n!차단 (@유저) (숫자) / 유저의 계좌이체 차단 여부를 수정합니다.\n!경고수 (@유저) (숫자) / 누적 경고 수를 수정합니다.\n!구매메시지 / 임베드 출력과 함께 구매하기 버튼을 생성합니다.\n!바로가기 / 임베드 출력과 함께 지정한 링크 바로가기 버튼을 생성합니다.\n!임베드 / 임베드를 출력합니다.\n!디비출력 / 자판기 DB를 출력합니다.\n!초기화 문상 / 문화상품권 누적 충전 금액을 초기화합니다.\n!초기화 계좌 / 계좌이체 누적 충전 금액을 초기화합니다.\n!초기화 전체 / 총 누적 충전 금액을 초기화합니다.", color=0x5c6cdf))

    if message.content == '!버튼':
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                try:
                    await message.delete()
                except:
                    pass
                con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM serverinfo;", ())
                server_info = cur.fetchone()
                con.close()
                color = server_info[14]
                if color == "파랑":
                    embed = discord.Embed(title=f"{message.guild.name}", description='원하시는 버튼을 클릭해주세요.', color=0x5c6cdf)
                    await message.channel.send(
                        embed=embed,
                        components = [
                            ActionRow(
                                Button(style=ButtonStyle.blue,label = "공지",custom_id="공지"),
                                Button(style=ButtonStyle.blue,label = "제품",custom_id="제품"),
                                Button(style=ButtonStyle.blue,label = "충전",custom_id="충전"),
                                Button(style=ButtonStyle.blue,label = "정보",custom_id="정보"),
                                Button(style=ButtonStyle.blue,label = "구매",custom_id="구매"),
                            )
                        ]
                    )
                if color == "빨강":
                    embed = discord.Embed(title=f"{message.guild.name}", description='원하시는 버튼을 클릭해주세요.', color=0xff4848)
                    await message.channel.send(
                        embed=embed,
                        components = [
                            ActionRow(
                                Button(style=ButtonStyle.red,label = "공지",custom_id="공지"),
                                Button(style=ButtonStyle.red,label = "제품",custom_id="제품"),
                                Button(style=ButtonStyle.red,label = "충전",custom_id="충전"),
                                Button(style=ButtonStyle.red,label = "정보",custom_id="정보"),
                                Button(style=ButtonStyle.red,label = "구매",custom_id="구매"),
                            )
                        ]
                    )
                if color == "초록":
                    embed = discord.Embed(title=f"{message.guild.name}", description='원하시는 버튼을 클릭해주세요.', color=0x00ff27)
                    await message.channel.send(
                        embed=embed,
                        components = [
                            ActionRow(
                                Button(style=ButtonStyle.green,label = "공지",custom_id="공지"),
                                Button(style=ButtonStyle.green,label = "제품",custom_id="제품"),
                                Button(style=ButtonStyle.green,label = "충전",custom_id="충전"),
                                Button(style=ButtonStyle.green,label = "정보",custom_id="정보"),
                                Button(style=ButtonStyle.green,label = "구매",custom_id="구매"),
                            )
                        ]
                    )
                if color == "검정":
                    embed = discord.Embed(title=f"{message.guild.name}", description='원하시는 버튼을 클릭해주세요.', color=0x010101)
                    await message.channel.send(
                        embed=embed,
                        components = [
                            ActionRow(
                                Button(style=ButtonStyle.gray,label = "공지",custom_id="공지"),
                                Button(style=ButtonStyle.grey,label = "제품",custom_id="제품"),
                                Button(style=ButtonStyle.grey,label = "충전",custom_id="충전"),
                                Button(style=ButtonStyle.grey,label = "정보",custom_id="정보"),
                                Button(style=ButtonStyle.grey,label = "구매",custom_id="구매"),
                            )
                        ]
                    )
                if color == "회색":
                    embed = discord.Embed(title=f"{message.guild.name}", description='원하시는 버튼을 클릭해주세요.', color=0xd1d1d1)
                    await message.channel.send(
                        embed=embed,
                        components = [
                            ActionRow(
                                Button(style=ButtonStyle.gray,label = "공지",custom_id="공지"),
                                Button(style=ButtonStyle.grey,label = "제품",custom_id="제품"),
                                Button(style=ButtonStyle.grey,label = "충전",custom_id="충전"),
                                Button(style=ButtonStyle.grey,label = "정보",custom_id="정보"),
                                Button(style=ButtonStyle.grey,label = "구매",custom_id="구매"),
                            )
                        ]
                    )

    if message.content == '!라이센스':
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                embed = discord.Embed(title=bot_name, description='원하시는 버튼을 클릭해주세요.', color=0x5c6cdf)
                await message.channel.send(
                    embed=embed,
                    components = [
                        ActionRow(
                            Button(style=ButtonStyle.blue,label = "연장",custom_id="연장"),
                            Button(style=ButtonStyle.blue,label = "웹패널",custom_id="웹패널"),
                        )
                    ]
                )

    try:
        if not message.guild.id == 956683874472177724:
            if message.content.startswith("!수동충전 "):
                if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
                    try:
                        userId = message.mentions[0].id
                    except:
                        userId = int(message.content.split(" ")[1])
                    try:
                        amount = message.content.split(" ")[2]
                    except:
                        return await message.channel.send(embed=discord.Embed(title="수동 충전 실패", description="`!수동충전 (@유저) (금액)`으로 입력해주세요.", color=0xff0000))
                    if(int(amount) > 10000000):
                        await message.channel.send(embed=discord.Embed(title="수동 충전 실패", description="충전할 금액은 1000만원 이하로 입력해주세요.", color=0xff0000))
                        return
                    con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (userId,))
                    user_info = cur.fetchone()
                    if not user_info:
                        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (userId, 0, 0, 0, "일반", 0, 0, message.author.name, 0))
                        con.commit()
                        con.close()
                    current_money = int(user_info[1])
                    now_money = current_money + int(amount)
                    userName = message.content.split(" ")[1]
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (now_money, userId))
                    con.commit()
                    con.close()
                    con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM serverinfo;")
                    server_info = cur.fetchone()
                    con.close()
                    color = server_info[14]
                    if color == "파랑":
                        color = 0x5c6cdf
                    if color == "빨강":
                        color = 0xff4848
                    if color == "초록":
                        color = 0x00ff27
                    if color == "검정":
                        color = 0x010101
                    if color == "회색":
                        color = 0xd1d1d1
                    await message.channel.send(embed=discord.Embed(title="수동 충전 성공", description=f"관리자: {message.author.mention}\n유저: {userName}\n기존 금액: `{current_money}`\n충전한 금액: `{amount}`\n충전 후 금액: `{now_money}`원", color=color))
        else:
            if message.content.startswith(".수동충전 "):
                if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
                    try:
                        userId = message.mentions[0].id
                    except:
                        userId = int(message.content.split(" ")[1])
                    try:
                        amount = message.content.split(" ")[2]
                    except:
                        return await message.channel.send(embed=discord.Embed(title="수동 충전 실패", description="`.수동충전 (@유저) (금액)`으로 입력해주세요.", color=0xff0000))
                    if(int(amount) > 10000000):
                        await message.channel.send(embed=discord.Embed(title="수동 충전 실패", description="충전할 금액은 1000만원 이하로 입력해주세요.", color=0xff0000))
                        return
                    con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (userId,))
                    user_info = cur.fetchone()
                    if not user_info:
                        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (userId, 0, 0, 0, "일반", 0, 0, message.author.name, 0))
                        con.commit()
                        con.close()
                    current_money = int(user_info[1])
                    now_money = current_money + int(amount)
                    userName = message.content.split(" ")[1]
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (now_money, userId))
                    con.commit()
                    con.close()
                    con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM serverinfo;")
                    server_info = cur.fetchone()
                    con.close()
                    color = server_info[14]
                    if color == "파랑":
                        color = 0x5c6cdf
                    if color == "빨강":
                        color = 0xff4848
                    if color == "초록":
                        color = 0x00ff27
                    if color == "검정":
                        color = 0x010101
                    if color == "회색":
                        color = 0xd1d1d1
                    await message.channel.send(embed=discord.Embed(title="수동 충전 성공", description=f"관리자: {message.author.mention}\n유저: {userName}\n기존 금액: `{current_money}`\n충전한 금액: `{amount}`\n충전 후 금액: `{now_money}`원", color=color))
    except AttributeError:
        pass
    
    if message.content == "!도움말":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            await message.channel.send(embed=discord.Embed(title="도움말", description=f"서버 등록 : !등록 (구매한 라이센스)\n연장 : !라이센스 입력 후 연장 버튼 클릭\n웹패널 확인 : !라이센스 입력 후 웹패널 버튼 클릭\n수동 충전 : !수동충전 (@멘션) (금액)\n서버 이전 : !서버 이전 (서버 아이디) (웹패널 비밀번호)", color=0x5c6cdf))

    if message.content == "!set":
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("CREATE TABLE bankwait(day TEXT, user TEXT, id TEXT, name TEXT, amount INTEGER);")
                con.commit()
                con.close
                await message.channel.send("셋 완료")
    
@bot.event
async def on_button_click(interaction):
    if not isinstance(interaction.channel, discord.channel.DMChannel):
        if (os.path.isfile("../DB/" + str(interaction.guild.id) + ".db")):
            con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM serverinfo;")
            cmdchs = cur.fetchone()
            con.close()
            try:
                tempvar = is_expired(cmdchs[1])
            except:
                os.rename("../DB/" + str(interaction.guild.id) + ".db", "../DB/" + str(interaction.guild.id) + f".db_old{datetime.datetime.now()}")
            if not(is_expired(cmdchs[1])):
                if interaction.responded:
                    return
                try:
                    con = sqlite3.connect(f"../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                    user_info = cur.fetchone()
                    if (user_info == None):
                        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (interaction.user.id, 0, 0, 0, "일반", 0, 0, f"{interaction.user.name}#{interaction.author.discriminator}", 0))
                        con.commit()
                        con.close()
                except:
                    pass
                con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                user_info = cur.fetchone()
                cur.execute("SELECT * FROM serverinfo;")
                server_info = cur.fetchone()
                con.close()
                color = server_info[14]
                if color == "파랑":
                    color = 0x5c6cdf
                if color == "빨강":
                    color = 0xff4848
                if color == "초록":
                    color = 0x00ff27
                if color == "검정":
                    color = 0x010101
                if color == "회색":
                    color = 0xd1d1d1
                webhook_profile_url = server_info[21]
                webhook_name = server_info[22]
                if interaction.custom_id == "제품":
                    con = sqlite3.connect(f"../DB/{interaction.guild.id}.db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM products;")
                    products = cur.fetchall()
                    con.close()
                    br = "\n"
                    list_embed = discord.Embed(title="제품 목록", color=color)
                    for product in products:
                        list_embed.add_field(inline=False, name=product[0], value=f"{str(len(product[2].split(br))) if product[2] != '' else '0'}개, {str(product[1])}원")

                    await interaction.respond(embed=list_embed)
                if interaction.custom_id == "충전":
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                    user_info = cur.fetchone()
                    con.commit()
                    con.close()
                    if color == 0x5c6cdf:
                        embed = discord.Embed(title='충전 수단 선택', description='원하시는 충전 수단을 클릭해주세요.', color=color)
                        await interaction.respond(
                            embed=embed,
                            components = [
                                ActionRow(
                                    Button(style=ButtonStyle.blue,label = "문화상품권",custom_id="문상충전"),
                                    Button(style=ButtonStyle.blue,label = "계좌이체",custom_id="계좌충전"),
                                )
                            ]
                        )
                    if color == 0xff4848:
                        embed = discord.Embed(title='충전 수단 선택', description='원하시는 충전 수단을 클릭해주세요.', color=color)
                        await interaction.respond(
                            embed=embed,
                            components = [
                                ActionRow(
                                    Button(style=ButtonStyle.red,label = "문화상품권",custom_id="문상충전"),
                                    Button(style=ButtonStyle.red,label = "계좌이체",custom_id="계좌충전"),
                                )
                            ]
                        )
                    if color == 0x00ff27:
                        embed = discord.Embed(title='충전 수단 선택', description='원하시는 충전 수단을 클릭해주세요.', color=color)
                        await interaction.respond(
                            embed=embed,
                            components = [
                                ActionRow(
                                    Button(style=ButtonStyle.green,label = "문화상품권",custom_id="문상충전"),
                                    Button(style=ButtonStyle.green,label = "계좌이체",custom_id="계좌충전"),
                                )
                            ]
                        )
                    if color == 0x5c6cdf:
                        embed = discord.Embed(title='충전 수단 선택', description='원하시는 충전 수단을 클릭해주세요.', color=color)
                        await interaction.respond(
                            embed=embed,
                            components = [
                                ActionRow(
                                    Button(style=ButtonStyle.grey,label = "문화상품권",custom_id="문상충전"),
                                    Button(style=ButtonStyle.grey,label = "계좌이체",custom_id="계좌충전"),
                                )
                            ]
                        )
                    if color == 0x010101:
                        embed = discord.Embed(title='충전 수단 선택', description='원하시는 충전 수단을 클릭해주세요.', color=color)
                        await interaction.respond(
                            embed=embed,
                            components = [
                                ActionRow(
                                    Button(style=ButtonStyle.grey,label = "문화상품권",custom_id="문상충전"),
                                    Button(style=ButtonStyle.grey,label = "계좌이체",custom_id="계좌충전"),
                                )
                            ]
                        )
                    if color == 0xd1d1d1:
                        embed = discord.Embed(title='충전 수단 선택', description='원하시는 충전 수단을 클릭해주세요.', color=color)
                        await interaction.respond(
                            embed=embed,
                            components = [
                                ActionRow(
                                    Button(style=ButtonStyle.grey,label = "문화상품권",custom_id="문상충전"),
                                    Button(style=ButtonStyle.grey,label = "계좌이체",custom_id="계좌충전"),
                                )
                            ]
                        )
                    
                if interaction.custom_id == "문상충전":
                    global charginguser
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                    user_info = cur.fetchone()
                    con.close()
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM serverinfo;")
                    server_info = cur.fetchone()
                    con.close()
                    if (server_info[2] != "" and server_info[3] != ""):
                        if not int(user_info[3]) >= int(server_info[15]):
                            if not interaction.user.id in charginguser:
                                charginguser.append(interaction.user.id)
                                try:
                                    await interaction.user.send(embed=discord.Embed(title="문화상품권 충전", description=f"문화상품권 핀번호를 `-`를 포함해서 입력해주세요.\n문화상품권 충전 수수료: {server_info[8]}%", color=color))
                                    await interaction.respond(embed=discord.Embed(title="전송 성공", description="DM을 확인해주세요.", color=color))
                                except:
                                    await interaction.respond(embed=discord.Embed(title="문화상품권 충전 실패", description="DM을 차단하셨거나 메시지 전송 권한이 없습니다.", color=color))
                                    chargingusers = []
                                    for user in charginguser:
                                        if user != interaction.user.id:
                                            chargingusers.append(user)
                                    charginguser = chargingusers
                                    return None

                                def check(msg):
                                    return (isinstance(msg.channel, discord.channel.DMChannel) and (len(msg.content) == 21 or len(msg.content) == 19) and (interaction.user.id == msg.author.id))
                                try:
                                    msg = await bot.wait_for("message", timeout=60, check=check)
                                except asyncio.TimeoutError:
                                    try:
                                        await interaction.user.send(embed=discord.Embed(title="문화상품권 충전 실패", description="시간이 초과되었습니다.", color=color))
                                        chargingusers = []
                                        for user in charginguser:
                                            if user != interaction.user.id:
                                                chargingusers.append(user)
                                        charginguser = chargingusers
                                    except:
                                        pass
                                    return None
                                
                                try:
                                    jsondata = {"token" : setting.api_token, "id" : server_info[2], "pw" : server_info[3], "pin" : msg.content}
                                    res = requests.post(setting.api, json=jsondata)
                                    if (res.status_code != 200):
                                        raise TypeError
                                    else:
                                        print(str(res))
                                        res = res.json()
                                except:
                                    try:
                                        await interaction.user.send(embed=discord.Embed(title="문화상품권 충전 실패", description="일시적인 서버 오류입니다.\n잠시 후 다시 시도해주세요.", color=color))
                                        chargingusers = []
                                        for user in charginguser:
                                            if user != interaction.user.id:
                                                chargingusers.append(user)
                                        charginguser = chargingusers
                                    except:
                                        pass
                                    return None

                                if (res["result"] == True):
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM serverinfo WHERE id == ?;",(interaction.guild.id,))
                                    guild_info = cur.fetchone()
                                    culture_fee = int(guild_info[8])
                                    culture_amount = int(res["amount"])
                                    culture_amount_after_fee = culture_amount - int(culture_amount*(culture_fee/100))
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (msg.author.id,))
                                    user_info = cur.fetchone()
                                    current_money = int(user_info[1])
                                    now_money = current_money + culture_amount_after_fee
                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (now_money, msg.author.id))
                                    con.commit()
                                    con.close()
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("UPDATE serverinfo SET mm = ?", (int(server_info[27]) + int(culture_amount),))
                                    con.commit()
                                    cur.execute("UPDATE serverinfo SET totalm = ?", (int(server_info[28]) + int(culture_amount),))
                                    con.commit()
                                    con.close()
                                    try:
                                        chargingusers = []
                                        for user in charginguser:
                                            if user != interaction.user.id:
                                                chargingusers.append(user)
                                        charginguser = chargingusers
                                        await interaction.user.send(embed=discord.Embed(title="문화상품권 충전 성공", description=f"핀 코드: {msg.content}\n금액: {culture_amount}원\n충전한 금액: {culture_amount_after_fee} (수수료 {culture_fee}%)\n충전 후 금액: {now_money}원", color=color))

                                        con = sqlite3.connect(f"../DB/charge_log.db")
                                        cur = con.cursor()
                                        cur.execute("INSERT INTO log VALUES(?, ?, ?, ?, ?, ?);", (
                                            interaction.guild.id, "문화상품권", f"{interaction.author.id}", int(culture_amount),
                                            now_time(),
                                            f"{interaction.author.name}#{interaction.author.discriminator}"))
                                        con.commit()
                                        con.close()

                                        try:
                                            webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                            eb = DiscordEmbed(title='문화상품권 충전 성공', description=f'[웹패널로 이동하기]({domain})', color=color)
                                            eb.add_embed_field(name='디스코드 닉네임', value=f"{msg.author}", inline=False)
                                            eb.add_embed_field(name='핀 코드', value=f"{msg.content}", inline=False)
                                            eb.add_embed_field(name='상품권 금액', value=f"`{culture_amount}`원", inline=False)
                                            eb.add_embed_field(name='충전한 금액', value=f"`{culture_amount_after_fee}`원 (수수료 {culture_fee}%)", inline=False)
                                            webhook.add_embed(eb)
                                            webhook.execute()
                                        except:
                                            pass
                                    except:
                                        pass
                                else:
                                    try:
                                        if (res["result"] == False):
                                            reason = res["reason"]
                                            con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                            cur = con.cursor()
                                            cur.execute("UPDATE users SET warnings = ? WHERE id == ?;", (user_info[3] + 1, msg.author.id))
                                            con.commit()
                                            con.close()
                                            chargingusers = []
                                        for user in charginguser:
                                            if user != interaction.user.id:
                                                chargingusers.append(user)
                                        charginguser = chargingusers
                                        await interaction.user.send(embed=discord.Embed(title="문화상품권 충전 실패", description=f"**핀 코드**\n{msg.content}\n**실패 사유**\n{reason}\n**날짜**\n{nowstr()}", color=color))
                                        try:
                                            webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                            eb = DiscordEmbed(title='문화상품권 충전 실패', description=f'[웹패널로 이동하기]({domain})', color=color)
                                            eb.add_embed_field(name='디스코드 닉네임', value=str(msg.author), inline=False)
                                            eb.add_embed_field(name='핀 코드', value=str(msg.content), inline=False)
                                            eb.add_embed_field(name='실패 사유', value=res["reason"], inline=False)
                                            webhook.add_embed(eb)
                                            webhook.execute()
                                        except Exception as e:
                                            pass
                                    except:
                                        pass
                            else:
                                await interaction.respond(embed=discord.Embed(title="문화상품권 충전 실패", description="이미 충전이 진행중입니다.", color=color))
                        else:
                            await interaction.respond(embed=discord.Embed(title="문화상품권 충전 실패", description=f"{server_info[15]}회 충전 실패로 충전이 정지되었습니다.\n샵 관리자에게 문의해주세요.", color=color))
                    else:
                        await interaction.respond(embed=discord.Embed(title="문화상품권 충전 실패", description="충전 기능이 비활성화되어 있습니다.\n샵 관리자에게 문의해주세요.", color=color))

                if interaction.custom_id == "계좌충전":
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                    user_info = cur.fetchone()
                    con.close()
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM serverinfo;")
                    serverinfo = cur.fetchone()
                    con.close()
                    try:
                        bankdata = json.loads(serverinfo[9])
                        assert len(bankdata['banknum']) > 1
                    except Exception as e:
                        await interaction.respond(embed=discord.Embed(title="계좌 정보 불러오기 실패", description="서버에 계좌 정보가 등록되어 있지 않습니다.\n샵 관리자에게 문의해주세요.", color=color))
                        return
                    if not interaction.user.id in bankchanginguser:
                        bankchanginguser.append(interaction.user.id)
                        if not int(user_info[8]) == 1:
                            try:
                                nam = await interaction.user.send(embed=discord.Embed(title="계좌 충전", description=f"입금자명을 입력해주세요.", color=color))
                                await interaction.respond(embed=discord.Embed(title="전송 성공", description="DM을 확인해주세요.", color=color))
                                def check(name):
                                    return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))
                                try:
                                    name = await bot.wait_for("message", timeout=60, check=check)
                                    await nam.delete()
                                    name = name.content
                                except asyncio.TimeoutError:
                                    try:
                                        await interaction.user.send(embed=discord.Embed(title="계좌 충전 실패", description="시간이 초과되었습니다.", color=color))
                                    except:
                                        pass
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("DELETE FROM bankwait WHERE id == ?;", (interaction.user.id,))
                                    con.commit()
                                    con.close()
                                    bankchanginguser.remove(interaction.user.id)
                                    return None
                                mone = await interaction.user.send(embed=discord.Embed(title="계좌 충전", description=f"입금하실 금액을 입력해주세요.", color=color))
                                def check(money):
                                    return (isinstance(money.channel, discord.channel.DMChannel) and (interaction.user.id == money.author.id))
                                try:
                                    money = await bot.wait_for("message", timeout=60, check=check)
                                    await mone.delete()
                                    money = money.content
                                    least = serverinfo[25]
                                    if int(money) < int(serverinfo[25]):
                                        try:
                                            con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                            cur = con.cursor()
                                            cur.execute("DELETE FROM bankwait WHERE id == ?;", (interaction.user.id,))
                                            con.commit()
                                            con.close()
                                            bankchanginguser.remove(interaction.user.id)
                                            return await interaction.user.send(embed=discord.Embed(title="계좌 충전 실패", description=f"최소 충전 금액은 {least}원 입니다.", color=color))
                                        except:
                                            pass
                                except asyncio.TimeoutError:
                                    try:
                                        await interaction.user.send(embed=discord.Embed(title="계좌 충전 실패", description="시간이 초과되었습니다.", color=color))
                                    except:
                                        pass
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("DELETE FROM bankwait WHERE id == ?;", (interaction.user.id,))
                                    con.commit()
                                    con.close()
                                    bankchanginguser.remove(interaction.user.id)
                                    return None
                                if money.isdigit():
                                    await interaction.user.send(embed=discord.Embed(title="계좌 충전", description=f"은행명 : **{bankdata.get('bankname')}**\n계좌번호 : **{bankdata.get('banknum')}**\n예금주명 : **{bankdata.get('bankowner')}**\n입금자명 : **{name}**\n입금 금액 : **{money}**원", color=color))
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("INSERT INTO bankwait VALUES(?, ?, ?, ?, ?);", (nowstr(), str(interaction.user), interaction.user.id, name, money))
                                    con.commit()
                                    con.close()
                                    bankchanginguser.remove(interaction.user.id)
                                else:
                                    await interaction.user.send(embed=discord.Embed(title="계좌 충전 실패", description=f"올바른 액수를 입력해주세요.", color=color))
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("DELETE FROM bankwait WHERE id == ?;", (interaction.user.id,))
                                    con.commit()
                                    con.close()
                                    bankchanginguser.remove(interaction.user.id)
                                    return
                            except Exception as e:
                                print(e)
                                con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                cur = con.cursor()
                                cur.execute("DELETE FROM bankwait WHERE id == ?;", (interaction.user.id,))
                                con.commit()
                                con.close()
                                return await interaction.respond(embed=discord.Embed(title="계좌 충전 실패", description="DM을 차단하셨거나 메시지 전송 권한이 없습니다.", color=color))
                                bankchanginguser.remove(interaction.user.id)
                            try:
                                if money.isdigit():
                                    webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                    eb = DiscordEmbed(title='계좌이체 충전 요청', description=f'[웹패널로 이동하기]({domain})', color=color)
                                    eb.add_embed_field(name='디스코드 닉네임', value=f"<@{interaction.user.id}>({interaction.user})", inline=False)
                                    eb.add_embed_field(name='입금자명', value=f"{name}", inline=False)
                                    eb.add_embed_field(name='입금 금액', value=f"{money}원", inline=False)
                                    eb.add_embed_field(name='입금 확인 후 충전 방법', value=f"!수동충전 <@{interaction.user.id}> {money}", inline=False)
                                    webhook.add_embed(eb)
                                    webhook.execute()
                            except:
                                pass
                        
                            async def waiting():
                                jsondata = {
                                    "api_key" : setting.api2_token, "bankpin" : f"{bankdata.get('bankpw')}", "shop": interaction.guild.id, "userinfo" : name, "userid" : interaction.user.id, "token" : "token", "type" : True, "amount": int(money)
                                }
                                loop = asyncio.get_event_loop()
                                bound = partial(
                                requests.post, setting.api2, json=jsondata)
                                ms_result = await loop.run_in_executor(None, bound)
                                print(ms_result)
                                if ms_result.status_code != 200:
                                    raise TypeError
                                ms_result = ms_result.json()
                                print(ms_result)

                                if ms_result["result"] == False:
                                    reason = ms_result["reason"]
                                    await interaction.user.send(embed=discord.Embed(title="계좌 충전 실패", description=f"**입금자명**\n{name}\n**입금금액**\n{money}\n**실패 사유**\n{reason}", color=color))
                                    try:
                                        webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                        eb = DiscordEmbed(title='계좌이체 충전 실패', description=f'[웹패널로 이동하기]({domain})', color=color)
                                        eb.add_embed_field(name='디스코드 닉네임', value=f"<@{interaction.user.id}>({interaction.user})", inline=False)
                                        eb.add_embed_field(name='입금자명', value=f"{name}", inline=False)
                                        eb.add_embed_field(name='입금 금액', value=f"{money}원", inline=False)
                                        eb.add_embed_field(name='실패 사유', value=f"{reason}", inline=False)
                                        webhook.add_embed(eb)
                                        webhook.execute()
                                    except:
                                        pass
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("DELETE FROM bankwait WHERE id == ?;", (interaction.user.id,))
                                    con.commit()
                                    con.close()
                                    bankchanginguser.remove(interaction.user.id)
                                    return

                                if ms_result["result"] == True:
                                    userId = interaction.user.id
                                    amount = int(ms_result["count"])
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (userId,))
                                    user_info = cur.fetchone()
                                    current_money = int(user_info[1])
                                    now_money = current_money + int(amount)
                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (now_money, userId))
                                    con.commit()
                                    con.close()
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("UPDATE serverinfo SET mm = ?", (int(server_info[26]) + int(money),))
                                    con.commit()
                                    cur.execute("UPDATE serverinfo SET totalm = ?", (int(server_info[28]) + int(money),))
                                    con.commit()
                                    con.close()
                                    await interaction.user.send(embed=discord.Embed(title="계좌 충전 성공", description=f"{amount}원 충전되었습니다. ", color=color))

                                    con = sqlite3.connect(f"../DB/charge_log.db")
                                    cur = con.cursor()
                                    cur.execute("INSERT INTO log VALUES(?, ?, ?, ?, ?, ?);", (
                                    interaction.guild.id, "계좌이체", f"{interaction.author.id}", int(money), now_time(),
                                        f"{interaction.author.name}#{interaction.author.discriminator}"))
                                    con.commit()
                                    con.close()

                                    try:
                                        webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                        eb = DiscordEmbed(title='계좌이체 충전 성공', description=f'[웹패널로 이동하기]({domain})', color=color)
                                        eb.add_embed_field(name='디스코드 닉네임', value=f"<@{interaction.user.id}>({interaction.user})", inline=False)
                                        eb.add_embed_field(name='입금자명', value=f"{name}", inline=False)
                                        eb.add_embed_field(name='입금 금액', value=f"{money}원", inline=False)
                                        eb.add_embed_field(name='충전 성공 금액', value=f"{money}원", inline=False)
                                        webhook.add_embed(eb)
                                        webhook.execute()
                                    except:
                                        pass
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("DELETE FROM bankwait WHERE id == ?;", (interaction.user.id,))
                                    con.commit()
                                    con.close()
                                    bankchanginguser.remove(interaction.user.id)

                            futures = [asyncio.ensure_future(waiting())]

                            await asyncio.gather(*futures)
                            try:
                                con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                cur = con.cursor()
                                cur.execute("DELETE FROM bankwait WHERE id == ?;", (interaction.user.id,))
                                con.commit()
                                con.close()
                                bankchanginguser.remove(interaction.user.id)
                            except:
                                pass
                            #await interaction.user.send(embed=discord.Embed(title="계좌 충전 실패", description="계좌 비밀번호가 잘못되었습니다.", color=color))
                        else:
                            await interaction.respond(embed=discord.Embed(title="계좌 충전 실패", description="계좌 충전이 차단되었습니다.", color=color))
                            bankchanginguser.remove(interaction.user.id)
                    else:
                        await interaction.respond(embed=discord.Embed(title="계좌 충전 실패", description="이미 계좌 충전을 진행중입니다.", color=color))
                    
                if interaction.custom_id == "구매":
                    global buyinguser
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM products;")
                    products = cur.fetchall()
                    options = []
                    if not interaction.user.id in buyinguser:
                        try:
                            buyinguser.append(interaction.user.id)
                            for product in products:
                                if user_info[4] == "일반":
                                    rank = server_info[10]
                                if user_info[4] == "VIP":
                                    rank = server_info[11]
                                if user_info[4] == "VVIP":
                                    rank = server_info[12]
                                if user_info[4] == "리셀러":
                                    rank = server_info[13]
                                options.append(SelectOption(description=str(product[1] - product[1] * rank/100).split(".")[0]+"원ㅣ재고 "+str(len(product[2].split('\n')))+"개" if product[2] != '' else '0'+"개 | 재고가 부족합니다.", label=product[0], value=product[0]))
                            gg = await interaction.user.send(embed=discord.Embed(title='제품 선택', description='구매할 제품을 선택해주세요.', color=color)
                                ,
                                components = [
                                    [Select(placeholder="구매하기", options=options)]
                                ]
                            )
                            await interaction.respond(embed=discord.Embed(title="전송 성공", description="DM을 확인해주세요.", color=color))
                        except:
                            buyingusers = []
                            for user in buyinguser:
                                if user != interaction.user.id:
                                    buyingusers.append(user)
                            buyinguser = buyingusers
                            await interaction.respond(embed=discord.Embed(title="전송 실패", description="DM을 차단하셨거나 제품이 없습니다.", color=color))
                            return
                        try:
                            event = await bot.wait_for("select_option", timeout=30, check=None)
                            product_name = event.values[0]
                            await gg.delete()
                        except asyncio.TimeoutError:
                            buyingusers = []
                            for user in buyinguser:
                                if user != interaction.user.id:
                                    buyingusers.append(user)
                            buyinguser = buyingusers
                            await gg.delete()
                            await interaction.user.send(embed=discord.Embed(title='구매 실패', description='시간 초과', color=color))
                            return
                        cur.execute("SELECT * FROM products WHERE name = ?;", (str(product_name),))
                        product_info = cur.fetchone()
                        if (product_info != None):
                            if (str(product_info[2]) != ""):
                                info_msg = await interaction.user.send(embed=discord.Embed(title="수량 선택", description="구매하실 수량을 숫자만 입력해주세요.", color=color))
                                def check(msg):
                                    return (msg.author.id == interaction.user.id)
                                try:
                                    msg = await bot.wait_for("message", timeout=20, check=check)
                                except asyncio.TimeoutError:
                                    try:
                                        await info_msg.delete()
                                    except:
                                        pass
                                    buyingusers = []
                                    for user in buyinguser:
                                        if user != interaction.user.id:
                                            buyingusers.append(user)
                                    buyinguser = buyingusers
                                    await interaction.user.send(embed=discord.Embed(title="시간 초과", description="처음부터 다시 시도해주세요.", color=color))
                                    return None

                                try:
                                    await info_msg.delete()
                                except:
                                    pass
                                try:
                                    await msg.delete()
                                except:
                                    pass
                                
                                if not msg.content.isdigit() or int(msg.content) == 0:
                                    buyingusers = []
                                    for user in buyinguser:
                                        if user != interaction.user.id:
                                            buyingusers.append(user)
                                    buyinguser = buyingusers
                                    await interaction.user.send(embed=discord.Embed(title="구매 실패", description="수량은 숫자로만 입력해주세요.", color=color))
                                    return None

                                buy_amount = int(msg.content)

                                if (len(product_info[2].split("\n")) >= buy_amount):
                                    if user_info[4] == "일반":
                                        rank = server_info[10]
                                    if user_info[4] == "VIP":
                                        rank = server_info[11]
                                    if user_info[4] == "VVIP":
                                        rank = server_info[12]
                                    if user_info[4] == "리셀러":
                                        rank = server_info[13]
                                    off_amount = product_info[1] * buy_amount * rank/100
                                    buy_money = int(str(product_info[1] * buy_amount - off_amount).split(".")[0])
                                    if (int(user_info[1]) >= product_info[1] * buy_amount - off_amount):
                                        try_msg = await interaction.user.send(embed=discord.Embed(title="구매 진행 중입니다..", color=color))
                                        stocks = product_info[2].split("\n")
                                        bought_stock = []
                                        for n in range(buy_amount):
                                            picked = random.choice(stocks)
                                            bought_stock.append(picked)
                                            stocks.remove(picked)
                                        now_stock = "\n".join(stocks)
                                        now_money = int(user_info[1]) - buy_money
                                        now_bought = int(user_info[2]) + buy_money
                                        con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                        cur = con.cursor()
                                        cur.execute("UPDATE users SET money = ?, bought = ? WHERE id == ?;", (now_money, now_bought, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE products SET stock = ? WHERE name == ?;", (now_stock, product_name))
                                        con.commit()
                                        con.close()
                                        bought_stock = "\n".join(bought_stock)
                                        con = sqlite3.connect("../DB/docs.db")
                                        cur = con.cursor()
                                        docs_name = randomstring.pick(30)
                                        cur.execute("INSERT INTO docs VALUES(?, ?);", (docs_name, bought_stock))
                                        con.commit()
                                        con.close()
                                        docs_url = f"{domain}product/" + docs_name
                                        try:
                                            try:
                                                webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                                eb = DiscordEmbed(title='제품 구매 로그', description=f'[웹패널로 이동하기]({domain})', color=color)
                                                eb.add_embed_field(name='디스코드 닉네임', value=f"<@{interaction.user.id}>({interaction.user})", inline=False)
                                                eb.add_embed_field(name='제품 이름', value=str(product_name), inline=False)
                                                eb.add_embed_field(name='제품 코드', value='[구매한 제품 보기](' + docs_url + ')', inline=False)
                                                webhook.add_embed(eb)
                                                webhook.execute()
                                            except:
                                                pass

                                            try:
                                                con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                                cur = con.cursor()
                                                cur.execute(f"SELECT * FROM products WHERE name == '{product_name}';")
                                                img_result = cur.fetchone()
                                                con.close()
                                                if img_result[3] != "":
                                                    webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_buylogwebhk(interaction.guild.id))
                                                    if server_info[18] == "Y":
                                                        eb = DiscordEmbed(title="`💵 구매로그`", description="`익명님, " + product_name + " " + str(buy_amount) + "개 구매 감사합니다! 💝`", color=color)
                                                        eb.set_footer(text="KA Button", icon_url="https://cdn.discordapp.com/attachments/881113697110609920/924248976616734760/KA-----.gif")
                                                        eb.set_thumbnail(url=img_result[3])
                                                        eb.set_timestamp()
                                                        webhook.add_embed(eb)
                                                    else:
                                                        eb = DiscordEmbed(title="`💵 구매로그`", description="<@" + str(interaction.user.id) + ">" + "`님, " + product_name + " " + str(buy_amount) + "개 구매 감사합니다! 💝`", color=color)
                                                        eb.set_footer(text="KA Button", icon_url="https://cdn.discordapp.com/attachments/881113697110609920/924248976616734760/KA-----.gif")
                                                        eb.set_thumbnail(url=img_result[3])
                                                        eb.set_timestamp()
                                                        webhook.add_embed(eb)
                                                    webhook.execute()
                                                else:
                                                    webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_buylogwebhk(interaction.guild.id))
                                                    if server_info[18] == "Y":
                                                        eb = DiscordEmbed(title="`💵 구매로그`", description="`익명님, " + product_name + " " + str(buy_amount) + "개 구매 감사합니다! 💝`", color=color)
                                                        eb.set_footer(text="KA Button", icon_url="https://cdn.discordapp.com/attachments/881113697110609920/924248976616734760/KA-----.gif")
                                                        eb.set_timestamp()
                                                        webhook.add_embed(eb)
                                                    else:
                                                        eb = DiscordEmbed(title="`💵 구매로그`", description="<@" + str(interaction.user.id) + ">" + "`님, " + product_name + " " + str(buy_amount) + "개 구매 감사합니다! 💝`", color=color)
                                                        eb.set_footer(text="KA Button", icon_url="https://cdn.discordapp.com/attachments/881113697110609920/924248976616734760/KA-----.gif")
                                                        eb.set_timestamp()
                                                        webhook.add_embed(eb)
                                                    webhook.execute()
                                            except Exception as e:
                                                print(e)
                                                pass
                                            try:
                                                buyer_role = interaction.guild.get_role(get_roleid(interaction.guild.id))
                                                await interaction.user.add_roles(buyer_role)
                                            except:
                                                pass
                                            await try_msg.delete()
                                            buyingusers = []
                                            for user in buyinguser:
                                                if user != interaction.user.id:
                                                    buyingusers.append(user)
                                                    buyinguser = buyingusers
                                            buyinguser = buyingusers
                                            con = sqlite3.connect("../DB/buy_log.db")
                                            cur = con.cursor()
                                            cur.execute("INSERT INTO log VALUES(?, ?, ?, ?, ?, ?)", (
                                                interaction.guild.id, product_name, f"{interaction.user.id}",
                                                f"{interaction.user.name}#{interaction.user.discriminator}", buy_amount, now_time()))
                                            con.commit()
                                            con.close()
                                            await interaction.user.send(embed=discord.Embed(title="구매 성공", description=f"제품 이름 : {product_name}\n구매 개수 : {buy_amount} 개\n차감 금액 : {buy_money}원", color=color),
                                            components = [
                                                    ActionRow(
                                                        Button(style=ButtonType().Link,label = "구매 제품 보기",url=docs_url),
                                                    )
                                                ]
                                            )
                                            con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                            cur = con.cursor()
                                            cur.execute("UPDATE users SET buycount = ? WHERE id == ?;", (user_info[5] + 1, msg.author.id))
                                            con.commit()
                                            con.close()
                                            if now_bought >= server_info[16]:
                                                con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                                cur = con.cursor()
                                                cur.execute("UPDATE users SET rank = ? WHERE id == ?;", ("VIP", msg.author.id))
                                                con.commit()
                                                con.close()
                                                vip_role = interaction.guild.get_role(server_info[19])
                                                await interaction.user.add_roles(vip_role)
                                            if now_bought >= server_info[17]:
                                                con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                                cur = con.cursor()
                                                cur.execute("UPDATE users SET rank = ? WHERE id == ?;", ("VVIP", msg.author.id))
                                                con.commit()
                                                con.close()
                                                vvip_role = interaction.guild.get_role(server_info[20])
                                                await interaction.user.add_roles(vvip_role)


                                        except:
                                            try:
                                                await try_msg.delete()
                                            except:
                                                buyingusers = []
                                                for user in buyinguser:
                                                    if user != interaction.user.id:
                                                        buyingusers.append(user)
                                                buyinguser = buyingusers
                                                await interaction.user.send(embed=discord.Embed(title="제품 구매 실패", description="제품 구매 중 알 수 없는 오류가 발생했습니다.\n샵 관리자에게 문의해주세요.", color=color))
                                                buyinguser.remove(interaction.user.id)
                                    else:
                                        buyingusers = []
                                        for user in buyinguser:
                                            if user != interaction.user.id:
                                                buyingusers.append(user)
                                        buyinguser = buyingusers
                                        await interaction.user.send(embed=discord.Embed(title="제품 구매 실패", description="잔액이 부족합니다.", color=color))
                                        buyinguser.remove(interaction.user.id)
                                else:
                                    buyingusers = []
                                    for user in buyinguser:
                                        if user != interaction.user.id:
                                            buyingusers.append(user)
                                    buyinguser = buyingusers
                                    await interaction.user.send(embed=discord.Embed(title="제품 구매 실패", description="재고가 부족합니다.", color=color))
                                    if interaction.user.id in buyinguser:
                                        buyinguser.remove(interaction.user.id)
                                    else:
                                        pass
                                    
                            else:
                                buyingusers = []
                                for user in buyinguser:
                                    if user != interaction.user.id:
                                        buyingusers.append(user)
                                        buyinguser = buyingusers
                                    await interaction.user.send(embed=discord.Embed(title="제품 구매 실패", description="재고가 부족합니다.", color=color))
                                    if interaction.user.id in buyinguser:
                                        buyinguser.remove(interaction.user.id)
                                    else:
                                        pass
                                
                                
                    else:
                        await interaction.respond(embed=discord.Embed(title="구매 실패", description="이미 구매가 진행중입니다.", color=color))
                        if interaction.user.id in buyinguser:
                            buyinguser.remove(interaction.user.id)
                        else:
                            pass

                if interaction.custom_id == "정보":
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.author.id,))
                    user_info = cur.fetchone()
                    con.close()
                    if user_info[4] == "일반":
                        rank = server_info[10]
                    if user_info[4] == "VIP":
                        rank = server_info[11]
                    if user_info[4] == "VVIP":
                        rank = server_info[12]
                    if user_info[4] == "리셀러":
                        rank = server_info[13]
                    await interaction.respond(embed=discord.Embed(title=str(interaction.user.name) + "님의 정보", description="닉네임 : " + str(interaction.user.name) + "\n보유 금액 : " + str(user_info[1]) + "원\n누적 금액 : " + str(user_info[2]) + f"원\n등급 : {user_info[4]}\n할인율 : {rank}%\n구매 수 : {user_info[5]}회\n경고 수 : {user_info[3]}회", color=color))

                if interaction.custom_id == "공지":
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM serverinfo WHERE id == ?;",(interaction.guild.id,))
                    server_info = cur.fetchone()
                    con.close
                    await interaction.respond(embed=discord.Embed(title="공지사항", description=server_info[23], color=color))

                if interaction.custom_id == "연장":
                    if interaction.user.guild_permissions.administrator or interaction.author.id == int(admin_id):
                        await interaction.user.send(embed=discord.Embed(description="라이센스를 입력해주세요.", color=color))
                        await interaction.respond(embed=discord.Embed(title="전송 성공", description="DM을 확인해주세요.", color=color))
                        def check(license_key):
                            return (license_key.author.id == interaction.user.id and isinstance(license_key.channel, discord.channel.DMChannel))
                        license_key = await bot.wait_for("message", timeout=30, check=check)
                        license_key = license_key.content
                        con = sqlite3.connect("../DB/" + "license.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
                        search_result = cur.fetchone()
                        con.close()
                        if (search_result != None):
                            if (search_result[2] == 0):
                                con = sqlite3.connect("../DB/" + "license.db")
                                cur = con.cursor()
                                cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;", (1, nowstr(), str(interaction.guild.id), license_key))
                                con.commit()
                                cur = con.cursor()
                                cur.execute("SELECT * FROM license WHERE code == ?;",(license_key,))
                                key_info = cur.fetchone()
                                con.close()
                                con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM serverinfo;")
                                server_info = cur.fetchone()
                                if (is_expired(server_info[1])):
                                    new_expiretime = make_expiretime(key_info[1])
                                else:
                                    new_expiretime = add_time(server_info[1], key_info[1])
                                cur.execute("UPDATE serverinfo SET expiredate = ?;", (new_expiretime,))
                                con.commit()
                                con.close()
                                await interaction.user.send(embed=discord.Embed(description=f"`{key_info[1]}`일 연장되었습니다.", color=color))
                                webhook = DiscordWebhook(username="KA Button", avatar_url="https://cdn.discordapp.com/attachments/783489649985060904/937736166961184768/KA_Vending.png", url="https://canary.discord.com/api/webhooks/969682032147984435/on3GYsITrPtUAzT8f5nAcCb-7TQhUbLgVWganKib-Cgskt9qcaL6Xnftp0fIeiFQcXSq")
                                eb = DiscordEmbed(title='서버 연장 로그', description=f'```유저 : {interaction.author.name}#{interaction.author.discriminator} ({interaction.author.id})\n서버 이름 : {interaction.guild.name}\n서버 아이디 : {interaction.guild.id}\n기간 : {key_info[1]} 일\n라이센스 : {license_key}```', color=0x5c6cdf)
                                webhook.add_embed(eb)
                                webhook.execute()
                                con.close()
                            else:
                                await interaction.user.send(embed=discord.Embed(description="이미 사용된 라이센스입니다.", color=color))
                        else:
                            await interaction.user.send(embed=discord.Embed(description="존재하지 않는 라이센스입니다.", color=color))

                if interaction.custom_id == "웹패널":
                    if interaction.user.guild_permissions.administrator or interaction.author.id == int(admin_id):
                        con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM serverinfo;")
                        server_info = cur.fetchone()
                        await interaction.respond(embed=discord.Embed(title="웹패널 정보", description="만료일: `" + server_info[1] + f"`\n웹패널: {domain}\n아이디: `" +str(interaction.guild.id) + "`\n비밀번호: `" + server_info[4] + "`", color=color))

                if interaction.custom_id == "디비백업":
                    if interaction.user.guild_permissions.administrator or interaction.author.id == int(admin_id):
                        await interaction.send(file=discord.File("../DB/" + str(interaction.guild.id) + ".db"))

bot.run(setting.token)
