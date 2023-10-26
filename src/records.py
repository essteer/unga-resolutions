# -*- coding: utf-8 -*-
import csv, random, re, requests, time
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from datetime import datetime
import os

# TODO: generalise get_figures to handle missing numbers

# NOTE: update before running
LATEST_VERSION = "./data/20231025_records.csv"

##########################################################################
# Prepare URLs and requests
##########################################################################

# URL components
BASE_URL = "https://digitallibrary.un.org/record/"
LANGUAGE = "?ln=en"

# Store URL segments in list
SEGMENTS = []
# Read csv of link segments
filename = "./data/20231026_link_segments.csv"
with open(filename, "r") as file:
    csv_reader = csv.reader(file)
    # Skip header row
    header = next(csv_reader)
    for row in csv_reader:
        SEGMENTS.append(row[0])

# Read csv of link segments previously processed
with open("./data/processed_segments.txt", "r") as file:
    processed_segments = [line.strip() for line in file]
    
BATCH_SIZE = 20
START = len(processed_segments)
END = min(START + BATCH_SIZE, len(SEGMENTS)) + 1

# Time delays in seconds
MIN_DELAY = 2
MAX_DELAY = 8

# ~~~ Header data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

REFERERS = ["https://www.google.com/", "https://bing.com/", "https://search.yahoo.com/", "https://www.baidu.com/", "https://yandex.com/"]
REFERER_PROBS = [0.88, 0.03, 0.03, 0.03, 0.03]

USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36", 
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36", 
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", 
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0", 
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", 
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", 
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36", 
               "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0", 
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", 
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0", 
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15", 
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0", 
               "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0", 
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0", 
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60", 
               "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0", 
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46", 
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15", 
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", 
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47"]
USER_AGENT_PROBS = [0.205, 0.14, 0.13, 0.105, 0.055, 
                    0.055, 0.05, 0.045, 0.04, 0.03, 
                    0.025, 0.02, 0.015, 0.015, 0.015, 
                    0.0125, 0.0125, 0.012, 0.01, 0.008]

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "en-US,en;q=0.9;q=0.7,zh-CN;q=0.6,zh;q=0.5", 
    "Referer": "https://www.google.com/", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "none", 
    "Sec-Fetch-User": "?1", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", 
  }

##########################################################################
# Helper functions
##########################################################################

def weighted_random_selection(sample_space: list[str], probs: list[float]) -> str:
    """
    Args:
        sample_space: list of options to randomly select from
        probs: list of probabilites per sample in sample_space (sum == 1)
    Returns:
        weighted random selection from sample_space
    """
    weighted_random_selection = random.choices(sample_space, weights=probs, k=1)
    
    return weighted_random_selection[0]


def get_figures(raw_data: str) -> list:
    """
    Extracts a list of string integers within a string object
    
    Args:
        raw_data, string object
    Returns:
        figures, list of integers parsed from raw_data
    """
    figures = re.findall(r"\d+", raw_data)
    return figures


def sort_countries(raw_data: ResultSet) -> None:
    """
    Sorts countries based on voting record
    Appends countries to corresponding lists
    
    Args:
        raw_data, BeautifulSoup bs4.element.ResultSet object    
    Returns:
        None
    """
    raw = raw_data[:]
    
    for i in range(len(raw)):
        # Separate vote and name values
        split_values = raw[i].split(maxsplit=1)
        # Yes votes
        if split_values[0] == "Y" and len(split_values) == 2:
            yes_countries.append(split_values[1])
        # No votes
        elif split_values[0] == "N" and len(split_values) == 2:
            no_countries.append(split_values[1])
        # Abstentions
        elif split_values[0] == "A" and len(split_values) == 2:
            abstention_countries.append(split_values[1])
        # Non-voting
        else:
            non_voting_countries.append(raw[i].strip())


##########################################################################
# Iterate through records
##########################################################################

# Master dict for resolution records
resolutions_dict = {}
# Set counter
counter = 0

test_segments = ["4016932", "3839868", "671259"]
for segment in test_segments:

