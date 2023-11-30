import discord
from discord.ext import commands
import asyncio
import os
import datetime
import time
import requests
import pytz
import mcstatus
from  mcstatus  import  JavaServer

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

server_ip = 'server_ip' #這裡輸入您server的ip
server_port = server_port #這裡輸入您server的端口號
Bedrock = server_Bedrock_ip #沒有可以刪除這行，還有下面的43行與62行
y = '' #這裡輸入您的所有版本

server_check_task = None
status_message = None

async def update_server_status(channel):
    global status_message

    while True:
        try:
            response = requests.get(f'https://api.mcsrvstat.us/3/{server_ip}:{server_port}')
            server_data = response.json()
            server = JavaServer.lookup("server_ip:server_port") #這裡請填入您server的ip 格式server_ip:server_port

            if server_data['online']:
                players_online = server_data['players']['online']
                taiwan_tz = pytz.timezone('Asia/Taipei')
                taiwan_time = datetime.datetime.now(taiwan_tz).strftime("%Y-%m-%d %p %I:%M:%S")
                ping = round(server.ping(), 1)

                embed = discord.Embed(title=f':white_check_mark:  伺服器狀態 - 在線 :white_check_mark: ', color=discord.Color.green())
                embed.add_field(name='伺服器 IP', value=server_data['hostname'], inline=False)
                embed.add_field(name='java版Port', value=server_data['port'], inline=False)
                embed.add_field(name='基岩版Port', value=Bedrock, inline=False) #這裡!
                embed.add_field(name='版本', value= y, inline=False)
                embed.add_field(name='ping', value=f"{ping}ms", inline=False)
                embed.add_field(name='檢查時間', value=taiwan_time, inline=False)
                embed.add_field(name='玩家在線', value=f"{players_online}/{server_data['players']['max']}", inline=False)
                embed.set_footer(text='', icon_url='') #這裡可以打下面的文字與圖片 圖片請輸入url

                if status_message is not None:
                    await status_message.edit(embed=embed)
                else:
                    status_message = await channel.send(embed=embed)

            else:
                taiwan_tz = pytz.timezone('Asia/Taipei')
                taiwan_time = datetime.datetime.now(taiwan_tz).strftime("%Y-%m-%d %p %I:%M:%S")

                embed = discord.Embed(title=f':x: 伺服器狀態 - 離線 :x:', color=discord.Color.red())
                embed.add_field(name='伺服器 IP', value=server_data['hostname'], inline=False)
                embed.add_field(name='伺服器 Port', value=server_data['port'], inline=False)
                embed.add_field(name='基岩版Port', value={Bedrock}, inline=False) #和這裡!
                embed.add_field(name='檢查時間', value=taiwan_time, inline=False)
                embed.add_field(name='ping', value="無法取得", inline=False)
                embed.set_footer(text='', icon_url='') #這裡可以打下面的文字與圖片 圖片請輸入url

                if status_message is not None:
                    await status_message.edit(embed=embed)
                else:
                    status_message = await channel.send(embed=embed)

                if status_message is None:
                    await status_message.edit(content="正在更新服务器状态...")
                else:
                    status_message = await channel.send("开始监视服务器状态...")

        except Exception as e:
            print(e)

        await asyncio.sleep(30)

@bot.event
async def on_ready():
    global server_check_task
    print(f'已連結機器人 {bot.user.name}')
    
    if server_check_task is None:
        text_channel_id = 000000000000000000  #填入你要發送訊息的頻道id
        channel = bot.get_channel(text_channel_id)
        server_check_task = asyncio.create_task(update_server_status(channel))

@bot.command()
async def status(ctx):
    await ctx.send('正在检查服务器状态...')

bot.run('') #填入你的discord bot TOKEN
