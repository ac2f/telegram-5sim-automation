from email import header
from faker import Faker
from telethon.sync import TelegramClient, events;
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
        "apiKey": "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzgzODYxMzcsImlhdCI6MTY0Njg1MDEzNywicmF5IjoiZjcxZGM0NjZlYWMwYjIyMjg3NjJmMTA2MWI1MWQ2YzQiLCJzdWIiOjc3NzI5M30.nDv9JXocsjkiwLHFjraXgYfX_9GYtDSN5RLnfVHhqFCkr2G2XrYO7p3IeYmIDt4LihIqFUpSyS52lbK9sJBJ4kwih-R2N4x03zpIeXqgwk3-fG7tz0EFZCI5gNq9GGqrFyCO0SM825XgdFkhHLh_vYDd6_TpYzxs8BU8T3BDLErZ_pGmtqRpRfXcOb9yaNmX74-GadhOmkOcEUbwAQxnKDS0e1tX9srkn-4T3shaMs4ISwV7DFRwBl4snAkL__yzTSgFkP0JhkWOsfKjvokm8Lh3TtVTg0BWjPR477VMy8qtnQMpnoZVLFhp6h7HalE1nAxk5tu_PV88BvDh0f2DNA"
    },
    "api_id": "2392599",
    "api_hash": "7e14b38d250953c8c1e94fd7b2d63550",
    "register_sessions_path": "registered_sessions/{0}",
    "login_sessions_path": "loggingin_sessions/{0}",
    "verified_sessions_path": "C:\\Users\\user\\Desktop\\HawkTelegramBot\\HawkTelegramBotSourcePrivate\\sessions\\{0}",
    "delayBeforeRetry": 10,
    "retryDelayWhenError": 5,
    "code": {
        "delay": 10,
        "tries": 5
    },
    "outfile": "C:\\Users\\user\\Desktop\\HawkTelegramBot\\HawkTelegramBotSourcePrivate\\phone.csv"
};

