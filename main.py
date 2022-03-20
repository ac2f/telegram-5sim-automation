from email import header
from faker import Faker
from telethon.sync import *
from telethon.errors.rpcerrorlist import *
from colorama import Fore, init, Style
from requests import Request, Response
import random, requests, datetime
import os
import time
import shutil
init(autoreset=True);
config:dict = {
    "5sim": {
        "apiKey": ""
    },
    "api_id": "2392599",
    "api_hash": "7e14b38d250953c8c1e94fd7b2d63550",
    "phone_numbers": [
        # "+50493609809"
    ],
    "sessions_path": "sessions/{0}",
    "delayBeforeRetry": 10,
    "code": {
        "delay": 5,
        "tries": 3
    },
    "outfile": "verified-phones.txt"
};

preferredCountries = [
    "russia", 
    "congo", 
    "indonesia",
    "bulgaria",
    "india",
    "indonesia",
    "egypt"
];

purchasePrefences:dict = [
    {
        "country": country,
        "operator": "any",
        "product": "telegram"
    } for country in preferredCountries
];

class M5sim:
    def __init__(self, apiKey:str, url:str = "https://5sim.net"):
        if(apiKey == "" or apiKey == None or len(apiKey)<499):
            raise ValueError("Invalid \"apiKey\"");
        self.url = url;
        self.apiKey = apiKey;
        self.path = {
            "profileData": "/v1/user/profile",
            "purchase": '/v1/user/buy/activation/{country}/{operator}/{product}',
            "cancelPurchase": "/v1/user/cancel/{id}",
            "purchaseData": "/v1/user/check/{id}"
        };
        self.headersTemplate = {
            "Authorization": f"Bearer {self.apiKey}",
            "Accept": "application/json"
        };
        self.lastPurchaseID = None;

    def urlWithPath(self, key:str) -> str:
        return f"{self.url}{self.path[key]}";

    def sendRequest(self, url:str|bytes, type:str, body:dict = {}, headers:dict = {}):
        type = type.lower();
        if (type=="get"):
            return requests.get(url, headers=headers);
        
    def aboutMe(self, logMode:bool = False) -> dict:
        data:dict = self.sendRequest(self.urlWithPath("profileData"), "GET", headers=self.headersTemplate).json(); 
        if (logMode):
            print(f"{Fore.LIGHTGREEN_EX}About 5sim.net account:")
            for item in data:
                print(f"> {Fore.LIGHTCYAN_EX}{item}  {' ' * (17 - len(str(item)))}:  {Fore.LIGHTRED_EX}{data[item][list(data[item])[0]] if type(data[item]) == dict else data[item]}")
        return data; 
    
    def purchase(self, country:str, operator:str = "any", product:str = "telegram") -> dict | str:
        try:
            data:dict = self.sendRequest(self.urlWithPath("purchase").format(country=country, operator=operator, product=product), "GET", headers=self.headersTemplate).json();
            self.lastPurchaseID = data["id"];
            return data; 
        except Exception as e:
            return e;

    def cancelPurchase(self, id:str|int) -> dict:
        return self.sendRequest(self.urlWithPath("cancelPurchase").format(id=id), "GET", headers=self.headersTemplate).json();

    def purchaseData(self, id:str|int) -> dict:
        return self.sendRequest(self.urlWithPath("purchaseData").format(id=id), "GET", headers=self.headersTemplate).json();

m5sim = M5sim(config["5sim"]["apiKey"]);
class Actions:
    def __init__(self):
        for file in os.listdir("sessions"):
            os.remove(f"sessions/{file}");
        m5sim.aboutMe(logMode=True);
        self.initializeModel1();

    def initializeModel1(self):
        while True:
            pref:dict = random.choice(purchasePrefences);
            print(f"Buying a \"{Fore.LIGHTCYAN_EX}{pref['product']}{Fore.RESET}\" item from \"{Fore.LIGHTCYAN_EX}{pref['country']}{Fore.RESET}\" country.");
            buyData:dict = m5sim.purchase(pref["country"], pref["operator"], pref["product"])
            if (type(buyData) == requests.exceptions.JSONDecodeError):
                self.printException("Encountered while purchasing. Error", buyData);
                continue;
            phone:str = buyData["phone"];
            print(f"Successfully bought \"{Fore.LIGHTGREEN_EX}{phone}{Fore.RESET}\" from \"{Fore.LIGHTCYAN_EX}{pref['country']}{Fore.RESET}\" for \"{Fore.LIGHTMAGENTA_EX}{buyData['price']}{Fore.RESET}\" ruble(s)")
            client = TelegramClient(config["sessions_path"].format(phone), api_id=config["api_id"], api_hash=config["api_hash"]);
            client.connect();
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone);
                    code = self.waitForCode();
                    if (code == -1):
                        continue;
                    client.sign_up(phone=phone, code=code, first_name=actions.generateRandomUser());
                    print(f"{Fore.LIGHTGREEN_EX}Successfully registered with using \"{Fore.WHITE}{phone}{Fore.LIGHTGREEN_EX}\"");
                    shutil.copy(config["sessions_path"].format(phone)+".session", "verified-sessions/");
                    self.appendDataToFile(phone);
                    client.disconnect();
                except (PhoneNumberBannedError, Exception) as e:
                    print(f"{Fore.LIGHTBLUE_EX}Cancelling purchase \"{Fore.LIGHTGREEN_EX}{phone}{Fore.RESET}\"{Fore.LIGHTBLUE_EX}. Purchase ID: \"{Fore.RESET}{buyData['id']}{Fore.LIGHTBLUE_EX}\"");
                    self.printException(f"Error \"{phone}\"", e);
                    self.cancelPurchase();
            time.sleep(config["delayBeforeRetry"]);

    def currentTime(self) -> float | int:
        return datetime.datetime.now().timestamp();
    
    def waitForCode(self) -> int:
        code:int|str = -1;
        tried:int = 0;
        initTime:float = self.currentTime(); 
        while True:
            data:dict = m5sim.purchaseData(m5sim.lastPurchaseID);
            if (len(data["sms"]) > 0):
                code = data["sms"][0]["code"];
                break;
            if (self.currentTime()-initTime < config["code"]["delay"] and tried < config["code"]["tries"]):
                self.cancelPurchase();
                break;
            tried += 1;
            time.sleep(config["code"]["delay"]);
        return code;

    def printException(self, msg:str, err:Exception):
        print(f"{msg}:  {Fore.LIGHTRED_EX}{err}");

    def cancelPurchase(self):
        m5sim.cancelPurchase(m5sim.lastPurchaseID);
    
    def generateRandomUser(self) -> str:
        return Faker().name().replace(" ", "") + str(random.randint(10000, 99999))
    
    def appendDataToFile(self, data:str):
        with open(config["outfile"], "a+", encoding="utf-8") as f:
            f.write(data + "\n");
            f.close();

actions = Actions();



# firefox_options = webdriver.FirefoxOptions();
# firefox_options.add_argument('--headless');

# driver = webdriver.Firefox(service = Service('geckodriver.exe'), options=firefox_options);

# def getElementContent(xpathOfelement:str):
#     return driver.find_element(by=By.XPATH, value=xpathOfelement).text;
