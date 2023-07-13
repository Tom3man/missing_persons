import sys
from datetime import date

import chromedriver_autoinstaller
import pandas as pd
from selenium import webdriver


def main():

    todays_date = date.today().strftime("%Y_%m_%d")
    FILE_NAME: str = f'missing_persons_{todays_date}.csv'

    folder_path = '../../'
    sys.path.append(folder_path)

    import missing_individuals.utils.utils as utils

    from missing_individuals import (BuildRawData, EngineerRawData,
                                     ExtractMissingPersonsUrls)

    data_path, chromedriver_path = utils.build_dirs()

    chromedriver_autoinstaller.install(path=chromedriver_path)
    driver = webdriver.Chrome()

    # Extract all URLs
    extract = ExtractMissingPersonsUrls(driver=driver)
    case_urls = extract.extract_case_urls()

    full_df = pd.DataFrame()
    for n, url in enumerate(case_urls, start=1):

        print(f"Running for URL {n} out of {len(case_urls)}")

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

    full_df.to_csv(f"{data_path}/{FILE_NAME}", index=False)


if __name__ == "__main__":
    main()
