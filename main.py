from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import os
import time
from scraper import DynamicScrapper as ds


def set_get_driver(headless=False, strDriverPath="drivers/firefox.exe"):
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options, executable_path=strDriverPath)
    return driver


def load_config_file(path="config.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        print("[-] Config file not found!")
        return None


def run():
    data = load_config_file()

    urls = []
    for item in data["countries"]:
        urls.append([data["url"][:len("https://apps.apple.com/")] + item["code"] +
                    "/"+data["url"][len("https://apps.apple.com/"):], item["code"]])

    for url, code in urls:
        driver = set_get_driver(
            headless=True, strDriverPath=data["driver_path"])
        scraper = ds("config.json", driver, url, code)
        scraper.run()
        time.sleep(0.2)


run()
