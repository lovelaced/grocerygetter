# -*- coding: utf-8 -*-
import os
import logging
import random
import time
from os.path import expanduser

homedir = expanduser("~")
repodir = '/git/lists/'

class irc_colors:
        NORMAL = u"\u000f"
        BOLD = u"\u0002"
        UNDERLINE = u"\u001f"
        REVERSE = u"\u0016"
        WHITE = u"\u00030"
        BLACK = u"\u00031"
        DARK_BLUE = u"\u00032"
        DARK_GREEN = u"\u00033"
        RED = u"\u00034"
        BROWN = u"\u00035"
        GREEN = u"\u00039"

logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] [%(levelname)s] %(message)s")

def getuser(ircmsg):
    return ircmsg.split(":")[1].split('!')[0]


_command_dict = {}


def command(name):
    # The decorator appending all fn's to a dict
    def _(fn):
        # Decorators return an inner function whom we
        # pass the function.
        _command_dict[name] = fn
    return _


def nothing(args):
    return ""

def get_command(name):
    # Explicity over implicity?
    # Fuck that

    # We just lower the string.
    # and check later its upper cased
    if name.lower() in _command_dict:
        return _command_dict[name.lower()]
    else:
        return nothing

@command("help")
def get_help(args):
    sendmsg = args["sendmsg"]
    commands = [
        ".add: add an item to your list",
        ".del: delete an item from your list",
        ".newlist: erase your list to start anew"
    ]
    for command in commands:
        sendmsg(getuser(args["raw"]), command)
        time.sleep(1)
    return "sent ;)"

@command("add")
def add(args):
    user = getuser(args["raw"])
    item = args["args"]
    item = " ".join(item)
    try:

        logging.debug("Attempting to open file: " + homedir + repodir + user + ".txt [append/create]")

        with open(homedir + repodir + user + ".txt", "a+") as textlist:
            lines = textlist.readlines()
            for line in lines:

                logging.debug("Reading line from file: " + line)

                if item.strip().lower() == line.strip().lower():

                    logging.info("Found a match for " + item + "in file")

                    return user + ", you've already added that..."
            else:
                textlist.write(item + "\n")
        return irc_colors.BOLD + item.capitalize() + irc_colors.NORMAL + \
               " successfully added to " + user + "'s list."
    except IOError as error:
        logging.warning(str(error))
        return "uh something bad happened"

@command("del")
def delete(args):
    user = getuser(args["raw"])
    item = args["args"]
    item = " ".join(item)
    try:

        logging.debug('Attempting to open file: ' + homedir + repodir + user + ".txt [reading]")
        logging.debug('Attempting to open new file: ' + homedir +repodir + user + ".txt.new [writing]")

        with open(homedir + repodir + user + ".txt", "r") as oldlist, \
                open(homedir +repodir + user + ".txt.new", "w+") as newlist:
            found = 0
            for line in oldlist.readlines():

                logging.debug('Checking line in file: ' + line + ' against item: ' + item)

                if item.strip().lower() != line.strip().lower():

                    logging.debug("Writing " + line + " to " + homedir +repodir + user + ".txt.new")

                    newlist.write(line)
                else:
                    found = 1
            if found:

                logging.info("Found " + item + " in " + homedir + repodir + user + ".txt")

                os.rename(homedir +repodir + user + ".txt.new", homedir + repodir + user + ".txt")
                return irc_colors.BOLD + item.capitalize() + irc_colors.NORMAL +\
                       " successfully deleted from " + user + "'s list."
            else:
                os.remove(homedir +repodir + user + ".txt.new")
                return irc_colors.BOLD + item.capitalize() + irc_colors.NORMAL + " wasn't in " + user + "'s list."
    except IOError as error:
        logging.warning(str(error))
        return user + " doesn't have a list."

@command("newlist")
def new_list(args):
    user = getuser(args["raw"])
    try:
        logging.debug("Deleting file: " + homedir + repodir + user + ".txt")
        os.remove(homedir + repodir + user + ".txt")
    except OSError as error:
        logging.warning(str(error))
        return user + "'s list has already been cleared."
    return user + "'s previous list has been cleared."

@command("r")
def random_option(args):
    arguments = args["args"]
    choice_list = []
    # current_choice = ""
    # for index in range(len(arguments)-1):
    #     word = arguments[index]
    #     if word != "|" and current_choice != "":
    #         current_choice = current_choice + " " + word
    #     elif current_choice == "":
    #         current_choice = word
    #     elif (word == "|" or index == len(arguments)-1) and current_choice != "":
    #         choice_list.append(current_choice)
    #         current_choice = ""

    for index in range(len(arguments)-1):
        word = arguments[index]
        sep_list = []
        if word == "|":
            sep_list.append(index)
        print sep_list
        for i in range(len(sep_list)-1):
            if i is not 0:
                current_choice = " ".join(arguments[i-1:i+1])
                print "i not 0", current_choice
            elif i is not len(sep_list)-1:
                current_choice = " ".join(arguments[:i])
                print "i not len", current_choice
            else:
                current_choice = " ".join(arguments[i:])
                print "else", current_choice

            if current_choice is not None:
                choice_list.append(current_choice)
        print choice_list
        if choice_list:
            return random.choice(choice_list)
        else:
            return ""

