from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import csv
import sys
import json
import os
import time


class DynamicScrapper:
    def __init__(self, config_path, driver, url, country):
        self.country = country
        self.driver = driver
        self.data = DynamicScrapper.load_config_file(config_path)
        self.parent_XPATH = self.data["parent"]
        self.childs_XPATHS = self.data["childs"]
        self.driver_path = self.data["driver_path"]
        self.url = url

    @staticmethod
    def load_config_file(path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        else:
            raise Exception("config file not found!")

    def run(self):
        try:
            print(self.url)
            self.driver.get(self.url)
            time.sleep(0.2)
            row = []
            parents = self.driver.find_elements_by_xpath(self.parent_XPATH)
            if len(parents) > 0:
                for parent in parents:
                    for i in range(0, len(self.childs_XPATHS)):
                        obj = parent.find_element_by_xpath(
                            self.childs_XPATHS[i]).text
                        m = {f"{i+1}": obj}
                        row.append(m)
                self.compare(self.reformatter(row))
                self.convert_json(self.reformatter(row))
            else:
                print("no item found!")
            self.driver.close()
            self.driver.quit()
        except Exception as e:
            print(e)

    def compare(self, row):
        with open(f"data/{self.country}.json", "r") as f:
            old_values = json.load(f)
        print(old_values)
        print(row)
        if old_values != row:
            print(f"New game has been added in {self.country}.")
        else:
            print(f"All looks same in {self.country}.")

    def reformatter(self, row):
        r_row = []
        counter = 1
        values = []
        for i in row:
            if counter < len(self.childs_XPATHS):
                values.append(i[str(counter)])
                counter += 1
            else:
                values.append(i[str(counter)])
                counter = 1
                m = {}
                keys = range(0, len(self.childs_XPATHS))
                values_ = values
                for j in keys:
                    m[str(j+1)] = values_[j]
                r_row.append(m)
                values = []
        return r_row

    def convert_csv(self, row):
        print(row)
        df = pd.DataFrame(row)
        df.to_csv("data2.csv", index=False)

    def convert_json(self, row):
        with open(f"data/{self.country}.json", "w") as f:
            json.dump(row, f, ensure_ascii=False)
