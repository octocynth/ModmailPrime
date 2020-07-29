import json
import os
import sys
import asyncio

config = {
    'prefix': '&',
    'developers': [],
    'discord_token': "Put Discord API Token here.",
    'debug': False,
}
config_file = 'config.json'

if os.path.isfile(config_file):
    with open(config_file) as f:
        config.update(json.load(f))

with open(config_file, 'w') as f:
    json.dump(config, f, indent='\t')
