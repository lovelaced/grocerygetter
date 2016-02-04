# -*- coding: utf-8 -*-
import os
import logging
import random
import time
import requests
import re
from os.path import expanduser
from bs4 import BeautifulSoup

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
    # Usage: .newlist [listname]
    if args["args"]:
        try:
           return args["args"]
        except OSError as error:
           return  
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
    choices = " ".join(args["args"]).split("|")
    choice_list = []
    for choice in choices:
        choice_list.append(choice.strip())
    return random.choice(choice_list)

@command("hype")
def hype(args):
    import time
    hypeText = []
    toResolve = args["args"]
    argString = " ".join(toResolve)
    if len(toResolve) < 1:
        hypeText = ["F R O S T",
                    "R",
                    "O",
                    "S",
                    "T"]
    elif len(argString) > 8:
        return ""
    else:
        char = 0
        while char < len(argString):
            c = argString[char].upper()
            if char == 0:
                x = 1
                while x < len(argString):
                    c += (" " + argString[x].upper())
                    x += 1
            hypeText.append(c)
            char += 1
    
    sendmsg = args["sendmsg"]
    channel = args["channel"]
    for lines in hypeText:
        sendmsg(channel, lines)
        time.sleep(.3)
    return ""

@command("8")
def eightball(args):
    responses = [
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Reply hazy try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful"
    ]
    number = random.randint(0, 100)
    if number == 0:
        return "Commit suicide"
    else:
        return random.choice(responses)

@command("ud")
def ud(args):
    if args["args"]:
        try:
            int(args["args"][-1])
            payload = {"term" : " ".join(args["args"][:-1])}
        except ValueError:
            payload = {"term" : " ".join(args["args"])}
        r = requests.get("https://www.urbandictionary.com/define.php", params=payload)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            title = irc_colors.BOLD + soup.title.string[18:].upper() + irc_colors.NORMAL
            l = [e.get_text().replace("\r", "").strip() for e in soup.find_all("div", class_= "meaning")]
            if len(l) > 0:
                if len(args["args"]) > 1:
                    try:
                        i = int(args["args"][-1].strip()) 
                        if i < 1:
                            raise ValueError
                        data = title + ": "+ str(l[i-1]) + irc_colors.BOLD + " [" + str(i) + "/" + str(len(l)) + "]"
                        return data.encode("utf-8")
                    except (TypeError, IndexError, ValueError) as e:
                        pass #print error for enterprise level debugging.

                data = title + ": " + l[0] + irc_colors.BOLD + " [" + "1/" + str(len(l)) + "]"
                return data.encode("utf-8")
            else:
                return "No definition found in UD."
        else:
            return "Connection error: " + str(r.status_code)

@command("ba")
def ba(args):
    #define a user agent
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'}
    baseurl = "http://www.beeradvocate.com"
    if args["args"]:
        try:
            int(args["args"][-1])
            payload = {"q" : " ".join(args["args"][:-1])}
        except ValueError:
            payload = {"q" : " ".join(args["args"])}
        r = requests.get(baseurl + "/search/", headers=user_agent, params=payload)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            regex = re.compile("/beer/profile/.*/.+") #so we match only the beers and not the brewery.
            beers = [b.get("href") for b in soup.find_all('a') if re.match(regex, str(b.get("href")))>=0]
            if len(beers) > 0:
                data = beer_lookup(baseurl+beers[0], user_agent)
                return data['name'] + " | " + data['style'], "BA score: " + data['ba_score'] + " (From: " + data['ba_ratings'] +") | Bro score: " + data['bro_score'], data['brewery'] + " | " + data['abv'], baseurl+beers[0]

            else:
               return "No results from BA." 

# BA helper function.
def beer_lookup(url, user_agent):
    r = requests.get(url, headers=user_agent) 
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find('table', attrs = {"width" : "100%"})
        data = []
        rows = table.find_all("tr")
        for r in rows:
            cols = r.find_all("td")
            cols = [e.text.strip() for e in cols]
            data.append([e for e in cols if e])

        info = {}
        rel_data = data[0][1].split('\n')
        info['name'] = soup.title.string.split("|")[0]
        info['ba_score'] = rel_data[1]
        info['ba_class'] = rel_data[2]
        info['ba_ratings'] = rel_data[3]
        info['bro_score'] = rel_data[7]
        info['brewery'] = rel_data[25]
        (info['style'], info['abv']) = rel_data[29].split("|")
        for e in info.keys():
            info[e] = info[e].encode("utf-8")
        return info


