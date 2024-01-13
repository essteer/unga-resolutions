# -*- coding: utf-8 -*-
import csv, logging, os, random, re, requests, time
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from datetime import datetime
from tqdm import tqdm

##########################################################################
# Prepare files
##########################################################################

logging.basicConfig(filename="./logs/error.log", 
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s: %(message)s")

ENCODING = "utf-8"
DATA_FOLDER = "./data"
# NOTE: update prefix before running to match the most recent completed
# "..._records.csv" and "..._processed_segments.txt" files in data folder
prefix = "20240113_1310"
# Get latest versions
LATEST_RECORDS = f"{DATA_FOLDER}/{prefix}_records.csv"
LATEST_PROCESSED_SEGMENTS = f"{DATA_FOLDER}/{prefix}_processed_segments.txt"
LATEST_LINKS = f"{DATA_FOLDER}/20240113_1340_links.csv"

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
MIN_DELAY = 2
MAX_DELAY = 8
# Response codes
GOOD_RESPONSES = [200]
RETRY_RESPONSES = [429]
BAD_RESPONSES = [400, 401, 403, 404, 500, 502, 504]

# ~~~ Header data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

REFERERS = ["https://www.google.com/", 
            "https://bing.com/", 
            "https://search.yahoo.com/", 
            "https://www.baidu.com/", 
            "https://yandex.com/"]

REFERER_PROBS = [0.88, 0.03, 0.03, 0.03, 0.03]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36", 
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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47"
]

USER_AGENT_PROBS = [
    0.205, 0.14, 0.13, 0.105, 0.055, 
    0.055, 0.05, 0.045, 0.04, 0.03, 
    0.025, 0.02, 0.015, 0.015, 0.015, 
    0.0125, 0.0125, 0.012, 0.01, 0.008
]

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


def get_figures_granular(raw_data: str) -> list:
    """
    Helper function for get_figures for cases where
    expected figures are missing, such as record 671259:
        voting_summary: Voting Summary Yes: 44 | No: | Abstentions: 5 | Non-Voting: 5 | Total voting membership: 54
    """
    voting_figures = []
    
    substrings = raw_data.split("|")
            
    for substring in substrings:
        
        figure = get_figures(substring)
        if figure == []:
            voting_figures.append("0")
        else:
            voting_figures.append(figure[0])
    
    return voting_figures


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
        if split_values[0].upper() == "Y" and len(split_values) == 2:
            yes_countries.append(split_values[1].upper())
        # No votes
        elif split_values[0].upper() == "N" and len(split_values) == 2:
            no_countries.append(split_values[1].upper())
        # Abstentions
        elif split_values[0].upper() == "A" and len(split_values) == 2:
            abstention_countries.append(split_values[1].upper())
        # Non-voting
        else:
            non_voting_countries.append(raw[i].strip().upper())


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
    referer = weighted_random_selection(REFERERS, REFERER_PROBS)
    user_agent = weighted_random_selection(USER_AGENTS, USER_AGENT_PROBS)
    header["Referer"] = referer
    header["User-Agent"] = user_agent
    
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
            logging.error(f"{record_html.status_code} response; url: {record_URL}; counter: {counter}")
            break
        elif record_html.status_code not in GOOD_RESPONSES:
            logging.info(f"{record_html.status_code} response; url: {record_URL}; counter: {counter}")
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
    
    except ValueError as e:
        logging.info(f"Data issue: {str(e)}; url: {record_URL}; counter: {counter}")
        # Set all to Undisclosed if breakdown not provided
        yes_countries = ["Undisclosed"]
        no_countries = ["Undisclosed"]
        abstention_countries = ["Undisclosed"]
        non_voting_countries = ["Undisclosed"]
    
    # Set record_name to resolution reference
    resolution = str(metadata_dict.get("Resolution", "None"))
    
    try:
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
    except Exception as e:
        logging.info(f"Data issue: {str(e)}; url: {record_URL}; counter: {counter}")
        # Skip record if voting data is missing
        continue
    
    processed_segments.append(segment)
    counter += 1

##########################################################################
# Encode data in UTF-8
##########################################################################

encoded_resolutions_dict = {}
for res, metadata in resolutions_dict.items():
    encoded_metadata = {}
    
    for key, value in metadata.items(): 
        # Encode byte literals
        if isinstance(value, bytes):
            encoded_value = value.decode(ENCODING)
        # Leave other values unchanged
        else:
            encoded_value = value
        
        encoded_metadata[key] = encoded_value
    
    encoded_resolutions_dict[res] = encoded_metadata

##########################################################################
# Save to csv
##########################################################################

# Get datetime as "yyyymmdd_hhmm"
current_datetime = datetime.now().strftime("%Y%m%d_%H%M")
# Set filename
new_version = f"./data/{current_datetime}_records.csv"
# Check whether LATEST_RECORDS exists
file_exists = os.path.isfile(LATEST_RECORDS)

if file_exists:
    try:
        # Read the existing CSV file
        with open(LATEST_RECORDS, "r", encoding=ENCODING, newline="") as file:
            reader = csv.reader(file)
            data = list(reader)
    
        # Append resolutions_dict data to existing data
        for res, metadata in encoded_resolutions_dict.items():
            new_row = [metadata.get(column, "") for column in data[0]]
            data.append(new_row)
    
        # Save entire dataset to new file
        with open(new_version, "w", encoding=ENCODING, newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)
    
    except Exception as e:
        logging.exception(f"Error: {str(e)}; url: {record_URL}; counter: {counter}")
  
else:
    try:
        # Save resolutions_dict data to csv
        with open(new_version, "w", encoding=ENCODING, newline="") as file:
            
            columns = list(encoded_resolutions_dict.values())[0].keys()
            writer = csv.DictWriter(file, fieldnames=columns)
            
            if not file_exists:
                writer.writeheader()
            for res, metadata in encoded_resolutions_dict.items():
                writer.writerow(metadata)
                    
    except Exception as e:
        logging.exception(f"Error: {str(e)}; url: {record_URL}; counter: {counter}")

# Create new file of processed URLs for later resumption
with open(f"./data/{current_datetime}_processed_segments.txt", "w", encoding=ENCODING) as file:
    for segment in processed_segments:
        file.write(f"{segment}\n")
        
print(f"{counter} record{'s' if counter != 1 else ''} saved to csv")

# Confirm no duplicates exist
assert len(processed_segments) == len(set(processed_segments))
