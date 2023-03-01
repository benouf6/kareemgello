from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
APP_ID = os.environ.get("APP_ID")
APP_HASH = os.environ.get("APP_HASH")
session = os.environ.get("TERMUX")
mb = TelegramClient(StringSession(session), APP_ID, APP_HASH)
