import os
from dotenv import load_dotenv

load_dotenv()

from telethon import TelegramClient, events, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = os.getenv('mtprotoapiid')
api_hash = os.getenv('mtprotoapihash')
bot_token = os.getenv('mtprototoken')

client = TelegramClient('user_session', api_id, api_hash)

async def main():
    print(await client.get_me())

with client:
    client.loop.run_until_complete(main())