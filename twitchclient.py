import socket


class TwitchChatClient:
    def __init__(self):
        self._host = "irc.chat.twitch.tv"
        self._port = 6667
        self.username = None
        self.password = None

        self._socket = None

    def connect(self, username, password):
        self.username = username
        self.password = password

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))

        self._send_command(f"PASS {self.password}")
        self._send_command(f"NICK {self.password}")

    def disconnect(self):
        self._socket.close()

    def join_channel(self, channel_name):
        self._send_command(f"JOIN #{channel_name}")

    def read_messages(self):
        response = self._socket.recv(1024)
        response = response.decode("UTF-8")

        if "PING" in response:
            self._answer_pong()

        return self._get_messages(response)

    def _send_command(self, command):
        _cmd = f"{command}\r\n".encode("UTF-8")
        self._socket.send(_cmd)

    def _answer_pong(self):
        self._send_command("PONG :tmi.twitch.tv")

    def _get_messages(self, response):
        _commands = response.split("\r\n")
        messages = []

        for command in _commands:
            message = self._get_message(command)
            if message:
                messages.append(message)

        return messages

    def _get_message(self, cmd):
        if "PRIVMSG" not in cmd:
            return

        command_parts = cmd.split(":", 2)

        if not command_parts or len(command_parts) < 3:
            return

        author = command_parts[1].split("!")[0]
        message = command_parts[2]

        return f"|{author}|> {message}"
