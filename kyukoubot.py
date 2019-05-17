import discord
import kyukou
import database
import gosh

# 接続に使うオブジェクト / starting
client = discord.Client()

# 起動した確認 / confirm starting
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



# こっから処理 / processing
@client.event
async def on_message(message):

    if message.content.startswith("設定"):
        if client.user != message.author.name:
            disname = message.author.name
            a = message.content
            list = a.split()
            print(list, disname)
            database.insert(disname, list[1], list[2])
            await message.channel.purge()
            channel = message.channel
            await channel.send("設定完了しました。休講情報を取ってくるには、「休講」と言ってみてください。")

    if message.content.startswith("休講"):
        if client.user != message.author.name:
            print(message.author.name)
            channel = message.channel
            await channel.send("Beep, beep. Now loading...")
            disname = message.author.name
            id = database.searchid(disname)
            password = database.searchpass(disname)
            kyukou.main(id, password, disname)         # kyukou.py
            print("OK")

    if message.content.startswith("消去"):
        if client.user != message.author.name:
            await message.channel.purge()

# ここにはdiscordのbotのトークンを入れる / fill in "token"
TOKEN = gosh.requestsTOKEN()
client.run(TOKEN)