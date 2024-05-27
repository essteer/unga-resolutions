import csv
import logging
import os
import pandas as pd
from datetime import datetime
from src.config import ASSETS_DIR, ENCODING, ERROR_LOGS_DIR


os.makedirs(os.path.join(ERROR_LOGS_DIR), exist_ok=True)
error_log = os.path.join(ERROR_LOGS_DIR, "error.log")
logging.basicConfig(
    filename=error_log,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


def save_dict_to_csv(d: dict, filename: str, is_new: bool = False) -> bool:
    """
    Saves dictionary to CSV

    Parameters
    ----------
    d : dict
        data to be saved

    filename : str
        name to save CSV with

    is_new : bool
        True if all new data else False

    Returns
    -------
    bool
        True if successful else False
    """
    try:
        if is_new:
            with open(filename, "w", encoding=ENCODING, newline="") as file:
                columns = list(d.values())[0].keys()
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writeheader()
                for metadata in d.values():
                    writer.writerow(metadata)

        else:
            with open(filename, "w", encoding=ENCODING, newline="") as file:
                writer = csv.writer(file)
                writer.writerows(d)

        return True

    except Exception as e:
        logging.exception(f"Error: {str(e)}")
        print("Error saving CSV: check error log")

        return False


def save_list_to_csv(d: list, filename: str, row: str) -> None:
    """
    Saves list to CSV

    Parameters:
    -----------
    d : list
        list of data to be saved

    filename : str
        name to save CSV with

    row : str
        name for header row
    """
    # Create csv of list elements
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow([row])
        # Write each element as a new row
        for data in d:
            writer.writerow([data])


def save_to_csv(
    data: list | pd.DataFrame, suffix: str, row_name: str | None = None
) -> bool:
    """
    Saves data to CSV

    Parameters
    ----------
    data : list | pd.DataFrame
        data to be saved

    suffix : str
        suffix to append to file name

    row_name : str | None
        name for header row

    Returns
    -------
    bool
        True if successful else False
    """
    # Get datetime as "yyyymmdd_hhmm"
    today = datetime.now().strftime("%Y%m%d_%H%M")
    # Set filename
    filepath = os.path.join(ASSETS_DIR, f"{today}{suffix}")

    try:
        if isinstance(data, list):
            save_list_to_csv(data, filepath, row_name)

        elif isinstance(data, pd.DataFrame):
            data.to_csv(filepath, encoding=ENCODING, index=False)

        else:
            print("Invalid file format: cannot save to CSV")
            return False

        return True

    except Exception as e:
        logging.exception(f"Error: {str(e)}")
        print("Error saving CSV: check error log")

        return False
