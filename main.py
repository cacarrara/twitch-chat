from pathlib import Path
from twitchclient import TwitchChatClient


class OBSChatHandler:
    def __init__(self, filepath, max_messages=5):
        self.messages_file = Path(filepath)
        self._messages = []
        self._max_messages = max_messages
        self._init_message_file()

    def _init_message_file(self):
        with open(self.messages_file, mode="w") as f:
            f.write("")

    def add_message(self, message):
        if len(self._messages) >= self._max_messages:
            self._messages.pop()

        self._messages.insert(0, message)
        self._refresh_file()

    def _refresh_file(self):
        with open(self.messages_file, mode="w") as f:
            f.writelines([f"{msg}\n\n" for msg in reversed(self._messages)])


if __name__ == "__main__":
    import time
    from prettyconf import config

    username = config("TWITCH_OAUTH_USERNAME")
    token = config("TWITCH_OAUTH_TOKEN")
    chat_messages_file = config("CHAT_MESSAGES_FILE", default="chat_messages.txt")
    max_messages_on_screen = config("MAX_MESSAGES_SCREEN", default="7", cast=int)

    client = TwitchChatClient()
    client.connect(username, token)
    client.join_channel(username)

    obs_chat_handler = OBSChatHandler(
        chat_messages_file, max_messages=max_messages_on_screen
    )

    while True:
        messages = client.read_messages()
        for message in messages:
            obs_chat_handler.add_message(message)
        time.sleep(7)
