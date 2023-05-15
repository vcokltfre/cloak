from os import environ
from subprocess import call
from sys import argv

from dotenv import load_dotenv

load_dotenv()

call(argv[1:], env=environ)
