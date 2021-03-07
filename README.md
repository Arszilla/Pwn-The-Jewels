[![Python][1]][2]
[![License][3]][4]
[![Twitter][5]][6]

<p align="center">
    <img src="./images/Pwn%20The%20Jewels%20Banner.png">
</p>

## Introduction
`Pwn The Jewels` is a Discord bot that utilizes *36" Cyber Kill Chain* &copy; to catch malicious *Pew Pew Pews* 
&copy;. Jokes aside, `Pwn The Jewels` is a project that was created to help cyber threat analysts (CTIs) with various 
tasks, mainly monitor feeds.  Originally, this bot was written back in late October 2019, but has been repurposed for 
CTI after [BushidoToken][7]'s [blog post][8], where he talked about how to turn Discord into a CTI dashboard.

In BushidoToken's blog post, it is quite noticeable that he had to use multiple bots to monitor various feeds, with 
the majority of the bots being closed source and having paywalled features. As a person that hates such paywalls, I 
decided to write my own and release it to the public to combat this annoyance, with the key difference being no 
paywalls and ability to self-host.

## Setup & Execution
After cloning the repository, configure your `config.yml` to assign your API keys and settings:

### Mandatory Values
- Discord:
  - [Discord API Bot Key][9]
  - Channel IDs. You can get this by right-clicking a channel name and pressing `Copy ID`.
- [Reddit API][10]:
  - Client ID
  - Secret
- [Twitter API][11]:
  - Access Token
  - Access Token Secret
  - Consumer Key
  - Consumer Secret
- [Youtube API v3][12]:
  - API key

### Optional Values
- Bot prefix
- Profile and footer picture
- Database name

