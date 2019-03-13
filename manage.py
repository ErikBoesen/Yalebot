import requests
import os
import json
from pick import pick
import argparse

parser = argparse.ArgumentParser(description="Control Yalebot directly")
parser.add_argument("verb")
args = parser.parse_args()


