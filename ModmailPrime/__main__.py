import json
import logging
import os
import sys
import asyncio

import uvloop
from discord.ext import commands

from .db import init

config = {
    'prefix': '$',
    'developers': [0, ],
    'discord_token': "Put Discord API Token here.",
    'server_id': 0,
    'category_id': 0,
    'error_channel_id': 0,
    'debug': False,
    'db': {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': 'localhost',
                    'port': '5432',
                    'user': 'tortoise',
                    'password': 'qwerty123',
                    'database': 'test',
                }
            }
        }
    }
}

config_file = 'config.json'

if os.path.isfile(config_file):
    with open(config_file) as f:
        config.update(json.load(f))

with open(config_file, 'w') as f:
    json.dump(config, f, indent='\t')

uvloop.install()  # uvloop is a drop in replacement for the asyncio event loop, this should make it faster

bot = commands.Bot(command_prefix=config['prefix'])
bot.bot_config = config

asyncio.run(init(config['db']))

if config['debug']:
    level = logging.DEBUG
else:
    level = logging.INFO
logging.basicConfig(level=level)

for ext in os.listdir('ModmailPrime/cogs'):
    if not ext.startswith(('_', '.')):
        bot.load_extension('ModmailPrime.cogs.' + ext[:-3])  # Remove '.py'

bot.run(config['discord_token'])
