import discord
import asyncio
import os
import datetime
import time
import requests
import pytz

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

server_ip = 'you_server_ip'
server_port = you_server_port

server_check_task = None
status_message = None

async def update_server_status(channel):
    global status_message  # 添加這行

    while True:
        try:
            response = requests.get(f'https://api.mcsrvstat.us/3/{server_ip}:{server_port}')
            server_data = response.json()

            if server_data['online']:
                players_online = server_data['players']['online']
                taiwan_tz = pytz.timezone('Asia/Taipei')
                taiwan_time = datetime.datetime.now(taiwan_tz).strftime("%Y-%m-%d %p %I:%M:%S")

                embed = discord.Embed(title=f':white_check_mark:  伺服器狀態 - 在線 :white_check_mark: ', color=discord.Color.green())
                embed.add_field(name='伺服器 IP', value=server_data['hostname'], inline=False)
                embed.add_field(name='伺服器 Port', value=server_data['port'], inline=False)
                embed.add_field(name='檢查時間', value=taiwan_time, inline=False)
                embed.add_field(name='玩家在線', value=f"{players_online}/{server_data['players']['max']}", inline=False)
                embed.set_footer(text='you_embed_text', icon_url='you_icon_url')

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
                embed.add_field(name='檢查時間', value=taiwan_time, inline=False)
                embed.set_footer(text='you_embed_text', icon_url='you_icon_url')

                if status_message is not None:
                    await status_message.edit(embed=embed)
                else:
                    status_message = await channel.send(embed=embed)

        except Exception as e:
            print(e)

        await asyncio.sleep(30)

@client.event
async def on_ready():
    global server_check_task
    print(f'Logged in as {client.user.name}')
    
    if server_check_task is None:
        text_channel_id = you_discord_channel_id  # Replace with your text channel ID
        channel = client.get_channel(text_channel_id)
        server_check_task = asyncio.create_task(update_server_status(channel))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!status'):
        await message.channel.send('正在检查服务器状态...')

token = 'you_discord_bot_token'
client.run(token)
