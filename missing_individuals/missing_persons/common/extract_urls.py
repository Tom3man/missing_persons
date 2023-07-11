from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait


class ExtractMissingPersonsUrls:
    """
    A class to extract missing persons' URLs from a website.
    """

    URL: str = "https://missingpersons.police.uk/en-gb/case-search/"

    def __init__(self, driver: webdriver.Chrome):
        """
        Initializes the ExtractMissingPersonsUrls class by setting up the Selenium driver and navigating to the URL.
        """
        self.driver = driver
        self.case_urls = []

        self.driver__init__()

    def driver__init__(self):
        self.driver.get(self.URL)
        self._ignore_warning_box()
        self._expand_to_100_items()

    def _ignore_warning_box(self):
        """
        Ignores the warning dialog box that may appear on the page.
        """
        dialog_box = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_any_elements_located((By.CLASS_NAME, 'Dialog')))[0]
        close_tag = WebDriverWait(dialog_box, 5).until(
            ec.visibility_of_any_elements_located((By.TAG_NAME, 'a')))[-1]
        close_tag.click()

    def _expand_to_100_items(self):
        """
        Expands the number of items per page to 100.
        """
        dropdown_per_page = Select(WebDriverWait(self.driver, 5).until(
            ec.visibility_of_any_elements_located((By.ID, 'setPerPage')))[-1])
        dropdown_per_page.select_by_visible_text("100 per page")

    def return_page_urls(self):
        """
        Returns a list of URLs for each page in the pagination.
        """
        urls_banner = WebDriverWait(self.driver, 5).until(
            ec.visibility_of_any_elements_located((By.CLASS_NAME, 'Pagination')))[0]
        page_urls_tags = WebDriverWait(urls_banner, 5).until(
            ec.visibility_of_any_elements_located((By.TAG_NAME, 'a')))[1:-2]
        self.page_urls = [self.driver.current_url]
        for tag in page_urls_tags:
            href = tag.get_attribute("href")
            if href:
                self.page_urls.append(href)

    def extract_case_urls(self) -> List[str]:
        """
        Extracts case URLs from each page and appends them to the case_urls list.
        """

        self.return_page_urls()
        for url in self.page_urls:

            self.driver.get(url)
            case_grid = WebDriverWait(self.driver, 5).until(
                ec.visibility_of_any_elements_located((By.CLASS_NAME, 'CaseGrid')))[0]
            case_url_tags = WebDriverWait(case_grid, 5).until(
                ec.visibility_of_any_elements_located((By.TAG_NAME, 'a')))
            for tag in case_url_tags:
                self.case_urls.append(tag.get_attribute("href"))

        return self.case_urls
