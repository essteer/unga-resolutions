import csv
import logging
import os
import random
import requests
import time
from bs4 import BeautifulSoup
from masquer import masq
from datetime import datetime
from tqdm import tqdm
from src.config import ASSETS_DIR, ENCODING, ERROR_LOGS_DIR
from utils.extract import get_country_votes, get_figures, get_figures_granular
from utils.load import save_dict_to_csv, save_to_csv
from utils.transform import encode_metadata_as_utf8, sort_countries

##########################################################################
# Prepare files
##########################################################################

os.makedirs(os.path.join(ERROR_LOGS_DIR), exist_ok=True)
error_log = os.path.join(ERROR_LOGS_DIR, "error.log")
logging.basicConfig(
    filename=error_log,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)

# NOTE: update prefix before running to match the most recent completed
# "..._records.csv" and "..._processed_segments.csv" files in data folder
prefix = "20240113_1310"
# Get latest versions
LATEST_RECORDS = os.path.join(ASSETS_DIR, f"{prefix}_records.csv")
LATEST_PROCESSED_SEGMENTS = os.path.join(ASSETS_DIR, f"{prefix}_processed_segments.csv")
LATEST_LINKS = os.path.join(ASSETS_DIR, "20240113_1340_links.csv")

##########################################################################
# Prepare URLs and requests
##########################################################################

BASE_URL = "https://digitallibrary.un.org/record/"
# Store URL segments in list
SEGMENTS = []
# Read csv of link segments
with open(LATEST_LINKS, "r") as file:
    csv_reader = csv.reader(file)
    # Skip header row
    header = next(csv_reader)
    for row in csv_reader:
        SEGMENTS.append(row[0])

# Read csv of link segments previously processed
with open(LATEST_PROCESSED_SEGMENTS, "r", encoding=ENCODING) as file:
    processed_segments = [line.strip() for line in file]

BATCH_SIZE = 50
START = len(processed_segments)
END = min(START + BATCH_SIZE, len(SEGMENTS))
# Time delays in seconds
MIN_DELAY = 0.5
MAX_DELAY = 3
# Response codes
GOOD_RESPONSES = [200]
RETRY_RESPONSES = [429]
BAD_RESPONSES = [400, 401, 403, 404, 500, 502, 504]

##########################################################################
# Sample sets
##########################################################################

# Specific record tests
# test_segments = [
# "4016932",  # general record
# "671259",  # missing figure
# "3996092",  # encoding "\u0130"
# "454783"  # no voting data
# ]
# Random tests
# sample = random.sample(SEGMENTS, 20)

##########################################################################
# Iterate through records
##########################################################################

# Master dict for resolution records
resolutions_dict = {}
# Counter to track progress
counter = 0

