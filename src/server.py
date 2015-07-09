from location import parse_location_file
from spyfall import new_game
from irc import ircbot
from re import *
from time import time

class server:

  IDLE = 1
  JOIN = 2
  PLAY = 3

  def __init__(self, ip, port, channel, loc_file):
    self.locations = parse_location_file(loc_file)
    self.irc = ircbot(ip, port, channel, self.handle, self.timehandle)
    self.state = self.IDLE
    self.players = []
    self.game = None
    self.nextminute = 0.0
    self.timelimit = 480.0
    self.endtime = 0.0

  def run(self):
    self.irc.run()

  def handle(self, irc, sender, message):

    command = message.strip().lower().split()[0]
    args = message.strip().lower().split()[1:]

    if (self.state == self.IDLE):
      if (message == "prepare"):
        self.state = self.JOIN
        irc.send("Preparing for a game! Type '" + irc.prefix + " join' to join!")
      if (message.split == "limit"):
        try:
          self.timelimit = int(args[1]) * 60
        except Exception:
          irc.send("Please specify a number") 
        else:
          irc.send("Time limit set to " + self.timelimit + " seconds")
    elif (self.state == self.JOIN):
      if (message == "join"):
        self.players.append(sender)
        irc.send(sender + " has joined the game!")
      elif (message == "start"):
        self.state = self.PLAY
        self.play()
        irc.send("Game is starting! Too late to join now!")
    elif (self.state == self.PLAY):
      if (message == "stop"):
        self.state = self.IDLE
        self.stop()
        irc.send("The game has been ended by " + sender + "!")
      elif (message == "time"):
        irc.send(self.timeleft() + " minutes left!");
    else:
      # The universe is broken
      raise Exception("Somethis is terriby wrog")

  def play(self):
    game = new_game(self.locations, len(self.players))
    for p, m in zip(players, game.messages()):
      self.irc.psend(p, m)
    self.irc.send("Roles have been private messaged to each player!")
    self.endtime = time() + self.timelimit

  def stop(self):
    self.players = []

  def timeleft(self):
    return str(round((self.nextminute - self.timelimit) / 60.0, 2))

  def timehandle(self):
    if (time() > self.endtime):
      self.irc.send("Ding Ding Ding! Time's up!") 
    elif (time() > self.nextminute):
      self.irc.send(self.timeleft() + " minutes left!");
      self.nextminute += 60.0
