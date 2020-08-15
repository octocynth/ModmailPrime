import json
import os
import sys
import asyncio

import uvloop

from .db import init

config = {
    'prefix': '&',
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

uvloop.install()
asyncio.run(init(config['db']))
