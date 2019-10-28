import os
import logging

# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

# Backend is any errbot backend. By default we want slack, but you could set this to text for easier local dev
BACKEND = os.environ.get("BOT_MODE", "Slack")
BOT_IDENTITY = {
    'token': os.environ.get("SLACK_TOKEN")
}
BOT_DIR = os.environ.get("BOT_DIR", r'/errbot')
BOT_DATA_DIR = os.path.join(BOT_DIR, "data")
os.makedirs(BOT_DATA_DIR, exist_ok=True)
BOT_EXTRA_PLUGIN_DIR = os.path.join(BOT_DIR, "plugins")
os.makedirs(BOT_EXTRA_PLUGIN_DIR, exist_ok=True)
BOT_LOG_FILE = os.path.join(BOT_DIR, "errbot.log")

# use pip to install any requirements for plugins
AUTOINSTALL_DEPS = True

# set our logging level. Follows python standard logging levels
BOT_LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "ERROR").upper())

# set bot envs from environment. Should be a comma separated list of slack identities
BOT_ADMINS = tuple(os.environ.get("BOT_ADMINS", "").split(","))

# Allow bot to execute commands async
BOT_ASYNC = True
# Set our poolsize to 5 threads, default is 3. Tweak this higher if we start running long running bot commands
BOT_ASYNC_POOLSIZE = 5

# command prefix. This will be expected in front of every command.
# For example, if your command is "help" and your prefix is set to "./" the full command is "./help"
# BOT_ALT_PREFIXES are alternative prefixes
BOT_PREFIX = os.environ.get("BOT_PREFIX", "./")
BOT_PREFIX_OPTIONAL_ON_CHAT = False

BOT_ALT_PREFIXES = tuple(os.environ.get("BOT_ALT_PREFIXES", "").split(","))

# Slack messages are limited to 4k characters. The slack backend limits this automatically, but setting it here is
# good if someone runs the bot in text mode for local dev
MESSAGE_SIZE_LIMIT = int(os.environ.get("MESSAGE_SIZE_LIMIT", "4000"))

# DIVERT_TO_THREAD moves the response to the listed commands to a thread if the backend supports it.
# By default, we want to thread help, about, and status. Other commands can be added here, or can force themselves to be
# threaded in their code
# THREADED_COMMANDS environment variable should be a comma separated list of the method names to be diverted.
# i.e. if you want to divert
DEFAULT_THREADED = ["help", "about", "status"]
USER_THREADED = os.environ.get("THREADED_COMMANDS", "").split(",")
DIVERT_TO_THREAD = tuple(DEFAULT_THREADED + USER_THREADED)