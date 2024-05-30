import asyncio
import csv
import logging
import os
import sys
from datetime import datetime
from tqdm import tqdm
from utils.extract import (
    extract_html,
    extract_metadata,
    fetch_records,
    get_vote_figures,
    get_votes_per_country,
)
from utils.load import load_csv_col, save_dict_to_csv, save_to_csv
from utils.transform import encode_metadata_as_utf8, sort_countries

sys.path.append("..")
from config import (
    ASSETS_DIR,
    BASE_URL,
    ENCODING,
    ERROR_LOGS_DIR,
    LATEST_PROCESSED_SEGMENTS,
    LATEST_RECORDS,
    LATEST_SEGMENTS,
)

os.makedirs(os.path.join(ERROR_LOGS_DIR), exist_ok=True)
error_log = os.path.join(ERROR_LOGS_DIR, "error.log")
logging.basicConfig(
    filename=error_log,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)

# Get all URL segments in list
SEGMENTS = load_csv_col(LATEST_SEGMENTS, "r")
# Check whether LATEST_PROCESSED_SEGMENTS exists
file_exists = os.path.isfile(LATEST_PROCESSED_SEGMENTS)
if file_exists:
    # Get URL segments processed so far in list
    processed_segments = load_csv_col(LATEST_PROCESSED_SEGMENTS, "r")
else:
    processed_segments = []

BATCH_SIZE = 10
START = len(processed_segments)
END = min(START + BATCH_SIZE, len(SEGMENTS))

##########################################################################
# Iterate through records
##########################################################################

valid_segments = [
    segment for segment in SEGMENTS[START:END] if segment not in processed_segments
]
# Send requests for records
records_with_responses = asyncio.run(fetch_records(valid_segments))
# Convert to BeautifulSoup objects
records_with_raw_html = extract_html(records_with_responses)
# Extract metadata from each BeautifulSoup object
records_with_metadata = extract_metadata(records_with_raw_html)
# Master dict for processed resolution records
resolutions_dict = {}
# Counter to track progress
counter = 0

for segment, metadata_dict in tqdm(
    records_with_metadata.items(), desc="Parsing records"
):
    segment_url = BASE_URL + segment
    # Extract vote figures
    if "Vote summary" in metadata_dict:
        vote_figures = get_vote_figures(metadata_dict["Vote summary"])
    else:  # Skip record if voting data is missing
        logging.info(
            f"Data Issue: no Vote summary data; url: {segment_url}; counter: {counter}"
        )
        continue

    try:  # Group countries by vote
        votes_by_country = get_votes_per_country(segment, records_with_raw_html)
        yes_voters, no_voters, abs_voters, non_voters = sort_countries(votes_by_country)

    except ValueError as e:
        logging.info(f"Data issue: {str(e)}; url: {segment_url}; counter: {counter}")
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
            "Num Yes": int(vote_figures[0]),
            "Num No": int(vote_figures[1]),
            "Num Abstentions": int(vote_figures[2]),
            "Num Non-Voting": int(vote_figures[3]),
            "Total Votes": int(vote_figures[4]),
            "Record URL": str(segment_url),
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
        logging.info(f"Data issue: {str(e)}; url: {segment_url}; counter: {counter}")
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
    logging.exception(f"Error saving file: {str(e)}")

##########################################################################
# Save URL segment progress to csv
##########################################################################

save_successful = save_to_csv(processed_segments, "_processed_segments.csv")
if save_successful:
    print("Processed URL segments saved to CSV")

# Confirm no duplicates exist
assert len(processed_segments) == len(set(processed_segments))
