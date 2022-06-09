import os
import configparser

PATH = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read('config.conf')
cfg = config['DEFAULT']
