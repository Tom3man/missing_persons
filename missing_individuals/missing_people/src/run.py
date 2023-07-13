import sys
from datetime import date

import chromedriver_autoinstaller
from selenium import webdriver


def main():

    todays_date = date.today().strftime("%Y_%m_%d")
    FILE_NAME: str = f'missing_people_{todays_date}.csv'

    folder_path = '../../../'
    sys.path.append(folder_path)

    from missing_individuals.missing_people.common.extract_all import ExtractMissingPeople

    import missing_individuals.utils.utils as utils

    data_path, chromedriver_path = utils.build_dirs()

    chromedriver_autoinstaller.install(path=chromedriver_path)
    driver = webdriver.Chrome()

    # Extract all URLs
    extract = ExtractMissingPeople(driver=driver)
    extract.run()

    extract.df_full.to_csv(f"{data_path}/{FILE_NAME}", index=False)


if __name__ == "__main__":
    main()
