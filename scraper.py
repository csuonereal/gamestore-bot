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
                self.compare(self.convertor_check(row))
                self.convertor_control(row)
            else:
                print("no item found!")
            self.driver.close()
            self.driver.quit()
        except not KeyboardInterrupt:
            self.run()

    def compare(self, row):
        with open(f"data/{self.country}.json", "r") as f:
            old_values = json.load(f)
        print(old_values)
        print(row)
        if old_values != row:
            print(f"New game has been added in {self.country}.")
        else:
            print(f"All looks same in {self.country}.")

    def child2(self, row):
        r_row = []
        counter = 1
        for i in row:
            if counter == 1:
                first = i[str(counter)]
                counter += 1
            elif counter == 2:
                second = i[str(counter)]
                counter = 1
                m = {
                    "1": first,
                    "2": second,
                }
                r_row.append(m)
        return r_row

    def child3(self, row):
        r_row = []
        counter = 1
        for i in row:
            if counter == 1:
                first = i[str(counter)]
                counter += 1
            elif counter == 2:
                second = i[str(counter)]
                counter += 1
            elif counter == 3:
                third = i[str(counter)]
                counter = 1
                m = {
                    "1": first,
                    "2": second,
                    "3": third
                }
                r_row.append(m)
        return r_row

    def child4(self, row):
        r_row = []
        counter = 1
        for i in row:
            if counter == 1:
                first = i[str(counter)]
                counter += 1
            elif counter == 2:
                second = i[str(counter)]
                counter += 1
            elif counter == 3:
                third = i[str(counter)]
                counter += 1
            elif counter == 4:
                fourth = i[str(counter)]
                counter = 1
                m = {
                    "1": first,
                    "2": second,
                    "3": third,
                    "4": fourth
                }
                r_row.append(m)
        return r_row

    def convertor_control(self, row):
        if len(self.childs_XPATHS) == 2:
            self.convert_json(self.child2(row))
        elif len(self.childs_XPATHS) == 3:
            self.convert_json(self.child3(row))
        elif len(self.childs_XPATHS) == 4:
            self.convert_json(self.child4(row))
        else:
            print("no compatible convertor found!")
            print(row)
            sys.exit(0)

    def convertor_check(self, row):
        if len(self.childs_XPATHS) == 2:
            return self.child2(row)
        elif len(self.childs_XPATHS) == 3:
            return self.child2(row)
        elif len(self.childs_XPATHS) == 4:
            return self.child3(row)
        else:
            print("no compatible convertor found!")
            print(row)
            sys.exit(0)

    def convert_csv(self, row):
        print(row)
        df = pd.DataFrame(row)
        df.to_csv("data2.csv", index=False)

    def convert_json(self, row):
        with open(f"data/{self.country}.json", "w") as f:
            f.write(json.dumps(row))
