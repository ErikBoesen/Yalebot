from .base import Module
import random

class Kelbo(Module):
  DESCRIPTION = '____ __ _____'
  ARGC = 0

  # returns a random string of ___ __ _ ____
  def random(self):
    kelboed_message = ""
    for x in range(0, random.randint(2, 10)):
      kelboed_message += "_" * random.randint(1, 5)
      kelboed_message += " "
    return kelboed_message

  # returns a kelboified version of a text arg
  def kelboify(self, text):
    return "".join([" " if char == " " else "_" for char in text])
    
  def response(self, query, message):
    if len(query) > 0:
      return self.random()
    else:
      return self.kelboify(query)