# for segment in test_segments:
# for segment in sample:
for segment in tqdm(SEGMENTS[START:END], desc="Fetching records"):
    if segment in processed_segments:
        print(f"segment {segment} already processed")
        continue

    # Random delay between requests
    random_delay = random.uniform(MIN_DELAY, MAX_DELAY)
    time.sleep(random_delay)

    # Assign weighted random referer and user-agent to header
    header = masq(ua=True, rf=True, hd=True)
    header["Accept-Language"] = "en-US,en;q=0.9;q=0.7,zh-CN;q=0.6,zh;q=0.5"

    # Example record URL "https://digitallibrary.un.org/record/4016932?ln=en"
    record_URL = BASE_URL + segment

    # Make request and catch response errors and retry
    for i in range(4):
        record_html = requests.get(record_URL, headers=header)

        if isinstance(record_html, requests.models.Response):
            if record_html.status_code not in RETRY_RESPONSES:
                break
            else:  # Exponential delay before each retry
                time.sleep(10 + 5**i)

    if isinstance(record_html, requests.models.Response):
        if record_html.status_code in BAD_RESPONSES:
            logging.error(
                f"{record_html.status_code} response; url: {record_URL}; counter: {counter}"
            )
            break
        elif record_html.status_code not in GOOD_RESPONSES:
            logging.info(
                f"{record_html.status_code} response; url: {record_URL}; counter: {counter}"
            )
            break

    # Extract and parse html source code
    record_URL_source_code = record_html.text
    raw_record = BeautifulSoup(record_URL_source_code, "html.parser")

    # Voting metadata contained in multiple <div class="metadata-row">
    keys = raw_record.find_all("span", class_="title col-xs-12 col-sm-3 col-md-2")
    values = raw_record.find_all("span", class_="value col-xs-12 col-sm-9 col-md-10")

    # Create dict of metadata
    metadata_dict = {}
    for key, value in zip(keys, values):
        metadata_dict[key.text.strip()] = value.text

    # Extract vote figures
    try:
        voting_summary = metadata_dict["Vote summary"]
        voting_figures = get_figures(voting_summary)
        # Conduct granular extraction if data missing
        if len(voting_figures) != 5:
            voting_figures = get_figures_granular(voting_summary)

    except KeyError as e:
        logging.info(f"Data Issue: {str(e)}; url: {record_URL}; counter: {counter}")
        # Skip record if voting data is missing
        continue

    try:
        # Extract vote and country string from data
        vote_by_country = get_country_votes(keys, values)
        # Sort countries into lists by vote record
        yes_voters, no_voters, abs_voters, non_voters = sort_countries(vote_by_country)

    except ValueError as e:
        logging.info(f"Data issue: {str(e)}; url: {record_URL}; counter: {counter}")
        # Set all to Undisclosed if breakdown not provided
        yes_voters = ["Undisclosed"]
        no_voters = ["Undisclosed"]
        abs_voters = ["Undisclosed"]
        non_voters = ["Undisclosed"]

    # Set record_name to resolution reference
    resolution = str(metadata_dict.get("Resolution", "None"))

    try:
        # Add dict of current resolution to main resolutions_dict
        resolutions_dict[resolution] = {
            "Resolution": resolution,
            "Vote Date": str(metadata_dict.get("Vote date", "None")),
            "Num Yes": int(voting_figures[0]),
            "Num No": int(voting_figures[1]),
            "Num Abstentions": int(voting_figures[2]),
            "Num Non-Voting": int(voting_figures[3]),
            "Total Votes": int(voting_figures[4]),
            "Record URL": str(record_URL),
            "Segment": segment,
            "Title": str(metadata_dict.get("Title", "None")),
            "Yes Votes": yes_voters,
            "No Votes": no_voters,
            "Abstentions": abs_voters,
            "Non-Voting": non_voters,
            "Agenda": str(metadata_dict.get("Agenda", "None")),
            "Meeting Record": str(metadata_dict.get("Meeting record", "None")),
            "Draft Resolution": str(metadata_dict.get("Draft resolution", "None")),
            "Committee Report": str(metadata_dict.get("Committee report", "None")),
            "Note": str(metadata_dict.get("Note", "None")),
        }
    except Exception as e:
        logging.info(f"Data issue: {str(e)}; url: {record_URL}; counter: {counter}")
        # Skip record if vote data is missing
        continue

    processed_segments.append(segment)
    counter += 1

# Encode data in UTF-8
encoded_resolutions_dict = encode_metadata_as_utf8(resolutions_dict)

##########################################################################
# Save records to csv
##########################################################################

# Get datetime as "yyyymmdd_hhmm"
current_datetime = datetime.now().strftime("%Y%m%d_%H%M")
# Set filename
new_version = os.path.join(ASSETS_DIR, f"{current_datetime}_records.csv")
# Check whether LATEST_RECORDS exists
file_exists = os.path.isfile(LATEST_RECORDS)

try:
    if file_exists:
        # Read the existing CSV file
        with open(LATEST_RECORDS, "r", encoding=ENCODING, newline="") as file:
            reader = csv.reader(file)
            data = list(reader)

        # Append resolutions_dict data to existing data
        for metadata in encoded_resolutions_dict.values():
            new_row = [metadata.get(column, "") for column in data[0]]
            data.append(new_row)

        # Save entire dataset to new file
        save_successful = save_dict_to_csv(data, new_version)

    else:
        # Save resolutions_dict data to csv
        save_successful = save_dict_to_csv(
            encoded_resolutions_dict, new_version, is_new=True
        )

    if save_successful:
        print(f"{counter} record{'s' if counter != 1 else ''} saved to csv")

except Exception as e:
    logging.exception(f"Error: {str(e)}; url: {record_URL}; counter: {counter}")

##########################################################################
# Save URL segment progress to csv
##########################################################################

save_successful = save_to_csv(
    processed_segments, "_processed_segments.csv", "Processed Segments"
)
if save_successful:
    print("Processed URL segments saved to CSV")

# Confirm no duplicates exist
assert len(processed_segments) == len(set(processed_segments))
