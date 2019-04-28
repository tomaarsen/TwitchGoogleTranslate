
from TwitchWebsocket import TwitchWebsocket
from googletrans import Translator
import random, time, json, requests

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Settings:
    def __init__(self, bot):
        try:
            # Try to load the file using json.
            # And pass the data to the GoogleTranslate class instance if this succeeds.
            with open("settings.txt", "r") as f:
                settings = f.read()
                data = json.loads(settings)
                bot.set_settings(data["Host"],
                                data["Port"],
                                data["Channel"],
                                data["Nickname"],
                                data["Authentication"],
                                data["UseProxies"],
                                data["MaxMessageLength"],
                                data["Cooldown"],
                                data["AmountOfTranslations"],
                                data["Languages"]
                                )
        except ValueError:
            raise ValueError("Error in settings file.")
        except FileNotFoundError:
            # If the file is missing, create a standardised settings.txt file
            # With all parameters required.
            with open("settings.txt", "w") as f:
                standard_dict = {
                                    "Host": "irc.chat.twitch.tv",
                                    "Port": 6667,
                                    "Channel": "#<channel>",
                                    "Nickname": "<name>",
                                    "Authentication": "oauth:<auth>",
                                    "UseProxies": False,
                                    "MaxMessageLength": 150,
                                    "Cooldown": 10,
                                    "AmountOfTranslations": 3,
                                    "Languages": ["Hawaiian"]
                                }
                f.write(json.dumps(standard_dict, indent=4, separators=(",", ": ")))
                raise ValueError("Please fix your settings.txt file that was just generated.")
        
        try:
            # Try to load the file using json.
            # And pass the data to the GoogleTranslate class instance if this succeeds.
            with open("languages.txt", "r") as f:
                languages = f.read()
                data = json.loads(languages)
                bot.set_languages(data)
        except ValueError:
            raise ValueError("Error in languages file.")
        except FileNotFoundError:
            # If the file is missing, create a standardised settings.txt file
            # With all parameters required.
            with open("languages.txt", "w") as f:
                standard_dict = {
                                    "en": "english"
                                }
                f.write(json.dumps(standard_dict, indent=4, separators=(",", ": ")))
                raise ValueError("Please add to your languages.txt file that was just generated.")

def pprint(code, msg=None):
    print("{:<20}: {}".format("[" + code + "]", msg if msg != None else ""))

class Languages:
    # Simple data structure to store name and id of a language.
    def __init__(self, name, id):
        self.name = name
        self.id   = id

