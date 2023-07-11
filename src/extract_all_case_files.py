import sys

folder_path = '../'
sys.path.append(folder_path)

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from common import BuildRawData, EngineerRawData, ExtractMissingPersonsUrls


def main():

    # Extract all URLs
    extract = ExtractMissingPersonsUrls()
    case_urls = extract.extract_case_urls()

    full_df = pd.DataFrame()
    for n, url in enumerate(case_urls, start=1):

        print(f"Running for URL {n} out of {len(case_urls)}")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)

        # Build raw dict
        build = BuildRawData(driver=driver)
        raw_case_dict = build.build_raw_case_dict()

        # Build cleaned dict
        clean_case_dict = EngineerRawData.format_raw_case_dict(
            case_date_dict=raw_case_dict
        )

        # Build single data frame row
        row_df = pd.DataFrame([clean_case_dict])

        # Concatenate row_df to full_df
        full_df = pd.concat([full_df, row_df], ignore_index=True)

    full_df.to_csv("output.csv", index=False)


if __name__ == "__main__":
    main()
