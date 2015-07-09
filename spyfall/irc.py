import socket

class ircbot():
  def __init__(self, ip, port, channel, messagehandler, timehandler, nick="spyfall", prefix="@spyfall"):
    self.ip = ip
    self.port = port
    self.channel = channel
    self.prefix = prefix
    self.messagehandler = messagehandler
    self.timehandler = timehandler

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((ip, port))
    self.socket.send("USER " + (nick + " ") * 3 + ": Spyfall IRC Bot\n")
    self.socket.send("NICK " + nick + "\n")
    self.socket.send("JOIN " + channel + "\n")

  def send(self, message):
    print(message)
    self.socket.send("PRIVMSG " + self.channel + " :" + message + "\n")

  def psend(self, nick, message):
    self.socket.send("PRIVMSG " + nick + " :" + message + "\n")

  def pong(self):
    self.socket.send("PONG :pingis\n")

  def recv(self, length):
    data = self.socket.recv(length)
    print(data)
    match = re.match(r':(.+?)\s+(.+?)\s+.*?:(.+)\s*', data)
    if match:
      sender = match.group(1).split('!')[0]
      dtype = match.group(2)
      message = match.group(3)
      return dtype, sender, message
    elif re.match(r'^PING', data):
      return 'PING', ' ', ' '
    return False, False, False

  def update(self):
    dtype,sender,message = self.recv(2048)
    if not dtype or not sender or not message:
      return #abort
    if dtype == "PRIVMSG" and message.startswith(self.prefix):
      self.messagehandler(self, sender, message[(len(self.prefix)):].strip())
    elif dtype == 'PING':
      self.pong()

  def run(self):
    while True:
      self.timehandler()
      self.update()
