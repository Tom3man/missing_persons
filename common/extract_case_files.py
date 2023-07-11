from typing import Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BuildRawData:

    def __init__(self, driver):
        self.driver = driver

    def build_raw_case_dict(self) -> Dict[str, str]:

        case_date_dict = {}

        # Find the case number
        case_number = WebDriverWait(
            self.driver, 5).until(
                ec.visibility_of_any_elements_located((By.CLASS_NAME, 'PageTitle')))[0].text
        case_date_dict["CASE_NUMBER"] = case_number

        # Find and extract case data
        case_data_raw = WebDriverWait(
            self.driver, 5).until(
                ec.visibility_of_any_elements_located((By.CLASS_NAME, 'CaseData')))[0]

        # All row entries are broken down into divs
        # These divs are split into further divs consisting of 'keys' and 'values'
        case_data_rows = WebDriverWait(
            case_data_raw, 5).until(
                ec.visibility_of_any_elements_located((By.CLASS_NAME, 'Entry')))

        for entry in case_data_rows:
            key_ = WebDriverWait(
                entry, 5).until(
                    ec.visibility_of_any_elements_located((By.CLASS_NAME, 'Key')))[0].text

            value_ = WebDriverWait(
                entry, 5).until(
                    ec.visibility_of_any_elements_located((By.CLASS_NAME, 'Value')))[0].text

            case_date_dict[key_.upper().replace(" ", "_")] = value_

        # Extract location information
        location_banner = WebDriverWait(
            self.driver, 5).until(
                ec.visibility_of_any_elements_located((By.CLASS_NAME, 'CaseMap')))[0]

        try:
            road = WebDriverWait(
                location_banner, 5).until(
                    ec.visibility_of_any_elements_located((By.CLASS_NAME, 'Road')))[0].text.lower()
            case_date_dict['LOCATION_ROAD'] = road
        except Exception as e:
            case_date_dict['LOCATION_ROAD'] = None

        try:
            county = WebDriverWait(
                location_banner, 5).until(
                    ec.visibility_of_any_elements_located((By.CLASS_NAME, 'County')))[0].text.lower()
            case_date_dict['LOCATION_COUNTY'] = county
        except Exception as e:
            case_date_dict['LOCATION_COUNTY'] = None

        try:
            country = WebDriverWait(
                location_banner, 5).until(
                    ec.visibility_of_any_elements_located((By.CLASS_NAME, 'Country')))[0].text.lower()
            case_date_dict['LOCATION_COUNTRY'] = country
        except Exception as e:
            case_date_dict['LOCATION_COUNTRY'] = None

        # Attempt to find who found them
        try:
            finders = WebDriverWait(
                location_banner, 5).until(
                    ec.visibility_of_any_elements_located((By.TAG_NAME, 'strong')))[0].text.lower()
            case_date_dict['FINDING_PARTY'] = finders
        except Exception as e:
            case_date_dict['FINDING_PARTY'] = None

        return case_date_dict
