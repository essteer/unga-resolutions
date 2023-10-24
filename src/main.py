# -*- coding: utf-8 -*-
import random, re, requests, time
from bs4 import BeautifulSoup
from bs4.element import ResultSet

##########################################################################
# Prepare URLs and requests
##########################################################################

# ~~~ URL components ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BASE_URL_SEARCH = "https://digitallibrary.un.org/search?ln=en&c=Voting+Data&rg="
LINKS_PER_PAGE = 100  # options = {10, 25, 50, 100}
LINK_LOC_BASE = "&jrec="
YEAR_BASE = "&fct__3="
FILTERS = "&fct__2=General+Assembly&cc=Voting+Data&fct__9=Vote"
PRESENT_SESSION = 2023

BASE_URL_RECORD = "https://digitallibrary.un.org/record/"
LANGUAGE = "?ln=en"

# Master dict for resolution dicts
resolutions_dict = {}
# Cannot paginate >500 records, so iterate by year (~100 per year)
sessions_list = list(range(1946, PRESENT_SESSION + 1))
# No records available for 1964
sessions_list.remove(1964)

link_loc = 1                # iterate by LINKS_PER_PAGE
year = sessions_list[0]     # iterate through sessions_list

# ~~~ Full search URL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

search_URL = "".join([BASE_URL_SEARCH, 
              str(LINKS_PER_PAGE), 
              LINK_LOC_BASE, 
              str(link_loc), 
              YEAR_BASE, 
              str(year), 
              FILTERS])

# ~~~ Request delay ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MIN_DELAY = 2  # Min delay in seconds
MAX_DELAY = 8  # Max delay in seconds

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
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"]
USER_AGENT_PROBS = [0.3, 0.15, 0.12, 0.1, 0.1, 0.08, 0.05, 0.05, 0.05]

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
# Extract record links
##########################################################################

# Assign weighted-random referer and user-agent to header
referer = random.choices(REFERERS, weights=REFERER_PROBS, k=1)
user_agent = random.choices(USER_AGENTS, weights=USER_AGENT_PROBS, k=1)
header["Referer"] = referer[0]
header["User-Agent"] = user_agent[0]

search_html = requests.get(search_URL, headers=header)
# Extract html source code
search_URL_source_code = search_html.text
# Parse source code
raw_search = BeautifulSoup(search_URL_source_code, "html.parser")

links = [link.get("href") for link in raw_search.find_all("a", href=True)]

##########################################################################
# Extract record data
##########################################################################

# Assign weighted-random referer and user-agent to header
referer = random.choices(REFERERS, weights=REFERER_PROBS, k=1)
user_agent = random.choices(USER_AGENTS, weights=USER_AGENT_PROBS, k=1)
header["Referer"] = referer
header["User-Agent"] = user_agent

# Example record URL "https://digitallibrary.un.org/record/4016932?ln=en"
# record_URL = BASE_URL_RECORD + "4016932" + LANGUAGE
# record_html = requests.get(record_URL, headers=header)
# # Extract html source code
# record_URL_source_code = record_html.text
# # Parse source code
# raw_record = BeautifulSoup(record_URL_source_code, "html.parser")

##########################################################################
# Process data
##########################################################################
"""
Voting data is contained in spans with the class: 
class="value col-xs-12 col-sm-9 col-md-10".
"""
# data = raw_record.find_all("span", class_="value col-xs-12 col-sm-9 col-md-10")
# Check object indices in data:
# for i in range(len(data)):
#     print(f"data[{i}]: \n {data[i]}")

# ~~~ Extract text into variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

title = data[0].text
agenda = data[1].text
resolution = data[2].text
meeting_record = data[3].text
draft_resolution = data[4].text
note = data[5].text
voting_summary = data[6].text
vote_date = data[7].text

# ~~~ Parse voting figures ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_figures(raw_data: str) -> list:
    """
    Args:
        raw_data, string object
    Returns:
        figures, list of integers parsed from raw_data
    """
    figures = re.findall(r"\d+", raw_data)
    return figures


"""voting_summary structure
Voting Summary Yes: 80 | No: 2 | Abstentions: 47 | Non-Voting: 64 | Total voting membership: 193 '
"""
voting_figures = get_figures(voting_summary)


# ~~~ Sort countries by vote record ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def sort_countries(raw_data: ResultSet) -> None:
    """
    Separates countries based on voting record
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
        if split_values[0] == "Y":
            yes_countries.append(split_values[1])
        # No votes
        elif split_values[0] == "N":
            no_countries.append(split_values[1])
        # Abstentions
        elif split_values[0] == "A":
            abstention_countries.append(split_values[1])
        # Non-voting
        else:
            non_voting_countries.append(raw[i].strip())
    

# Lists to store country names by voting record
yes_countries = []
no_countries = []
abstention_countries = []
non_voting_countries = []

# Extract vote and country string from data
vote_by_country = data[8].find_all(string=True)
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
                                 "Non-Voting": non_voting_countries
                                 }
