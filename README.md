# TwitchGoogleTranslate
Twitch Chat bot which uses Google Translate in a chain to modify input sentences into ridiculous new sentences.

---
# Explanation
When the bot has started, it will start listening to chat messages in the channel listed in the settings.txt file. If any message starts with "!translate ", the bot will take the remainder of that message, and randomly choose a certain amount of languages. (This amount is also defined in the settings.txt file)

The bot will translate the remainder from the initial language (does not need to be English) to all languages that were randomly picked, in a chain. At the end, it will translate the sentence back to English, and it will be printed out in the Twitch chat.

# Example

The console when sending the message "!translate How much wood could a woodchuck chuck, if a woodchuck could chuck wood?" in Twitch chat 3 times:

<pre>
[Start]             : #cubiedev

[Initial]           : <b>How much wood could a woodchuck chuck, if a woodchuck could chuck wood?</b>
[To Cebuano]        : Pila ka kahoy ang mahimo nga usa ka kahoy nga kahoy, kung ang usa ka kahoy nga kahoy makagisi sa kahoy?
[To Nepali]         : कति काठको रूख हुन सक्छ, यदि रूखले रूख छोड्छ भने?
[To Thai]           : มีไม้เท่าไหร่ถ้าต้นไม้ออกจากต้นไม้?
[To English]        : <b>How much wood is there if the tree leaves the tree?</b>
[Path]              : <b>English -> Cebuano -> Nepali -> Thai -> English</b>

[Initial]           : <b>How much wood could a woodchuck chuck, if a woodchuck could chuck wood?</b>
[To Finnish]        : Kuinka paljon puuta voisi hakata puuhihnaa, jos puukouru voisi hakata puuta?
[To Chinese (traditional)]: 如果木屑可以切割木材，木材可以切割多少木材？
[To Kyrgyz]         : жыгач отун кесип мүмкүн болсо, анда канча жыгач устун кесип болот?
[To English]        : <b>If he can cut firewood wood boards can be cut?</b>
[Path]              : <b>English -> Finnish -> Chinese (traditional) -> Kyrgyz -> English</b>

[Initial]           : <b>How much wood could a woodchuck chuck, if a woodchuck could chuck wood?</b>
[To Xhosa]          : Ubungakanani umthi onokuthi ube ngumthi we-woodchuck chuck, ukuba i-woodchuck yayingakwazi ukuxubha ukhuni?
[To Uzbek]          : Yog'och daraxti yog'ochni cho'ktirolmasa, daraxt daraxt daraxti qanday daraxtga aylanishi mumkin?
[To Shona]          : Ndeupi rudzi rwemuti unogona kutendeuka mumuti kana muti wehuni usingadziki huni?
[To English]        : <b>What kind of tree can turn into a tree or wood tree without wood?</b>
[Path]              : <b>English -> Xhosa -> Uzbek -> Shona -> English</b>
</pre>
---

# Requirements
* googletrans
* requests
* bs4
* fake_useragent

Install these using `pip install ...`

* TwitchWebsocket

Install this using `pip install git+https://github.com/CubieDev/TwitchWebsocket.git`

This last library is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "UseProxies": false,
    "Cooldown": 10,
    "AmountOfTranslations": 3,
    "Languages": [
        "Hawaiian"
    ]
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| UseProxies           | Whether Proxies should be used                                    | False (recommended) |
| Cooldown             | How many seconds inbetween messages that the bot should translate | 10 |
| AmountOfTranslations | How many languages the bot should choose to translate through     | 3 (Recommended) |
| Languages            | The chain of languages which will be translated through. If this list has languages, these languages will always be used in the listed order. If this list is empty, an amount of random languages will be chosen. | ["Hawaiian"] (recommended) |

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# Other Twitch Bots

* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchRhymeBot](https://github.com/CubieDev/TwitchRhymeBot)
* [TwitchCubieBotGUI](https://github.com/CubieDev/TwitchCubieBotGUI)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchUrbanDictionary](https://github.com/CubieDev/TwitchUrbanDictionary)
* [TwitchWeather](https://github.com/CubieDev/TwitchWeather)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchMMLevelPickerGUI](https://github.com/CubieDev/TwitchMMLevelPickerGUI) (Mario Maker 2 specific bot)
* [TwitchMMLevelQueueGUI](https://github.com/CubieDev/TwitchMMLevelQueueGUI) (Mario Maker 2 specific bot)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Not designed for non-programmers)