# for segment in SEGMENTS[START:END]:

    if segment in processed_segments:
        print(f"segment {segment} already processed")
        continue
    
    # Generate random delay
    random_delay = random.uniform(MIN_DELAY, MAX_DELAY)
    # Add random delay
    time.sleep(random_delay)
    
    # Get weighted random selection of referer and user-agent
    referer = weighted_random_selection(REFERERS, REFERER_PROBS)
    user_agent = weighted_random_selection(USER_AGENTS, USER_AGENT_PROBS)
    # Assign weighted random referer and user-agent to header
    header["Referer"] = referer
    header["User-Agent"] = user_agent
    
    # Example record URL "https://digitallibrary.un.org/record/4016932?ln=en"
    record_URL = BASE_URL + segment + LANGUAGE
    record_html = requests.get(record_URL, headers=header)
    # Extract html source code
    record_URL_source_code = record_html.text
    # Parse source code
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
    except KeyError:
        voting_figures = ["0", "0", "0", "0", "0"]
    
    
    try:
        # Extract vote and country string from data
        key_list = [key.text.strip() for key in keys]
        vote_index = key_list.index("Vote")
        vote_by_country = values[vote_index].find_all(string=True)
        # Lists to store country names by voting record
        yes_countries = []
        no_countries = []
        abstention_countries = []
        non_voting_countries = []
        # Sort countries into lists by vote record
        sort_countries(vote_by_country)
    except ValueError:
        yes_countries = ["Unknown"]
        no_countries = ["Unknown"]
        abstention_countries = ["Unknown"]
        non_voting_countries = ["Unknown"]
    
    # Set record_name to resolution reference
    resolution = str(metadata_dict.get("Resolution", "None"))
    # Add dict of current resolution to main resolutions_dict
    resolutions_dict[resolution] = {"Resolution": resolution,
                                    "Vote Date": str(metadata_dict.get("Vote date", "None")), 
                                    "Num Yes": int(voting_figures[0]), 
                                    "Num No": int(voting_figures[1]), 
                                    "Num Abstentions": int(voting_figures[2]), 
                                    "Num Non-Voting": int(voting_figures[3]), 
                                    "Total Votes": int(voting_figures[4]), 
                                    "Record URL": str(record_URL),
                                    "Segment": segment,
                                    "Title": str(metadata_dict.get("Title", "None")), 
                                    "Yes Votes": yes_countries, 
                                    "No Votes": no_countries, 
                                    "Abstentions": abstention_countries, 
                                    "Non-Voting": non_voting_countries, 
                                    "Agenda": str(metadata_dict.get("Agenda", "None")),
                                    "Meeting Record": str(metadata_dict.get("Meeting record", "None")), 
                                    "Draft Resolution": str(metadata_dict.get("Draft resolution", "None")), 
                                    "Committee Report": str(metadata_dict.get("Committee report", "None")),
                                    "Note": str(metadata_dict.get("Note", "None"))
                                    }
    
    processed_segments.append(segment)
    counter += 1

##########################################################################
# Save to csv
##########################################################################

# Get current date in the format "yyyymmdd"
today = datetime.now().strftime("%Y%m%d")
# Set filename
new_version = f"./data/{today}_records.csv"

# Check whether the file exists
file_exists = os.path.isfile(LATEST_VERSION)

if file_exists:

    # Read the existing CSV file
    with open(LATEST_VERSION, "r", newline="") as file:
        reader = csv.reader(file)
        data = list(reader)

    # Append resolutions_dict data to existing data
    for res, metadata in resolutions_dict.items():
        new_row = [metadata.get(column, "") for column in data[0]]
        data.append(new_row)

    # Save entire dataset to new file
    with open(new_version, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
  
else:
    # Save resolutions_dict data to csv
    with open(new_version, "w", newline="") as file:
        
        columns = list(resolutions_dict.values())[0].keys()
        writer = csv.DictWriter(file, fieldnames=columns)
        
        if not file_exists:
            writer.writeheader()
        
        for res, metadata in resolutions_dict.items():
            writer.writerow(metadata)

# Updated file of processed URLs for later resumption
with open("./data/processed_segments.txt", "a") as file:
    for segment in processed_segments:
        file.write(f"{segment}\n")
        
print(f"{counter} record{'s' if counter != 1 else ''} saved to csv")
