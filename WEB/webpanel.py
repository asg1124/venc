from logging import log
from flask import Flask, render_template, request, make_response
from flask import session, redirect, url_for, abort
from datetime import timedelta
import datetime
import time
import sqlite3
import randomstring
import os
import datetime
from datetime import timedelta
import ssl
import json
from discord_webhook import DiscordEmbed, DiscordWebhook
import discord

curdir = os.path.dirname(__file__) + "/"
app = Flask(__name__)

app.secret_key = randomstring.pick(30)


def is_expired(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        return False
    else:
        return True


def get_expiretime(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        how_long = (ExpireTime - ServerTime)
        days = how_long.days
        hours = how_long.seconds // 3600
        minutes = how_long.seconds // 60 - hours * 60
        return str(round(days)) + "일 " + str(round(hours)) + "시간"
    else:
        return False


def getip():
    return request.headers.get("CF-Connecting-IP", request.remote_addr)


def make_expiretime(days):
    ServerTime = datetime.datetime.now()
    ExpireTime = ServerTime + timedelta(days=days)
    ExpireTime_STR = (ServerTime + timedelta(days=days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR


def add_time(now_days, add_days):
    ExpireTime = datetime.datetime.strptime(now_days, '%Y-%m-%d %H:%M')
    ExpireTime_STR = (ExpireTime + timedelta(days=add_days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR


def nowstr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


def get_logwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT logwebhk FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    return data


@app.route("/discord")
def discord():
    return redirect("https://discord.gg/P29QZE6Kzr")

@app.route("/", methods=["GET"])
def index():
    if ("id" in session):
        return redirect(url_for("login"))
    else:
        return redirect(url_for("setting"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "GET"):
        if ("id" in session):
            return redirect(url_for("setting"))
        else:
            return render_template("login.html")
    else:
        if ("id" in request.form and "pw" in request.form):
            if (request.form["id"].isdigit() and os.path.isfile(curdir + "../DB/" + request.form["id"] + ".db")):
                con = sqlite3.connect(curdir + "../DB/" + request.form["id"] + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM serverinfo")
                serverinfo = cur.fetchone()
                con.close()
                webhook_profile_url = serverinfo[21]
                webhook_name = serverinfo[22]
                color = serverinfo[14]
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
                if (request.form["pw"] == serverinfo[4]):
                    session.clear()
                    session["id"] = request.form["id"]
                    try:
                        webhook = DiscordWebhook(username=webhook_name,
                                                 avatar_url=webhook_profile_url,
                                                 url=get_logwebhk(session["id"]))
                        eb = DiscordEmbed(title='웹패널 로그인 알림', description=f'[웹패널로 이동하기](https://royvend.xyz)',
                                          color=color)
                        eb.add_embed_field(name='서버 아이디', value=session["id"], inline=False)
                        eb.add_embed_field(name='로그인 날짜', value=f"{nowstr()}", inline=False)
                        eb.add_embed_field(name='접속 IP', value=f"||{getip()}||", inline=False)
                        webhook.add_embed(eb)
                        webhook.execute()
                    except:
                        pass
                    return "Ok"
                else:
                    return "비밀번호가 틀렸습니다."
            else:
                return "아이디가 틀렸습니다."
        else:
            return "아이디가 틀렸습니다."

@app.route("/setting", methods=["GET", "POST"])
def setting():
    if (request.method == "GET"):
        if ("id" in session):
            con = sqlite3.connect("../DB/" + session["id"] + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM serverinfo")
            serverinfo = cur.fetchone()
            con.close()

            con = sqlite3.connect("../DB/log.db")
            cur = con.cursor()
            cur.execute(f"SELECT * FROM webhook WHERE server=='{session['id']}';")
            result = cur.fetchone()
            con.close()

            if result == None:
                log_webhook = "None"
            else:
                log_webhook = result[1]
            try:
                bank = json.loads(serverinfo[9])
                bank['banknum']
            except:
                bank = {}
            return render_template("manage.html", info=serverinfo, bank=bank, log_webhook=log_webhook)
        else:
            return redirect(url_for("login"))
    else:
        if ("id" in session):
            if (session["id"] != "495888018058510357"):
                if (request.form["buyusernamehide"] == "Y" or request.form["buyusernamehide"] == "N"):
                    if (request.form["normaloff"].isdigit() and request.form["vipoff"].isdigit() and request.form[
                        "vvipoff"].isdigit() and request.form["reselloff"].isdigit()):
                        if (request.form["roleid"].isdigit() and request.form["viproleid"].isdigit() and request.form[
                            "vviproleid"].isdigit()):
                            if (request.form["color"] == "파랑" or request.form["color"] == "빨강" or request.form[
                                "color"] == "초록" or request.form["color"] == "검정" or request.form["color"] == "회색"):
                                if request.form["webhookname"] != "" or request.form["webhookprofile"] != "":
                                    if (request.form["vipautosetting"].isdigit() and request.form[
                                        "vvipautosetting"].isdigit()):

                                        con = sqlite3.connect("../DB/" + session["id"] + ".db")
                                        cur = con.cursor()
                                        bankdata = {"bankname": request.form['bankname'],
                                                    "banknum": request.form['banknum'],
                                                    "bankowner": request.form['bankowner'],
                                                    "bankpw": request.form['bankpw']}
                                        cur.execute(
                                            "UPDATE serverinfo SET pw = ?, cultureid = ?, culturepw = ?, logwebhk = ?, buylogwebhk = ?, roleid = ?, culture_fee = ?, bank = ?, normaloff = ?, vipoff = ?, vvipoff = ?, reselloff = ?, color = ?, chargeban = ?, vipautosetting = ?, vvipautosetting = ?, buyusernamehide = ?, viproleid = ?, vviproleid = ?, webhookprofile = ?, webhookname = ?, notice = ?, least = ?;",
                                            (request.form["webpanelpw"], request.form["cultureid"],
                                                request.form["culturepw"], request.form["logwebhk"],
                                                request.form["buylogwebhk"], request.form["roleid"], request.form['fee'],
                                                json.dumps(bankdata), request.form["normaloff"], request.form["vipoff"],
                                                request.form["vvipoff"], request.form["reselloff"], request.form["color"],
                                                request.form["chargeban"], request.form["vipautosetting"],
                                                request.form["vvipautosetting"], request.form["buyusernamehide"],
                                                request.form["viproleid"], request.form["vviproleid"],
                                                request.form["webhookprofile"], request.form["webhookname"],
                                                request.form["notice"], request.form["least"]))
                                        con.commit()
                                        con.close()

                                        con = sqlite3.connect("../DB/log.db")
                                        cur = con.cursor()
                                        cur.execute(f"UPDATE webhook SET webhook = '{request.form['log_webhook']}' WHERE server=='{session['id']}';")
                                        con.commit()
                                        con.close()

                                        return "ok"
                                    else:
                                        return "VIP 자동 등급 누적 금액, VVIP 자동 등급 누적 금액은 정수로만 적어주세요."
                                else:
                                    return "웹훅 이름과 웹훅 프로필을 적어주세요."
                            else:
                                return "버튼 임베드 색깔은 파랑, 빨강, 초록, 검정, 회색 중에 하나를 입력해주세요."
                        else:
                            return "역할 아이디는 숫자로만 입력해주세요."
                    else:
                        return "할인율은 숫자로만 입력해주세요."
                else:
                    return "Y 또는 N으로만 입력해주세요."
            else:
                return "잘못된 접근입니다."
        else:
            return "로그인이 해제되었습니다. 다시 로그인해주세요."

@app.route("/buy_log", methods=["GET"])
def buy_log():
    if (request.method == "GET"):
        if ("id" in session):
            con = sqlite3.connect("../DB/buy_log.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM log WHERE server_id == ?;", (session['id'],))
            logs = cur.fetchall()
            con.close()
            logs = list(reversed(logs))
            goup = len(logs)+1
            return render_template("buy_log.html", logs=logs, count=goup)
        else:
            return redirect(url_for("login"))

@app.route("/charge_log")
def charge_log():
    if (request.method == "GET"):
        if ("id" in session):
            con = sqlite3.connect("../DB/charge_log.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM log WHERE server_id == ?;", (session['id'],))
            logs = cur.fetchall()
            con.close()
            return render_template("charge_log.html", logs=logs)
        else:
            return redirect(url_for("login"))

@app.route("/manage_user", methods=["GET"])
def manage_user():
    if ("id" in session):
        con = sqlite3.connect("../DB/" + session["id"] + ".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        con.close()
        return render_template("manage_user.html", users=users)
    else:
        return redirect(url_for("login"))



@app.route("/manage_user_detail", methods=["GET", "POST"])
def manageuser_detail():
    if (request.method == "GET"):
        if ("id" in session):
            user_id = request.args.get("id", "")
            if (user_id != ""):
                con = sqlite3.connect("../DB/" + session["id"] + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
                user_info = cur.fetchone()
                con.close()
                if (user_info != None):
                    return render_template("manage_user_detail.html", info=user_info)
                else:
                    abort(404)
            else:
                abort(404)
        else:
            return redirect(url_for("login"))
    else:
        if ("id" in session):
            if ("money" in request.form and "bought" in request.form and "id" in request.form):
                if (request.form["money"].isdigit()):
                    if (request.form["bought"].isdigit()):
                        if (request.form["warnings"].isdigit()):
                            if (request.form["rank"] == "일반" or request.form["rank"] == "VIP" or request.form[
                                "rank"] == "VVIP" or request.form["rank"] == "리셀러"):
                                con = sqlite3.connect("../DB/" + session["id"] + ".db")
                                cur = con.cursor()
                                cur.execute(
                                    "UPDATE users SET money = ?, bought = ?, warnings = ?, rank = ?, ban = ? WHERE id == ?;",
                                    (request.form["money"], request.form["bought"], request.form["warnings"],
                                     request.form["rank"], request.form["ban"], request.form["id"]))
                                con.commit()
                                con.close()
                                return "ok"
                            else:
                                return "등급은 일반, VIP, VVIP, 리셀러 중에 선택해서 적어주세요."
                        else:
                            return "문화상품권 충전 경고 수는 정수로만 적어주세요."
                    else:
                        return "누적 금액은 정수로만 적어주세요."
                else:
                    return "잔액은 정수로만 적어주세요."
            else:
                return "잘못된 접근입니다."
        else:
            return "로그인이 해제되었습니다. 다시 로그인해주세요."


@app.route("/managereq", methods=["GET", "POST"])  
def managereq():
    if ("id" in session):
        if (request.method == "GET"):
            con = sqlite3.connect("../DB/" + session["id"] + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM bankwait")
            reqs = cur.fetchall()
            cur.execute("SELECT * FROM serverinfo")
            server_info = cur.fetchone()
            con.close()
            return render_template("admin_managereq.html", server_info=server_info, reqs=reqs)
        else:
            if ("type" in request.get_json() and "id" in request.get_json() and request.get_json()["type"] in ["delete", "accept"]):
                con = sqlite3.connect("../DB/" + session["id"] + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users")
                user_info = cur.fetchone()
                if (request.get_json()["type"] == "delete"):
                    cur.execute("DELETE FROM bankwait WHERE id == ?;", (user_info[0],))
                    con.commit()
                    con.close()
                    return "ok"
                else:
                    cur.execute("SELECT * FROM bankwait WHERE id == ?;", (user_info[0],))
                    bankwait_info = cur.fetchone()
                    if (bankwait_info == None):
                        con.close()
                        return "존재하지 않는 충전신청 입니다."
                    else:
                        cur.execute("UPDATE users SET money = money + ? WHERE id == ?;", (bankwait_info[4],user_info[0]))
                        con.commit()
                        cur.execute("DELETE FROM bankwait WHERE id == ?;", (user_info[0],))
                        con.commit()
                        con.close
                        return "ok"
            else:
                return ""
    else:
        return ""

@app.route("/manage_product", methods=["GET"])
def manage_product():
    if ("id" in session):
        con = sqlite3.connect("../DB/" + session["id"] + ".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        con.close()
        return render_template("manage_prod.html", products=products)
    else:
        return redirect(url_for("login"))

@app.route("/delete_product", methods=["POST"])
def deleteprod():
    if ("id" in session):
        if ("name" in request.form):
            con = sqlite3.connect("../DB/" + session["id"] + ".db")
            cur = con.cursor()
            cur.execute("DELETE FROM products WHERE name == ?;", (request.form["name"],))
            con.commit()
            con.close()
            return "ok"
        else:
            return "fail"
    else:
        return "fail"


@app.route('/buy_log_detail', methods=["GET", "POST"])
def buy_log_detail():
    if (request.method == "GET"):
        if ("id" in session):
            name = request.args.get("id", "")
            if name == "":
                return redirect(url_for("buy_log"))
            else:
                if (name.isdigit()):
                    con = sqlite3.connect(f"../DB/buy_log.db")
                    cur = con.cursor()
                    cur.execute(f"SELECT * FROM log WHERE server_id == ? AND buy_id == ?;", (session.get('id'),int(name),))
                    logs = cur.fetchall()
                    con.close()
                    if logs == []:
                        return render_template("buy_log_detail.html")
                    else:
                        return render_template("buy_log_detail.html", logs=logs, qna=name)
                else:
                    con = sqlite3.connect(f"../DB/buy_log.db")
                    cur = con.cursor()
                    cur.execute(f"SELECT * FROM log WHERE server_id == ? AND product_name == ?;", (session.get('id'),name))
                    logs = cur.fetchall()
                    con.close()
                    if logs == []:
                        return render_template("buy_log_detail.html")
                    else:
                        return render_template("buy_log_detail.html", logs=logs, qna=name)
        else:
            return redirect(url_for("login"))
    else:
        name = request.form["qna"]
        if name == "":
            return redirect(url_for("buy_log"))
        else:
            if (name.isdigit()):
                con = sqlite3.connect(f"../DB/buy_log.db")
                cur = con.cursor()
                cur.execute(f"SELECT * FROM log WHERE server_id == ? AND buy_id == ?;", (session.get('id'),int(name),))
                logs = cur.fetchall()
                con.close()
                if logs == []:
                    return {"result": "no", "text": "해당 유저ID를 찾을 수 없습니다."}
                else:
                    return render_template("buy_log_detail.html", logs=logs, qna=name)
            else:
                con = sqlite3.connect(f"../DB/buy_log.db")
                cur = con.cursor()
                cur.execute(f"SELECT * FROM log WHERE server_id == ? AND product_name == ?;", (session.get('id'), name))
                logs = cur.fetchall()
                con.close()
                if logs == []:
                    return {"result": "no", "text": "해당 제품명을 찾을 수 없습니다."}
                else:
                    return render_template("buy_log_detail.html", logs=logs, qna=name)


@app.route("/manage_product_detail", methods=["GET", "POST"])
def manage_product_detail():
    if (request.method == "GET"):
        if ("id" in session):
            product_name = request.args.get("id", "")
            if (product_name != ""):
                con = sqlite3.connect("../DB/" + session["id"] + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM products WHERE name == ?;", (product_name,))
                prod_info = cur.fetchone()
                con.close()
                if (prod_info != None):
                    return render_template("manage_prod_detail.html", info=prod_info)
                else:
                    abort(404)
            else:
                abort(404)
        else:
            return redirect(url_for("login"))
    else:
        if ("id" in session):
            if ("price" in request.form and "produrl" in request.form and "stock" in request.form and "name" in request.form and "product_name" in request.form):
                if (request.form["price"].isdigit()):
                    con = sqlite3.connect("../DB/" + session["id"] + ".db")
                    cur = con.cursor()
                    cur.execute(f"SELECT * FROM products WHERE name == '{request.form['product_name']}'")
                    result = cur.fetchone()
                    con.close()
                    if result == None:

                        con = sqlite3.connect("../DB/" + session["id"] + ".db")
                        cur = con.cursor()
                        cur.execute("UPDATE products SET name = ? WHERE name == ?;", (
                        request.form["product_name"], request.form["name"]))
                        con.commit()
                        con.close()

                        con = sqlite3.connect("../DB/" + session["id"] + ".db")
                        cur = con.cursor()
                        cur.execute(f"SELECT * FROM products WHERE name == '{request.form['product_name']}';")
                        result = cur.fetchone()[2]
                        gop = str(result).split("\n")
                        con.close()

                        con = sqlite3.connect("../DB/" + session["id"] + ".db")
                        cur = con.cursor()
                        cur.execute("UPDATE products SET money = ?, produrl = ?, stock = ? WHERE name == ?;", (
                        request.form["price"], request.form["produrl"], request.form["stock"],
                        request.form["name"]))
                        con.commit()
                        con.close()


                        finaa = str(request.form["stock"]).split("\n")
                        finnayl = int(len(finaa))-int(len(gop))

                        con = sqlite3.connect("../DB/log.db")
                        cur = con.cursor()
                        cur.execute(f"SELECT * FROM webhook WHERE server == '{session['id']}'")
                        webhook = cur.fetchone()
                        con.close()

                        con = sqlite3.connect("../DB/" + session["id"] + ".db")
                        cur = con.cursor()
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

                        print(len(gop))
                        print(finnayl)
                        if finnayl == 0:
                            pass
                        else:
                            if webhook == None:
                                pass
                            else:
                                con = sqlite3.connect("../DB/" + session["id"] + ".db")
                                cur = con.cursor()
                                cur.execute(f"SELECT * FROM products WHERE name == '{request.form['product_name']}';")
                                result = cur.fetchone()
                                con.close()
                                if result[3] == "":
                                    try:
                                        webhooks = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=webhook[1])
                                        eb = DiscordEmbed(title='입고 알림', description=f'제품이 입고되었습니다.', color=color)
                                        eb.add_embed_field(name='제품명', value=f"`{request.form['product_name']}`", inline=False)
                                        eb.add_embed_field(name='제품 가격', value=f"{request.form['price']}원", inline=False)
                                        eb.add_embed_field(name='입고 전 재고 개수', value=f"{len(gop)}개", inline=False)
                                        eb.add_embed_field(name='입고된 재고 개수', value=f"{finnayl}개", inline=False)
                                        eb.add_embed_field(name='남은 재고 개수', value=f"{len(finaa)}개", inline=False)
                                        eb.set_footer(text=datetime.datetime.now().strftime('%m월 %d일 %H시 %M분'.encode('unicode-escape').decode()).encode().decode('unicode-escape'))
                                        webhooks.add_embed(eb)
                                        webhooks.execute()
                                    except:
                                        pass
                                else:
                                    try:
                                        webhooks = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=webhook[1])
                                        eb = DiscordEmbed(title='입고 알림', description=f'제품이 입고되었습니다.', color=color)
                                        eb.set_author(name=request.form['product_name'],icon_url=result[3])
                                        eb.set_thumbnail(url=result[3])
                                        eb.add_embed_field(name='제품명', value=f"`{request.form['product_name']}`", inline=False)
                                        eb.add_embed_field(name='제품 가격', value=f"{request.form['price']}원", inline=False)
                                        eb.add_embed_field(name='입고 전 재고 개수', value=f"{len(gop)}개", inline=False)
                                        eb.add_embed_field(name='입고된 재고 개수', value=f"{finnayl}개", inline=False)
                                        eb.add_embed_field(name='남은 재고 개수', value=f"{len(finaa)}개", inline=False)
                                        eb.set_footer(text=datetime.datetime.now().strftime('%m월 %d일 %H시 %M분'.encode('unicode-escape').decode()).encode().decode('unicode-escape'))
                                        webhooks.add_embed(eb)
                                        webhooks.execute()
                                    except:
                                        pass
                    else:
                            con = sqlite3.connect("../DB/" + session["id"] + ".db")
                            cur = con.cursor()
                            cur.execute(f"SELECT * FROM products WHERE name == '{request.form['product_name']}';")
                            result = cur.fetchone()[2]
                            gop = str(result).split("\n")
                            con.close()

                            con = sqlite3.connect("../DB/" + session["id"] + ".db")
                            cur = con.cursor()
                            cur.execute("UPDATE products SET money = ?, produrl = ?, stock = ? WHERE name == ?;", (
                            request.form["price"], request.form["produrl"], request.form["stock"],
                            request.form["name"]))
                            con.commit()
                            con.close()

                            finaa = str(request.form["stock"]).split("\n")
                            finnayl = int(len(finaa))-int(len(gop))

                            con = sqlite3.connect("../DB/log.db")
                            cur = con.cursor()
                            cur.execute(f"SELECT * FROM webhook WHERE server == '{session['id']}'")
                            webhook = cur.fetchone()
                            con.close()

                            con = sqlite3.connect("../DB/" + session["id"] + ".db")
                            cur = con.cursor()
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

                            if finnayl == 0:
                                pass
                            else:
                                if webhook == None:
                                    pass
                                else:
                                    con = sqlite3.connect("../DB/" + session["id"] + ".db")
                                    cur = con.cursor()
                                    cur.execute(f"SELECT * FROM products WHERE name == '{request.form['product_name']}';")
                                    result = cur.fetchone()
                                    con.close()
                                    if result[3] == "":
                                        try:
                                            webhooks = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=webhook[1])
                                            eb = DiscordEmbed(title='입고 알림', description=f'제품이 입고되었습니다.', color=color)
                                            eb.add_embed_field(name='제품명', value=f"`{request.form['product_name']}`", inline=False)
                                            eb.add_embed_field(name='제품 가격', value=f"{request.form['price']}원", inline=False)
                                            eb.add_embed_field(name='입고 전 재고 개수', value=f"{len(gop)}개", inline=False)
                                            eb.add_embed_field(name='입고된 재고 개수', value=f"{finnayl}개", inline=False)
                                            eb.add_embed_field(name='남은 재고 개수', value=f"{len(finaa)}개", inline=False)
                                            eb.set_footer(text=datetime.datetime.now().strftime('%m월 %d일 %H시 %M분'.encode('unicode-escape').decode()).encode().decode('unicode-escape'))
                                            webhooks.add_embed(eb)
                                            webhooks.execute()
                                        except:
                                            pass
                                    else:
                                        try:
                                            webhooks = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=webhook[1])
                                            eb = DiscordEmbed(title='입고 알림', description=f'제품이 입고되었습니다.', color=color)
                                            eb.set_author(name=request.form['product_name'],icon_url=result[3])
                                            eb.set_thumbnail(url=result[3])
                                            eb.add_embed_field(name='제품명', value=f"`{request.form['product_name']}`", inline=False)
                                            eb.add_embed_field(name='제품 가격', value=f"{request.form['price']}원", inline=False)
                                            eb.add_embed_field(name='입고 전 재고 개수', value=f"{len(gop)}개", inline=False)
                                            eb.add_embed_field(name='입고된 재고 개수', value=f"{finnayl}개", inline=False)
                                            eb.add_embed_field(name='남은 재고 개수', value=f"{len(finaa)}개", inline=False)
                                            eb.set_footer(text=datetime.datetime.now().strftime('%m월 %d일 %H시 %M분'.encode('unicode-escape').decode()).encode().decode('unicode-escape'))
                                            webhooks.add_embed(eb)
                                            webhooks.execute()
                                        except:
                                            pass

                            return "ok"
                else:
                    return "가격은 숫자로만 적어주세요."
            else:
                return "잘못된 접근입니다."
        else:
            return "로그인이 해제되었습니다. 다시 로그인해주세요."


@app.route("/user_result", methods=["GET", "POST"])
def user_result():
    if (request.method == "GET"):
        if ("id" in session):
            return render_template("manage_user.html")
        else:
            return redirect(url_for("login"))
    else:
        if ("id" in session):
            if ("user_id" in request.form):
                con = sqlite3.connect("../DB/" + session["id"] + ".db")
                cur = con.cursor()
                cur.execute(f"SELECT * FROM users WHERE id == ?;", (request.form["user_id"],))
                user = cur.fetchone()
                con.close()
                if (user == None):
                    return {"result": "no", "text": "존재하지 않는 유저입니다."}
                else:
                    users = str(user).replace("(", "").replace(",)", "")
                    return users
            else:
                return "잘못된 접근입니다."
        else:
            return "로그인이 해제되었습니다. 다시 로그인해주세요."


@app.route("/createprod", methods=["GET", "POST"])
def createprod():
    if (request.method == "GET"):
        if ("id" in session):
            return render_template("create_prod.html")
        else:
            return redirect(url_for("login"))
    else:
        if ("id" in session):
            if ("price" in request.form and "name" in request.form):
                if (request.form["price"].isdigit()):
                    con = sqlite3.connect("../DB/" + session["id"] + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM products WHERE name == ?;", (request.form["name"],))
                    prod = cur.fetchone()
                    if (prod == None):
                        con = sqlite3.connect("../DB/" + session["id"] + ".db")
                        cur = con.cursor()
                        cur.execute("INSERT INTO products VALUES(?, ?, ?, ?);",
                                    (request.form["name"], request.form["price"], "", ""))
                        con.commit()
                        con.close()
                        return "ok"
                    else:
                        return "이미 존재하는 제품명입니다."
                else:
                    return "가격은 숫자로만 적어주세요."
            else:
                return "잘못된 접근입니다."
        else:
            return "로그인이 해제되었습니다. 다시 로그인해주세요."


@app.route("/license", methods=["GET", "POST"])
def managelicense():
    if (request.method == "GET"):
        if ("id" in session):
            con = sqlite3.connect("../DB/" + session["id"] + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM serverinfo")
            serverinfo = cur.fetchone()
            con.close()
            if (is_expired(serverinfo[1])):
                return render_template("manage_license.html", expire="0일 0시간 (만료됨)")
            else:
                return render_template("manage_license.html", expire=get_expiretime(serverinfo[1]))
        else:
            return redirect(url_for("login"))
    else:
        if ("id" in session):
            if ("code" in request.form):
                license_key = request.form["code"]
                con = sqlite3.connect("../DB/" + "license.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
                search_result = cur.fetchone()
                con.close()
                if (search_result != None):
                    if (search_result[2] == 0):
                        con = sqlite3.connect("../DB/" + "license.db")
                        cur = con.cursor()
                        cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;",
                                    (1, nowstr(), session["id"], license_key))
                        con.commit()
                        cur = con.cursor()
                        cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
                        key_info = cur.fetchone()
                        con.close()
                        con = sqlite3.connect("../DB/" + session["id"] + ".db")
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
                        return f"{key_info[1]}"
                    else:
                        return "이미 사용된 라이센스입니다."
                else:
                    return "존재하지 않는 라이센스입니다."
            else:
                return "잘못된 접근입니다."
        else:
            return "로그인이 해제되었습니다. 다시 로그인해주세요."


@app.route("/product/<docsid>", methods=["GET"])
def product(docsid):
    con = sqlite3.connect("../DB/docs.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM docs WHERE id == ?;", (docsid,))
    docs_info = cur.fetchone()
    con.close()
    if (docs_info != None):
        # return docs_info[1].replace("\n", "<br>")
        return render_template("docs.html", docs=docs_info[1])
    else:
        return render_template("docs.html", docs="존재하지 않는 제품입니다.")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # 보안 호스트
