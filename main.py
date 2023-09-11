import discord
import asyncio
import socket
import os
import datetime
import time
import ping3

# 初始化Discord客户端
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

# 监视的服务器IP和端口
server_ip = 'edge.icehost.xyz'
server_port = 25947

server_online = False  # 用于存储服务器在线状态


async def check_server_status(channel):
  global server_online

  while True:
    try:
      start_time = time.time()
      # 创建一个套接字对象并尝试连接到服务器
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)  # 设置连接超时时间为5秒
        s.connect((server_ip, server_port))
      end_time = time.time()
      ping_ms = round((end_time - start_time) * 1000, 2)  # 计算响应时间（以毫秒为单位）

      embed = discord.Embed(title=f':x: 伺服器狀態 - 離線 :x:',
                            color=discord.Color.red())
      embed.add_field(name='伺服器 IP', value=server_ip, inline=False)
      embed.add_field(name='伺服器 Port', value=server_port, inline=False)
      embed.add_field(
          name='檢查時間',
          value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          inline=False)
      embed.add_field(name='機器人 Ping 延迟', value=f'{ping_ms} ms', inline=False)
      embed.set_footer(
          text='宇的伺服器監視x @&b 服主 宇 製作',
          icon_url=
          'https://cdn.discordapp.com/avatars/1110595055758090304/801f181d0aca9994f891824d60ec236f.png?size=512'
      )

      if not server_online:
        await channel.send(embed=embed)
        server_online = True
    except (ConnectionRefusedError, socket.timeout):
      if server_online:
        embed = discord.Embed(
            title=f':white_check_mark: 伺服器狀態 - 線上 :white_check_mark:',
            color=discord.Color.green())
        embed.add_field(name='伺服器 IP', value=server_ip, inline=False)
        embed.add_field(name='伺服器 Port', value=server_port, inline=False)
        embed.add_field(
            name='檢查時間',
            value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            inline=False)
        embed.set_footer(
            text='宇的伺服器監視系統x @&b 服主 宇 製作',
            icon_url=
            'https://cdn.discordapp.com/avatars/1110595055758090304/801f181d0aca9994f891824d60ec236f.png?size=512'
        )
        await channel.send(embed=embed)
        server_online = False

    await asyncio.sleep(60)  # 每60秒检查一次


@client.event
async def on_ready():
  global server_online
  print(f'Logged in as {client.user.name}')

  # 启动服务器检查循环
  if not server_online:
    # 请将下面的通道ID替换为你希望将服务器状态信息发送到的文本通道的ID
    text_channel_id = 1150349297464922183
    channel = client.get_channel(text_channel_id)
    server_online = await check_server_status(channel)


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!status'):
    await message.channel.send('Checking server status...')


# 运行Discord客户端
# 请将下面的令牌替换为你的Bot令牌
token = os.getenv('DISCORD_TOKEN')  # 使用环境变量来存储你的Bot令牌
client.run(token)