class GoogleTranslate:
    def __init__(self):
        # None valuse are to be overridden by Settings
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.use_proxies = None
        self.message_length = None
        self.raw_languages = None
        
        # For retries 
        self.error_counter = 0

        # Variables used for cooldown
        self.prev_message_t = -1
        self.cooldown = None

        # Amount of languages that will be translated to, ignoring English as the final language and the initial language. An amount of 3 would be:
        # Dutch -> Khmer -> Latin -> Xhosa -> English
        # This amount is only used when the "Languages" is empty
        self.amount = None

        # Variable for holding a potential chain of fixed languages to chain through
        self.fixed = None

        # Standard URL
        self.url = "translate.google.com"

        # Set t, which may be overridden by a version using proxies.
        self.t = Translator(service_urls=[
            self.url
        ])

        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

        # All languages which can be randomly chosen by the bot.
        # Remove English so we can put English as the first index, 
        # without having a duplicate
        # Note, add more languages to this list to prevent them from being randomly picked by the bot.
        removed_languages = ["en"]

        # Create more convenient storage for all languages that can be chosen.
        self.languages = [Languages("English", "en")]
        for key in self.raw_languages:
            if key not in removed_languages:
                self.languages.append(Languages(self.raw_languages[key].capitalize(), key))
        
        # Set fixed to lower, to prevent case mismatches
        self.fixed = [l.lower() for l in self.fixed]
        # Set fixed languages which are used in a chain when FixedLanguages=true in the settings.
        self.fixed_languages = []
        for lan in self.languages:
            if lan.name.lower() in self.fixed or lan.id in self.fixed:
                self.fixed_languages.append(lan)
        
        if len(self.fixed) != len(self.fixed_languages):
            print("Warning, not all languages entered in \"Languages\" were recognised.")
        
        self.fixed_languages += [self.languages[0]]
        self.get_fixed_languages = lambda: self.fixed_languages 

        # Standard setup for the TwitchWebsocket.
        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability="tags",
                                  live=True)
        self.ws.start_bot()
        
    def proxy_init(self):
        self.ua = UserAgent()
        self.proxies = set()
        self.get_proxies()
        self.update_translator()

    def set_settings(self, host, port, chan, nick, auth, use_proxies, message_length, cooldown, amount, fixed):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth
        self.use_proxies = use_proxies
        self.message_length = message_length
        self.cooldown = cooldown
        self.amount = amount
        self.fixed = fixed

        if self.use_proxies:
            self.proxy_init()

    def set_languages(self, data):
        self.raw_languages = data

    def message_handler(self, m):

        if m.type == "JOIN" and m.user == "cubieb0t":
            pprint("Start", m.params + "\n")

        if m.type == "PRIVMSG":
            if m.message.startswith("!translate ") and len(m.message) < self.message_length and self.prev_message_t + self.cooldown < time.time():
                # Set initial message as m.message
                message = " ".join(m.message.split(" ")[1:])
                pprint("Initial", message)

                # Update for cooldown
                self.prev_message_t = time.time()

                # Get language path and output message
                path, message = self.translate_message(message)
                if len(message) == 0:
                    return
                pprint("Path", path + "\n")

                self.ws.send_message(f"@{m.tags['display-name']}: {message}")

            if m.message.startswith("!help"):
                self.ws.send_message("The input sentence is taken and translated in a chain, eg: Any Language -> " + " -> ".join([l.name for l in (self.get_fixed_languages() if len(self.fixed_languages) > 0 else self.get_random_languages())]))

    def translate_message(self, message_in):
        # Start is the initial language, which we do not know in advance
        start = str()

        # Create copy so input message is still available
        message = message_in

        # Get list of languages to translate through
        if len(self.fixed_languages) > 0:
            path = self.get_fixed_languages()
        else:
            path = self.get_random_languages()
        
        # Set starting message as "auto"
        s = "auto"
        for l in path:
            d = l.id
            result = self.translate(message, s, d)
            
            # Set the initial language
            try:
                if s == "auto":
                    start = self.raw_languages[result.src].capitalize()
            except:
                start = "English"
            
            # If a translation failed, we will try again 20 times before giving up.
            if result is None:
                if self.use_proxies:
                    # Update the proxy used when the message breaks.
                    self.update_translator()
                print("Error Occurred. Result is None")

                if self.error_counter < 20:
                    # Set prev_message to -1 to make sure the cooldown doesn't prevent it from working.
                    self.prev_message_t = -1
                    self.error_counter += 1
                    return self.translate_message(message_in)
                return ("", "")

            self.error_counter = 0
            message = result.text
            pprint(f"To {l.name}", message)
            
            # Update source for next iteration
            s = d

        return (start + " -> " + " -> ".join([l.name for l in path]), message)

    def get_random_languages(self):
        # Randoms from 1 onwards to prevent English from being picked
        languages = [self.languages[random.randint(1, len(self.languages) - 1)] for i in range(self.amount)]
        
        # Adds English for final translation
        languages.append(self.languages[0])
        return languages

    def translate(self, message, s, d):
        try:
            result = self.t.translate(message, src=s, dest=d)
            return result
        except Exception as e:
            pprint("Error T", e)
    
    def get_proxies(self):
        proxies_req = Request("https://www.sslproxies.org/")
        proxies_req.add_header("User-Agent", self.ua.random)
        proxies_doc = urlopen(proxies_req).read().decode("utf8")

        soup = BeautifulSoup(proxies_doc, "html.parser")
        proxies_table = soup.find(id="proxylisttable")

        # Save proxies in the array
        for row in proxies_table.tbody.find_all("tr"):
            self.proxies.add(row.find_all("td")[0].string + ":" + row.find_all("td")[1].string)
        pprint("Add", str(len(self.proxies)) + " Proxies left.")

    def update_translator(self):
        while True:
            # Grab a proxy
            p = self.proxies.pop()
            pprint("Try", p)
            try:
                # Try to perform a GET request using this proxy.
                s = requests.Session()
                s.proxies = {
                    "http": p
                }
                s.get("http://icanhazip.com/s", timeout=3.05)
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
                # If the proxy failed and there are no more proxies left, fetch more.
                pprint("Remove", str(len(self.proxies)) + " Proxies left.")
                if len(self.proxies) == 0:
                    self.get_proxies()
            else:
                # If the GET request succeeded, we will update our Translator object with the new proxy.
                pprint("Success")
                self.t = Translator(service_urls=[
                    self.url
                ], proxies={
                    "http": p
                })

                if len(self.proxies) == 0:
                    self.get_proxies()
                return
    
if __name__ == "__main__":
    GoogleTranslate()
