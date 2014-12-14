import configparser
import UserFileSys
import os
import Oram
import Encryptor
import pickle
Config = configparser.ConfigParser()

from os.path import expanduser
home = expanduser("~")

Config.read(home + "/Dropbox/config.ini")

treeSize = Config.getint("UserFileSys","treeSize")
z = Config.getint("UserFileSys","z")
segSize = Config.getint("UserFileSys","segSize")
maxStashSize = Config.getint("UserFileSys","maxStashSize")
growR = Config.getfloat("UserFileSys","growR")
targetR = Config.getfloat("UserFileSys","targetR")
shrinkR = Config.getfloat("UserFileSys","shrinkR")
multiBlock = Config.getint("UserFileSys","multiBlock")

oram = UserFileSys.UserFileSys(treeSize, z, segSize, maxStashSize, growR, targetR, shrinkR, multiBlock)
