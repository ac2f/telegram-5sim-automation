from faker import Faker
from telethon.sync import *
from telethon.errors.rpcerrorlist import *
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from colorama import Fore, init
import random, requests
from requests import Request, Response
init(autoreset=True);
url = "https://www.binance.com/tr/support/announcement/c-48";
delay = 60; # Seconds
config:dict = {
    "api_id": "2392599",
    "api_hash": "7e14b38d250953c8c1e94fd7b2d63550",
    "phone_numbers": [
        # "+50493609809"
    ],
    "sessions_path": "sessions/{0}"
};

purchasePrefence:dict = {
    "country": "russia",
    "operator": "any",
    "product": "telegram"
};

class M5sim:
    def __init__(self, apiKey:str, url:str = "https://5sim.net"):
        self.url = url;
        self.apiKey = apiKey;
        self.path = {
            "profileData": "/v1/user/profile",
            "purchase": '/v1/user/buy/activation/{country}/{operator}/{product}'
        }

    def urlWithPath(self, key:str) -> str:
        return f"{self.url}{self.path[key]}";

    def sendRequest(self, url:str|bytes, type:str, body:dict = {}, headers:dict = {}):
        type = type.lower();
        if (type=="get"):
            return requests.get(url, headers=headers);
        
    def aboutMe(self, logMode:bool = False):
        data:dict = self.sendRequest(self.urlWithPath("profileData"), "get", headers={"Authorization": f"Bearer {self.apiKey}"}).json(); 
        if (logMode):
            print(f"{Fore.LIGHTGREEN_EX}About 5sim.net account:")
            for item in data:
                print(f"> {Fore.LIGHTCYAN_EX}{item}  {' ' * (17 - len(str(item)))}:  {Fore.LIGHTRED_EX}{data[item][list(data[item])[0]] if type(data[item]) == dict else data[item]}")
        return data; 
    
    def purchase(self):
        self

class Actions:
    def __init__(self):
        self

    def bannedNumberAction(self, phone:str):
        self

    def generateRandomUser(self) -> str:
        return Faker().name().replace(" ", "") + str(random.randint(10000, 99999))

m5sim = M5sim("eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzgzODYxMzcsImlhdCI6MTY0Njg1MDEzNywicmF5IjoiZjcxZGM0NjZlYWMwYjIyMjg3NjJmMTA2MWI1MWQ2YzQiLCJzdWIiOjc3NzI5M30.nDv9JXocsjkiwLHFjraXgYfX_9GYtDSN5RLnfVHhqFCkr2G2XrYO7p3IeYmIDt4LihIqFUpSyS52lbK9sJBJ4kwih-R2N4x03zpIeXqgwk3-fG7tz0EFZCI5gNq9GGqrFyCO0SM825XgdFkhHLh_vYDd6_TpYzxs8BU8T3BDLErZ_pGmtqRpRfXcOb9yaNmX74-GadhOmkOcEUbwAQxnKDS0e1tX9srkn-4T3shaMs4ISwV7DFRwBl4snAkL__yzTSgFkP0JhkWOsfKjvokm8Lh3TtVTg0BWjPR477VMy8qtnQMpnoZVLFhp6h7HalE1nAxk5tu_PV88BvDh0f2DNA");
m5sim.aboutMe(True)
actions = Actions();

for phone in config["phone_numbers"]:
    client = TelegramClient(config["sessions_path"].format(phone), api_id=config["api_id"], api_hash=config["api_hash"]);
    client.connect();
    if not client.is_user_authorized():
        try:
            client.send_code_request(phone);
            me = client.sign_up(phone=phone, code=input(f'Enter the code that has sent to {phone}: '), first_name=actions.generateRandomUser());
        except PhoneNumberBannedError as e:
            print(f"Error \"{phone}\":  {Fore.LIGHTRED_EX}{e}");
            actions.bannedNumberAction(phone);
            continue;

# firefox_options = webdriver.FirefoxOptions();
# firefox_options.add_argument('--headless');

# driver = webdriver.Firefox(service = Service('geckodriver.exe'), options=firefox_options);

# def getElementContent(xpathOfelement:str):
#     return driver.find_element(by=By.XPATH, value=xpathOfelement).text;
