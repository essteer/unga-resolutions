# -*- coding: utf-8 -*-
import csv, random, re, requests, time
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from datetime import datetime

##########################################################################
# Prepare URLs and requests
##########################################################################

# URL components
BASE_URL = "https://digitallibrary.un.org/record/"
LANGUAGE = "?ln=en"

# Store URL segments in list
SEGMENTS = []
# Read csv of link segments
with open("./data/20231026_link_segments.csv", "r") as file:
    csv_reader = csv.reader(file)
    # Skip header row
    header = next(csv_reader)
    for row in csv_reader:
        SEGMENTS.append(row[0])

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

test_segments = ["4016932", "3839868"]
for segment in test_segments:

# for segment in SEGMENTS[:2]:
    
    # Generate random delay
    random_delay = random.uniform(MIN_DELAY, MAX_DELAY)
    # Add random delay
    time.sleep(random_delay)
    
    ##########################################################################
    # Extract record data
    ##########################################################################
    
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
    
    ##########################################################################
    # Process data
    ##########################################################################
    
    # Voting metadata contained in multiple <div class="metadata-row">
    keys = raw_record.find_all("span", class_="title col-xs-12 col-sm-3 col-md-2")
    values = raw_record.find_all("span", class_="value col-xs-12 col-sm-9 col-md-10")
    
    # ~~~ Extract text into variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    metadata_dict = {}
    
    for key, value in zip(keys, values):
        metadata_dict[key.text.strip()] = value.text
    
    # title = values[0].text
    # agenda = values[1].text
    # resolution = values[2].text
    # meeting_record = values[3].text
    # draft_resolution = values[4].text
    # committee_report = 1
    # note = values[5].text
    # voting_summary = values[6].text
    # vote_date = values[7].text
    
    title =             str(metadata_dict.get("Title", "None"))
    agenda =            str(metadata_dict.get("Agenda", "None"))
    resolution =        str(metadata_dict.get("Resolution", "None"))
    meeting_record =    str(metadata_dict.get("Meeting record", "None"))
    draft_resolution =  str(metadata_dict.get("Draft resolution", "None"))
    committee_report =  str(metadata_dict.get("Committee report", "None"))
    note =              str(metadata_dict.get("Note", "None"))
    vote_date =         str(metadata_dict.get("Vote date", "None"))
    
    # ~~~ Sort countries by vote record ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    Voting Summary Yes: 80 | No: 2 | Abstentions: 47 | Non-Voting: 64 | Total voting membership: 193 '
    """
    try:
        voting_summary = metadata_dict["Vote summary"]
        voting_figures = get_figures(voting_summary)
    except KeyError:
        voting_figures = ["0", "0", "0", "0", "0"]
    
    # Lists to store country names by voting record
    yes_countries = []
    no_countries = []
    abstention_countries = []
    non_voting_countries = []
    
    # Extract vote and country string from data
    vote_by_country = values[-2].find_all(string=True)  # TODO update this based on key location
    # Sort countries into lists by vote record
    sort_countries(vote_by_country)
    
    # ~~~ Create dict of resolution data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # Set record_name to current resolution reference
    record_name = str(resolution)
    
    # Add dict of current resolution to main resolutions_dict
    resolutions_dict[record_name] = {"Title": title, 
                                     "Agenda": agenda,
                                     "Resolution": resolution, 
                                     "Meeting Record": meeting_record, 
                                     "Draft Resolution": draft_resolution, 
                                     "Committee Report": committee_report,
                                     "Note": note, 
                                     "Num Yes": int(voting_figures[0]), 
                                     "Num No": int(voting_figures[1]), 
                                     "Num Abstentions": int(voting_figures[2]), 
                                     "Num Non-Voting": int(voting_figures[3]), 
                                     "Total Votes": int(voting_figures[4]), 
                                     "Vote Date": vote_date, 
                                     "Yes Votes": yes_countries, 
                                     "No Votes": no_countries, 
                                     "Abstentions": abstention_countries, 
                                     "Non-Voting": non_voting_countries, 
                                     "Record URL": str(record_URL)
                                     }

print("Process complete.")
