# bot.py
import os
import random
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = 'OTA5MTY4OTE1NTkzMTk1NTgx.YZAXiQ.a8kbJbTRq85H0mPEppkDTPV26kg'

bot = commands.Bot(command_prefix='!')

reminders = {}

def convert_time(t):
    crs = [*t]
    d = []
    l = None
    while (c:=crs.pop(0)):
        if c.isdigit() or c == '.':
            d.append(c)
        else:
            l = c
            break
    if crs or l is None or l not in 'smhdy' or not d:
        return None
    try:
        n = float(''.join(d))
    except:
        return None
    if l == 'y':
        n *= 365.25
        l = 'd'
    if l == 'd':
        n *= 24
        l = 'h'
    if l == 'h':
        n *= 60
        l = 'm'
    if l == 'm':
        n *= 60
    return int(n)

def convert_to_fmt(n, l):
    if l == 'y':
        n /= 365.25
        l = 'd'
    if l == 'd':
        n /= 24
        l = 'h'
    if l == 'h':
        n /= 60
        l = 'm'
    if l == 'm':
        n /= 60
    return float(n)

async def decrement_reminders():
    while 1:
        for reminder_set in reminders.values():
            for rem in reminder_set:
                rem[1] -= 1
        await asyncio.sleep(1)

async def check_reminders(ctx):
    for user, reminder_set in reminders.copy().items():
        for l in reminder_set:
            name, nsecs, fmt = l
            if nsecs <= 0:
                await ctx.send(f'<@{user}>, reminding you about {name}!')
                reminders[user].remove(l)

@bot.command(name='remind-me', help='set a reminder')
async def add_reminder(ctx, remindername=None, remindertime='30m'):
    await check_reminders(ctx)
    nsecs = convert_time(remindertime)
    if nsecs is None or remindername is None:
        await ctx.send('Invalid Reminder')
        return
    reminders.setdefault(ctx.message.author.id, []).append([remindername, nsecs, remindertime[-1]])
    await ctx.send(f'Added a Reminder: {remindername}')

@bot.command(name='show-reminders', help='show reminders')
async def show_reminder(ctx):
    await check_reminders(ctx)
    user_reminders = reminders.get(ctx.message.author.id)
    if user_reminders is None:
        await ctx.send('No Reminders Set')
        return
    await ctx.send('\n'.join(
        [f'{n}: {convert_to_fmt(s, f):.2f}{f}' for n, s, f in user_reminders]
    ))

bot.loop.create_task(decrement_reminders())
bot.run(TOKEN)
