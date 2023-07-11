import os
import pathlib
from pathlib import Path
from typing import Union


def build_dirs() -> Union[str, os.PathLike]:

    REPO_PATH = pathlib.Path(
        __file__).parent.resolve().parent.absolute().parent.absolute()

    data_path = f"{REPO_PATH}/data"
    chromedriver_path = f"{REPO_PATH}/chromedrivers"

    Path(data_path).mkdir(parents=True, exist_ok=True)
    Path(chromedriver_path).mkdir(parents=True, exist_ok=True)

    return data_path, chromedriver_path
