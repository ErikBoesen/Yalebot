from .base import Module
import random
import re

class Kelbo(Module):
    DESCRIPTION = '____ __ _____'
    ARGC = 1

    # returns a random string of ___ __ _ ____
    def kelbo1(self):
      num_of_groups = random.randint(2, 10)
      kelboed_message = ""
      while num_of_groups > 0:
        kelboed_message+="_"*random.randint(1, 5)
        kelboed_message+=" "
        num_of_groups-=1
      return kelboed_message

    # returns a kelboified version of a text arg
    def kelbo2(self, text):
      kelboed_message = re.sub("[^\s]", "_", text)
      return kelboed_message
    
    def response(self, query, message):
      test = ""
      if query.len() > 0:
        test = self.kelbo()
      else:
        test = self.kelbo2(query)
      return test
