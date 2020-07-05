# Twitch Chat

Experimental project to monitor Twitch chat messages and show them on a stream with
OBS.

## How it works

Twitch chat is basically an IRC channel. So this script connects to the IRC channel of a
Twitch channel and start polling the messages. Once a message arrives it is written to a
file.

To show the messages on stream add a new text source in your OBS Scene pointing to a
file.

By default the script is going to create a new file called `chat_messages.txt` in script
directory. This is the file that need to be set on OBS text source. It is possible to
override it adding a new configuration on `.env` file: `CHAT_MESSAGES_FILE`.


## How to

### Install

The usage of Python virtualenv is highly recommended.

```
git clone git@github.com:cacarrara/twitch-chat.git
cd twitch-chat
pip install -r requirements.txt
```

### Configure

```
cp env.sample .env
```
Now edit the `.env` file created with your user name and your OAuth token.

### Run

```
python main.py
```

## Configurations

- `TWITCH_OAUTH_USERNAME`: user name used to authenticate in Twitch
- `TWITCH_OAUTH_TOKEN`: OAuth token used to authenticate in Twitch
- `CHAT_MESSAGES_FILE`: file path used as text source on OBS
- `MAX_MESSAGES_SCREEN`: how many messages should be kept on the screen
