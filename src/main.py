# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet

# TODO: set up a loop to crawl pages
# TODO: organise into modules

##########################################################################
# Prepare URLs and source code
##########################################################################

# Set URL components
BASE_URL = "https://digitallibrary.un.org/search?ln=en&c=Voting+Data&rg="
LINKS_PER_PAGE = 100  # options = {10, 25, 50, 100}
LINK_LOC_BASE = "&jrec="
YEAR_BASE = "&fct__3="
FILTERS = "&fct__2=General+Assembly&cc=Voting+Data&fct__9=Vote"
PRESENT_SESSION = 2023

# Master dict for resolution dicts
resolutions_dict = {}
# Cannot paginate >500 records, so iterate by year (~100 per year)
sessions_list = list(range(1946, PRESENT_SESSION + 1))
# No records available for 1964
sessions_list.remove(1964)

link_loc = 1                # iterate by LINKS_PER_PAGE
year = sessions_list[0]     # iterate through sessions_list

# ~~~ Full URL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
URL = "".join([BASE_URL, 
              str(LINKS_PER_PAGE), 
              LINK_LOC_BASE, 
              str(link_loc), 
              YEAR_BASE, 
              str(year), 
              FILTERS])

# ~~~ Single page test ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
single_URL = "https://digitallibrary.un.org/record/4016932?ln=en"
html = requests.get(single_URL)
# Extract html source code
URL_source_code = html.text
# Parse URL_source_code
soup = BeautifulSoup(URL_source_code, "html.parser")

##########################################################################
# Extract data
##########################################################################
"""
Voting data is contained in spans with the class: 
class="value col-xs-12 col-sm-9 col-md-10".
"""
data = soup.find_all("span", class_="value col-xs-12 col-sm-9 col-md-10")
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

# ~~~ Extract voting figures ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
