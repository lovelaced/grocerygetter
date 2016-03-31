# listbot

## IRC bot which performs various SUPER USEFUL functions

**Usage:** python irc.py config.json

Commands can be seen by typing .help.

prefers python 3.5

Config Syntax
```
{
    "server" : "irc.rizon.net", <- server address
    "port" : 6697, <- server port
    "bot_nick" : "listbot", <- nick of bot, 0 for random nick
    "channels" : ["#bots", "#test"], <- list of channels to connect to
    "password" : "bot123", <- password of bot, 0 for no password
    "prefix" : "." <- command prefix so commands start with $prefix
}
```

