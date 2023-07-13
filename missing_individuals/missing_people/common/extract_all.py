from typing import List

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class ExtractMissingPeople:

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver

    LOADED_PAGES: int = 100
    URL: str = f"https://www.missingpeople.org.uk/appeal-search?loaded={LOADED_PAGES}"

    def accept_cookies_banner(self):

        cookie_banner = WebDriverWait(
            self.driver, 5).until(
                ec.visibility_of_any_elements_located(
                    (By.ID, 'cookie-law-info-bar')))[0]

        accept_button = WebDriverWait(
            cookie_banner, 5).until(
                ec.visibility_of_any_elements_located(
                    (By.TAG_NAME, 'a')))[-1]

        accept_button.click()

    def close_pop_up(self):

        pop_up = WebDriverWait(
            self.driver, 5).until(
                ec.visibility_of_any_elements_located(
                    (By.CLASS_NAME, 'close')))[0]

        pop_up.click()

    def extract_all_urls(self) -> List[str]:

        self.driver.get(url=self.URL)

        self.accept_cookies_banner()

        self.url_list = []
        all_content = WebDriverWait(
            self.driver, 5).until(
                ec.visibility_of_any_elements_located(
                    (By.CLASS_NAME, 'section__content')))

        all_a_tags = WebDriverWait(
            all_content[0], 5).until(
                ec.visibility_of_any_elements_located(
                    (By.TAG_NAME, 'a')))

        for url in all_a_tags:
            self.url_list.append(url.get_attribute("href"))

    def extract_all_data_from_urls(self) -> pd.DataFrame:

        self.df_full = pd.DataFrame()
        for url in self.url_list:

            self.driver.get(url=url)
            self.close_pop_up()

            self.item_dict = {}

            # Extract the main content
            main_content = WebDriverWait(
                self.driver, 5).until(
                    ec.visibility_of_any_elements_located(
                        (By.CLASS_NAME, 'main_content_cell')))[0]

            # Get name
            self.item_dict["NAME"] = WebDriverWait(
                main_content, 5).until(
                    ec.visibility_of_any_elements_located(
                        (By.TAG_NAME, 'h1')))[0].text

            item_content = WebDriverWait(
                main_content, 5).until(
                    ec.visibility_of_any_elements_located(
                        (By.TAG_NAME, 'li')))

            for item in item_content[:-2]:

                item_name = WebDriverWait(
                    item, 5).until(
                        ec.visibility_of_any_elements_located(
                            (By.TAG_NAME, 'h2')))[0].text
                item_value = WebDriverWait(
                        item, 5).until(
                            ec.visibility_of_any_elements_located(
                                (By.TAG_NAME, 'span')))[0].text

                self.item_dict[item_name] = item_value

        self.df_full = pd.concat(
            [self.df_full, pd.DataFrame(self.item_dict, index=[0])])

    def run(self):

        # Extract all URLs
        self.extract_all_urls()

        # Extract data frame
        self.extract_all_data_from_urls()
