from email import header
import time
from faker import Faker
from telethon.sync import *
from telethon.errors.rpcerrorlist import *
from colorama import Fore, init
from requests import Request, Response
import random, requests, datetime
init(autoreset=True);
config:dict = {
    "api_id": "2392599",
    "api_hash": "7e14b38d250953c8c1e94fd7b2d63550",
    "phone_numbers": [
        # "+50493609809"
    ],
    "sessions_path": "sessions/{0}",
    "code": {
        "delay": 5,
        "tries": 3
    }
};

preferredCountries = [
    "russia", 
    "congo", 
    "indonesia"
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
    
    def purchase(self, country:str, operator:str = "any", product:str = "telegram") -> dict:
        return self.sendRequest(self.urlWithPath("purchase").format(country=country, operator=operator, product=product), "GET", headers=self.headersTemplate).json();
    
    def cancelPurchase(self, id:str|int) -> dict:
        return self.sendRequest(self.urlWithPath("cancelPurchase").format(id=id), "GET", headers=self.headersTemplate).json();

    def purchaseData(self, id:str|int) -> dict:
        return self.sendRequest(self.urlWithPath("purchaseData").format(id=id), "GET", headers=self.headersTemplate).json();

m5sim = M5sim("eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzgzODYxMzcsImlhdCI6MTY0Njg1MDEzNywicmF5IjoiZjcxZGM0NjZlYWMwYjIyMjg3NjJmMTA2MWI1MWQ2YzQiLCJzdWIiOjc3NzI5M30.nDv9JXocsjkiwLHFjraXgYfX_9GYtDSN5RLnfVHhqFCkr2G2XrYO7p3IeYmIDt4LihIqFUpSyS52lbK9sJBJ4kwih-R2N4x03zpIeXqgwk3-fG7tz0EFZCI5gNq9GGqrFyCO0SM825XgdFkhHLh_vYDd6_TpYzxs8BU8T3BDLErZ_pGmtqRpRfXcOb9yaNmX74-GadhOmkOcEUbwAQxnKDS0e1tX9srkn-4T3shaMs4ISwV7DFRwBl4snAkL__yzTSgFkP0JhkWOsfKjvokm8Lh3TtVTg0BWjPR477VMy8qtnQMpnoZVLFhp6h7HalE1nAxk5tu_PV88BvDh0f2DNA");
class Actions:
    def __init__(self):
        m5sim.aboutMe(logMode=True)
        self.initializeModel1();

    def initializeModel1(self):
        while True:
            pref:dict = random.choice(purchasePrefences);
            phone:str = m5sim.purchase(pref["name"], pref["operator"], pref["product"])["phone"];
            client = TelegramClient(config["sessions_path"].format(phone), api_id=config["api_id"], api_hash=config["api_hash"]);
            client.connect();
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone);
                    code = self.waitForCode();
                    if (code == -1):
                        continue;
                    me = client.sign_up(phone=phone, code=code, first_name=actions.generateRandomUser());
                except (PhoneNumberBannedError, Exception) as e:
                    self.printException();
                    self.cancelPurchase();
                    continue;

    def currentTime(self) -> float | int:
        return datetime.datetime.now().timestamp();
    
    def waitForCode(self) -> int:
        code:int|str = -1;
        tried:int = 0;
        initTime:float = self.currentTime(); 
        while True:
            data:dict = m5sim.purchaseData(m5sim.lastPurchaseID);
            if (type(data["sms"])==list):
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

actions = Actions();



# firefox_options = webdriver.FirefoxOptions();
# firefox_options.add_argument('--headless');

# driver = webdriver.Firefox(service = Service('geckodriver.exe'), options=firefox_options);

# def getElementContent(xpathOfelement:str):
#     return driver.find_element(by=By.XPATH, value=xpathOfelement).text;
