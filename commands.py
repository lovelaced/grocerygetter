# -*- coding: utf-8 -*-
import os
import logging
import random
import time
import requests
import re
from os.path import expanduser
from bs4 import BeautifulSoup
from nltk.tag import pos_tag

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

@command("r8")
def random_rate(args):
    message = args["args"]
    give_rating = random.randint(0, 1)
    message = pos_tag(message)
    print message
    nounlist = []
    for word, tag in message:
        if tag == "NNP" or tag == "NN":
            nounlist.append(word)
    if not nounlist:
        nounlist.append("nothings")
    word = nounlist[random.randint(0, len(nounlist)-1)]
    rating = random.randint(0, 10)
    if give_rating:
        return str(rating) + "/10"
    else:
        return word + "/10"

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
    elif len(argString) > 20:
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

@command("stump")
def trump(args):
    s = []
    s.append("I don't even want to talk about %s. Just look at his numbers. He's " \
            "a very low-energy person.")
    s.append("People come to me and tell me, they say, \"Donald, we like you, but" \
           " there's something weird about %s.\" It's a very serious problem.")
    s.append("We have incompetent people, they are destroying this country, and " \
           "%s doesn't have what we need to make it great again.")
    s.append("Nobody likes %s, nobody in Congress likes %s, nobody likes %s anywh" \
           "ere once they get to know him.")
    s.append("%s is an embarrassment to himself and his family, and the Republica" \
            "n Party has essentially -- they're not even listening to %s.")
    s.append("Look, here's the thing about %s. We're losing in all of our deals, " \
            "we're losing to Mexico, we're losing with China, and I'm sure ther" \
            "e are some good ones, but %s has to go back.")
    s.append("What are they saying? Are those %s people? Get 'em outta here! Get " \
            "'em out! Confiscate their coats!")
    s.append("Donald J. Trump is calling for a total and complete shutdown of %s " \
            "entering the United States.")
    s.append("Did you read about %s? No more \"Merry Christmas\" at %s's house. N" \
            "o more. Maybe we should boycott %s.")
    s.append("Look at that face! Would anyone vote for that? Can you imagine that" \
            ", %s, the face of our next president?")
    s.append("We have to have a wall. We have to have a border. And in that wall" \
            " we're going to have a big fat door where people can come into the" \
            " country, but they have to come in legally and those like %s who a" \
            "re here illegally will have to go back.")
    s.append("%s, you haven't been called, go back to Univision.")
    s.append("%s? You could see there was blood coming out of %s's eyes. Blood c" \
            "oming out of %s's... wherever.")
    s.append("%s is not a war hero. He's a war hero because he was captured? I l" \
            "ike people who weren't captured.")
    s.append("When Mexico sends its people, they're not sending the best. They'r" \
            "e sending people like %s that have lots of problems and they're br" \
            "inging those problems. They're bringing drugs, they're bringing cr" \
            "ime. They're rapists and some, I assume, are good people, but I sp" \
            "eak to border guards and they're telling us what we're getting.")
    s.append("I thought that was disgusting. That showed such weakness, the way " \
            "%s was taken away by two young women, the microphone; they just to" \
            "ok the whole place over. That will never happen with me. I don't " \
            "know if I'll do the fighting myself or if other people will, but t" \
            "hat was a disgrace. I felt badly for %s. But it showed that he's w" \
            "eak.")
    s.append("%s is an enigma to me. He said that he's \"pathological\" and that" \
            " he's got, basically, pathological disease... I don't want a perso" \
            "n that's got pathological disease.")
    s.append("The concept of global warming was created by and for %s in order t" \
            "o make U.S. manufacturing non-competitive.")
    s.append("The U.S. will invite %s, the Mexican criminal who just escaped pri" \
            "son, to become a U.S. citizen because our \"leaders\" can't say no" \
            "!")
    s.append("You want to know what will happen? The wall will go up and %s will" \
            " start behaving.")
    s.append("Our great African American President hasn't exactly had a positive" \
            " impact on the thugs like %s who are so happily and openly destroy" \
            "ing Baltimore!")
    s.append("%s is a weak and ineffective person. He's also a low-energy person" \
            ", which I've said before. ... If he were president, it would just " \
            "be more of the same. He's got money from all of the lobbyists and " \
            "all of the special interests that run him like a puppet.")
    s.append("%s is weak on immigration and he’s weak on jobs. We need someone w" \
            "ho is going to make the country great again, and %s is not going t" \
            "o make the country great again.")
    s.append("I will build a great wall -- and nobody builds walls better than m" \
            "e, believe me -- and I'll build them very inexpensively. I will bu" \
            "ild a great, great wall on our southern border, and I will make %s" \
            " pay for that wall. Mark my words.")
    s.append("The other candidates -- like %s -- they went in, they didn't know " \
            "the air conditioning didn't work. They sweated like dogs... How ar" \
            "e they gonna beat ISIS? I don't think it's gonna happen.")
    stumpee = " ".join(args["args"])
    if stumpee.lower() == "trump":
        return "You can't stump the Trump"
    selection = random.randint(0, 24)
    return s[selection].replace("%s", stumpee)


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