preferredCountries = [
    "turkey",
    "russia", 
    "congo",
    "indonesia",
    "bulgaria",
    "india",
    "indonesia",
    "egypt",
    "cyprus",
    "venezuela",
    "uganda",
    "malawi"
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
        data:dict = self.sendRequest(self.urlWithPath("purchase").format(country=country, operator=operator, product=product), "GET", headers=self.headersTemplate);
        try:
            data = data.json();
            self.lastPurchaseID = data["id"];
            return data;
        except Exception as e:
            if ("no free phones" in str(e)):
                raise e;
            print(f"Retrying cause of {Fore.LIGHTRED_EX}{e}{Fore.RESET}\nDELAY: {config['retryDelayWhenError']} seconds");
            time.sleep(config["retryDelayWhenError"]);
            return self.purchase(country=country, operator=operator, product=product);

    def cancelPurchase(self, id:str|int) -> dict:
        data = self.sendRequest(self.urlWithPath("cancelPurchase").format(id=id), "GET", headers=self.headersTemplate);
        try:
            return data.json();
        except Exception as e:
            print(f"Retrying cause of {Fore.LIGHTRED_EX}{e}{Fore.RESET}\nDELAY: {config['retryDelayWhenError']} seconds");
            time.sleep(config["retryDelayWhenError"]);
            return self.cancelPurchase(id);

    def purchaseData(self, id:str|int) -> dict:
        data = self.sendRequest(self.urlWithPath("purchaseData").format(id=id), "GET", headers=self.headersTemplate);
        try:
            return data.json();
        except Exception as e:
            print(f"Retrying cause of {Fore.LIGHTRED_EX}{e}{Fore.RESET}\nDELAY: {config['retryDelayWhenError']} seconds");
            time.sleep(config["retryDelayWhenError"]);
            return self.purchaseData(id);

m5sim = M5sim(config["5sim"]["apiKey"]);
class Actions:
    def __init__(self):
        for file in os.listdir(config["register_sessions_path"].format("")):
            os.remove(config["register_sessions_path"].format(file));
        m5sim.aboutMe(logMode=True);
        self.initializeModel1();

    def initializeModel1(self):
        while True:
            pref:dict = random.choice(purchasePrefences);
            print(f"Buying a \"{Fore.LIGHTCYAN_EX}{pref['product']}{Fore.RESET}\" item from \"{Fore.LIGHTCYAN_EX}{pref['country']}{Fore.RESET}\" country.");
            try:
                buyData:dict = m5sim.purchase(pref["country"], pref["operator"], pref["product"])
                if (type(buyData) == requests.exceptions.JSONDecodeError):
                    self.printException("Encountered while purchasing. Error", buyData);
                    continue;
                phone:str = buyData["phone"];
                print(f"Successfully bought \"{Fore.LIGHTGREEN_EX}{phone}{Fore.RESET}\" from \"{Fore.LIGHTCYAN_EX}{pref['country']}{Fore.RESET}\" for \"{Fore.LIGHTMAGENTA_EX}{buyData['price']}{Fore.RESET}\" ruble(s)")
                client = TelegramClient(config["register_sessions_path"].format(phone), api_id=config["api_id"], api_hash=config["api_hash"]);
                print(f"{Fore.LIGHTYELLOW_EX}The phone number \"{Fore.LIGHTGREEN_EX}{phone}{Fore.RESET}{Fore.LIGHTYELLOW_EX}\" is available. Waiting for code to be received..");
                client.connect();
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone);
                        code = self.waitForCode();
                        if (code == -1):
                            continue;
                        client.sign_up(phone=phone, code=code, first_name=self.generateRandomUser());
                        print(f"{Fore.LIGHTGREEN_EX}Successfully registered with using \"{Fore.WHITE}{phone}{Fore.LIGHTGREEN_EX}\"");
                        client.session.save_entities = True;
                        client.session.save();
                        shutil.copy(config["register_sessions_path"].format(phone)+".session", config["verified_sessions_path"].format(phone.replace("+", ""))+".session");
                        print(f"{Fore.LIGHTGREEN_EX}Successfully registered and signed in. Session file can be found at \"{Fore.LIGHTMAGENTA_EX}{config['verified_sessions_path'].format(phone)}.session{Fore.LIGHTGREEN_EX}\"")
                        self.appendDataToFile(phone); 
                    except FileNotFoundError as e:
                        self.printException("", e)
                        continue;
                    except (PhoneNumberBannedError, Exception) as e:
                        print(f"{Fore.LIGHTYELLOW_EX}Cancelling purchase \"{Fore.LIGHTGREEN_EX}{phone}{Fore.RESET}\"{Fore.LIGHTYELLOW_EX}. Purchase ID: \"{Fore.RESET}{buyData['id']}{Fore.LIGHTYELLOW_EX}\"");
                        self.printException(f"Error \"{phone}\"", e);
                        self.cancelPurchase();
                client.disconnect();

                time.sleep(config["delayBeforeRetry"]);
            except Exception as e:
                self.printException("Error: ", e);

    def currentTime(self) -> float | int:
        return datetime.datetime.now().timestamp();
    
    def waitForCode(self, smsIndex:int = 0) -> int:
        code:int|str = -1;
        tried:int = 0;
        initTime:float = self.currentTime(); 
        while True:
            data:dict = m5sim.purchaseData(m5sim.lastPurchaseID);
            print(f"Waiting for code to be received..");
            if (len(data["sms"]) > smsIndex):
                print(f"{Fore.LIGHTGREEN_EX}Code received!");
                code = data["sms"][smsIndex]["code"];
                break;
            if (self.currentTime()-initTime > config["code"]["delay"] and tried > config["code"]["tries"]):
                print(f"{Fore.LIGHTRED_EX}Max wait time exceeded! Cancelling purchase..");
                self.cancelPurchase();
                break;
            tried += 1;
            time.sleep(config["code"]["delay"]);
        return code;

    def printException(self, msg:str, err:Exception):
        print(f"{msg}:  {Fore.LIGHTRED_EX}{err}");

    def cancelPurchase(self):
        m5sim.cancelPurchase(m5sim.lastPurchaseID);
        print(f"{Fore.LIGHTYELLOW_EX}Successfully cancelled purchase");
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