After setting the [mandatory values](#mandatory-settings), you can either run the bot via `pipenv` or via Docker:

### Pipenv
```
$ sudo apt install python3-pip
$ sudo pip3 install pipenv
$ sudo pipenv install
$ pipenv shell
$ pipenv run bot
```

### Docker
```
$ sudo apt install docker docker-compose
$ sudo groupadd docker
$ sudo usermod -aG docker ${USER}
$ su -s ${USER}
$ docker build -t pwnthejewels .
$ docker run pwnthejewels &
```

## Available Commands
| help            | Displays the help menu                                                                                                                                                              |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| clear           | Clears a given amount of messages from the channel the command was invoked in.<br><br>Example usage:  `$clear <amount>`                                                             |
| addrss          | Add a RSS feed to the database.<br><br>Example usage: `$addrss <url>`                                                                                                               |
| removerss       | Remove a RSS feed from the database.<br><br>Example usage: `$removerss <url>`                                                                                                       |
| addalert        | Add a Google Alerts RSS feed to the database.<br><br>Example usage: `$addalert <url>`                                                                                               |
| removealert     | Remove a Google Alerts RSS feed from the database.<br><br>Example usage: `$removealert <url>`                                                                                       |
| addsubreddit    | Add a subreddit to the database. The `/r/` should **NOT** be included.<br><br>Example usage: `$addsubreddit <subreddit-name>`                                                       |
| removesubreddit | Remove a subreddit from the database. The `/r/` should **NOT** be included.<br><br>Example usage: `$addsubreddit <subreddit-name>`                                                  |
| addtelegram     | Add a Telegram RSS feed to the database.<br><br>Example usage: `$addtelegram <url>`                                                                                                 |
| removetelegram  | Remove a Telegram RSS feed from the database.<br><br>Example usage: `$removetelegram <url>`                                                                                         |
| addtweeter      | Add a Twitter user to the database. The `@` should **NOT** be included.<br><br>Example usage: `$addtweeter <username>`                                                              |
| removetweeter   | Remove a Twitter user from the database. The `@` should **NOT** be included.<br><br>Example usage: `$removetweeter <username>`                                                      |
| enablerts       | Enable monitoring for retweets for a given username in the database. By default this is disabled. The `@` should **NOT** be included.<br><br>Example usage: `$enablerts <username>` |
| disablerts      | Disable monitoring for retweets for a given username in the database. The `@` should **NOT** be included.<br><br>Example usage: `$disablerts <username>`                            |
| addchannel      | Add a YouTube channel to the database.<br><br>Example usage: `$addchannel <channel-url>`                                                                                            |
| removechannel   | Remove a YouTube channel from the database.<br><br>Example usage: `$removechannel <channel-url>`                                                                                    |                                                                                |

## Roadmap/TODOs
I plan to expand the capabilities of the bot further as time goes on. The following is a ist of features I hope to 
implement in the near future (listed in no specific order):

- Basic file analysis via `checksec.py`
- Have I Been Pwned API
- Reminders
- Twitch monitoring
- VirusTotal API

Suggestions/Requests are more than welcome. If you'd like to suggest a feature, be sure to submit a `Feature Request` 
in the Issues tab of the repository.

## Donations
Donations are more than welcome. You can either donate to just thank me or encourage me to work further on the 
project. Because PayPal ceased its operations in Turkey back in 2016, I sadly can't take PayPal donations. As a 
result, cryptocurrencies are my main choice of donations. If you'd like to donate, you can donate with your choice of 
cryptocurrency at the following addresses:

- Bitcoin:      `bc1qfp2a7pncxvq3s9qgtj0fp7k6v5rzy8g763u7uk`
- Bitcoin Cash: `qz3s06xm9j6cj26qavstykwysf3xs92l3ymjpvut88`
- DogeCoin:     `DNPBgj2JVgYm17h8ybxkpYmC2LZmL91pUs`
- Ethereum:     `0x3FB9505DA434Ce308880261acbe56A4e321DdEFC`
- Litecoin:     `LRrcsYvbSnQoFmR3H8nYTtXYM8r2ZU14eU`
- Monero:       `47cyUEhzoakWsQUWme4zrJ5yKbU31TJu57DmySnGmGQFCjQgrYvG1EAUPzwVFQQJqBbBuhPXXKcT1Uu2krS2Dn7wNXHvbGx`
- Ripple:       `rUT1G4DT1kCYamsh1AoQcMvcN29PcyPWP1`

If you can't see your cryptocurrency of choice here, please don't hesitate to contact me on [Twitter][6] so I can 
sort out alternative cryptocurrencies.

## Disclaimers
- The project's name is a parody and a homage to [*Run The Jewels*][13].
- *36" Cyber Kill Chain* is a parody and a reference to *Run The Jewels*' song, [*36" Chain*][14]
- *Pew Pew Pews* is a parody and a reference to *Run The Jewels*' song, [*Pew Pew Pew (ft. DJ QBert)*][15]
- The logo used in the bot and the banner was created by the Redditor [/u/Rant423][16] in [/r/runthejewels][17].

[1]:    https://img.shields.io/badge/Python-3.9.2-yellow.svg?color=blue&logo=python&logoColor=white
[2]:    https://www.python.org/download/
[3]:    https://img.shields.io/github/license/Arszilla/Pwn-The-Jewels?color=orange&logo=github
[4]:    https://github.com/Arszilla/Pwn-The-Jewels/blob/master/LICENSE
[5]:    https://img.shields.io/twitter/url?label=Twitter&style=flat-square&url=https%3A%2F%2Ftwitter.com%2FArszilla?color=blue&logo=Twitter
[6]:    https://twitter.com/Arszilla
[7]:    https://twitter.com/BushidoToken
[8]:    https://blog.bushidotoken.net/2021/02/using-discord-server-as-personal-cti.html
[9]:    https://discord.com/developers/
[10]:   https://www.reddit.com/prefs/apps/
[11]:   https://developer.twitter.com/
[12]:   https://developers.google.com/youtube/v3
[13]:   https://www.youtube.com/channel/UCeveumRTn2o--9j1Xz2KUCQ
[14]:   https://www.youtube.com/watch?v=c_rwa4ZbKgA
[15]:   https://www.youtube.com/watch?v=gw9-F69EltY
[16]:   https://www.reddit.com/user/Rant423
[17]:   https://www.reddit.com/r/runthejewels/comments/gvx9vs/to_celebrate_rtj4/
