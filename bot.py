import discord
from discord.ext import commands, tasks
import sqlite3
import random
import requests
import ast
import io
from PIL import Image, ImageDraw, ImageFont, ImageOps
import ffmpeg
import json
import asyncio
from itertools import cycle
import cv2
from pyzbar import pyzbar
import qrcode
import os
import psutil
from Cybernator import Paginator
import ast

bot = commands.Bot(command_prefix='-')
COLOR_ERROR = 0xFF0000

@bot.event
async def on_ready():
	print('Gone')
	await bot.change_presence(activity=discord.Activity(name='mc.greenshine.space', type=discord.ActivityType.watching))

@bot.event
async def on_command_error(ctx, error):
    channel = bot.get_channel(729800700447686667)
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Ошибка", description=f"Команда `{str(ctx.message.content)}` не найдена! Убедитесь в правильности написания команды!", color=COLOR_ERROR)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, У бота недостаточно прав!\n'
                                                              f'❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций.', color=color))
    elif isinstance(error, commands.MissingPermissions) or isinstance(error, discord.Forbidden):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, У вас недостаточно прав!', color=COLOR_ERROR))
    elif isinstance(error, commands.BadArgument):
        if "Member" in str(error):
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Пользователь не найден!', color=COLOR_ERROR))
        if "Guild" in str(error):
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Сервер не найден!', color=COLOR_ERROR))
        else:
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Введён неверный аргумент!', color=COLOR_ERROR))
    elif isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Пропущен аргумент с названием {error.param.name}!', color=COLOR_ERROR))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Воу, Воу, Не надо так быстро прописывать команды.\n'
                                                       f'❗️ Подожди {error.retry_after:.2f} секунд и сможешь написать команду ещё раз.'))
    else:
        if "ValueError: invalid literal for int()" in str(error):
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Укажите число а не строку!', color=COLOR_ERROR))
        else:
            await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, \n**`ERROR:`** {error}', color=COLOR_ERROR))
            raise error

@bot.command()
async def greenshine(ctx):
	from mcstatus import MinecraftServer
	ip = 'mc.greenshine.space'
	server = MinecraftServer.lookup(ip)
	status = server.status()
	query = server.query()
	await ctx.send(embed = discord.Embed(description = f"На сервере: `{status.players.online}`\n Задержка сервера: `{status.latency:.2f}`\n \n Тут должно что-то быть"))

@bot.command()
async def eval_fn(self, ctx, *, cmd):
    try:
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

            # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

            # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

    except Exception as error:
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, В вашем коде произошла следующая ошибка:\n`{error}`', color=config.COLOR_ERROR))

bot.run('NzI5NzkwNTAyNDkyNDM4NjUw.XwOEeA.j8bTSqLUg6jAcncm9ZUyQHqa0_o')
