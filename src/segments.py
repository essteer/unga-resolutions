# -*- coding: utf-8 -*-
import csv, random, re, requests, time
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm

##########################################################################
# Prepare URLs and requests
##########################################################################

# ~~~ URL components ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BASE_URL = "https://digitallibrary.un.org/search?ln=en&c=Voting+Data&rg="
LINKS_PER_PAGE = 100  # options = {10, 25, 50, 100}
LINK_LOC_BASE = "&jrec="
YEAR_BASE = "&fct__3="
FILTERS = "&fct__2=General+Assembly&cc=Voting+Data&fct__9=Vote"
PRESENT_SESSION = 2023

# ~~~ Updates ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Cannot paginate >500 records, so iterate by year (~100 records per year)
SESSIONS_LIST = list(range(1946, PRESENT_SESSION + 1))
# No records available for 1964
SESSIONS_LIST.remove(1964)
# Records with data missing from archive
MISSING_RECORDS = ["454783"]
# Max no. of records was 170, in 1952
MAX_LINKS_PER_SESSION = 170
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


def get_segments(raw_data: str) -> list:
    """
    Extracts URL segments from a string object
    
    Args:
        raw_data, string object
    Returns:
        segments, list of URL segments parsed from raw_data
    """
    segments = re.findall(r"record/(\d+)\?", raw_data)
    return segments


##########################################################################
# Extract record links
##########################################################################

# Master list for URL record segments
segments_master = []

for session in tqdm(SESSIONS_LIST, desc="Fetching links:"):
    # Reset link_loc to 1 for each session (year)
    link_loc = 1
    # Get record links displayed on each page for that session (year)
    for page in range((MAX_LINKS_PER_SESSION // LINKS_PER_PAGE) + 1):
        # Generate random delay
        random_delay = random.uniform(MIN_DELAY, MAX_DELAY)
        # Add random delay
        time.sleep(random_delay)
        
        # Update search_URL with current session and link_loc
        search_URL = "".join([BASE_URL, 
                          str(LINKS_PER_PAGE), 
                          LINK_LOC_BASE, 
                          str(link_loc), 
                          YEAR_BASE, 
                          str(session), 
                          FILTERS])
        
        # Get weighted random selection of referer and user-agent
        referer = weighted_random_selection(REFERERS, REFERER_PROBS)
        user_agent = weighted_random_selection(USER_AGENTS, USER_AGENT_PROBS)
        # Assign weighted random referer and user-agent to header
        header["Referer"] = referer
        header["User-Agent"] = user_agent
        
        search_html = requests.get(search_URL, headers=header)
        # Extract html source code
        search_URL_source_code = search_html.text
        # Parse source code
        raw_search = BeautifulSoup(search_URL_source_code, "html.parser")
        
        # Get link elements from source code
        links = str(raw_search.find_all("a", href=True))
        # Get URL segments and remove duplicates
        segments = list(set(get_segments(links)))
        
        if len(segments) == 0:
            print(f"No segments for {session} found at {search_URL}")
            break
        
        segments_master.extend(segments)
        
        if len(segments) < LINKS_PER_PAGE:
            print(f"No more records for year {session}")
            break
        
        # Iterate link_loc by LINKS_PER_PAGE
        link_loc += LINKS_PER_PAGE

for missing_segment in MISSING_RECORDS:
    segments_master.remove(missing_segment)

##########################################################################
# Save to csv
##########################################################################

# Get current date in the format "yyyymmdd"
today = datetime.now().strftime("%Y%m%d_%H%M")
# Set filename
filename = f"./data/{today}_segments.csv"
# Create csv of link segments
with open(filename, 'w', newline="") as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["Segment"])
    # Write each element of the list to the CSV file as a new row
    for segment in segments_master:
        writer.writerow([segment])

print("Process complete.")
