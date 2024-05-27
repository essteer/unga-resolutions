import csv
import random
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
from masquer import masq
from tqdm import tqdm
from utils.extract import get_segments

##########################################################################
# Prepare URLs and requests
##########################################################################

# ~~~ URL components ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BASE_URL = "https://digitallibrary.un.org/search?ln=en&c=Voting+Data&rg="
LINKS_PER_PAGE = 100  # options = {10, 25, 50, 100}
LINK_LOC_BASE = "&jrec="
YEAR_BASE = "&fct__3="
FILTERS = "&fct__2=General+Assembly&cc=Voting+Data&fct__9=Vote"
PRESENT_SESSION = 2024

# ~~~ Updates ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Cannot paginate >500 records, so iterate by year (~100 records per year)
SESSIONS_LIST = list(range(1990, PRESENT_SESSION + 1))
# No records available for 1964
# SESSIONS_LIST.remove(1964)
# Records with data missing from archive
MISSING_RECORDS = ["454783"]
# Max no. of records was 170, in 1952
MAX_LINKS_PER_SESSION = 170
# Time delays in seconds
MIN_DELAY = 1
MAX_DELAY = 2

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
        search_URL = "".join(
            [
                BASE_URL,
                str(LINKS_PER_PAGE),
                LINK_LOC_BASE,
                str(link_loc),
                YEAR_BASE,
                str(session),
                FILTERS,
            ]
        )

        # Assign weighted random referer and user-agent to header
        header = masq(ua=True, rf=True, hd=True)
        header["Accept-Language"] = "en-US,en;q=0.9;q=0.7,zh-CN;q=0.6,zh;q=0.5"

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

# Uncomment below if within range
# for missing_segment in MISSING_RECORDS:
#     segments_master.remove(missing_segment)

##########################################################################
# Save to csv
##########################################################################

# Get current date in the format "yyyymmdd"
today = datetime.now().strftime("%Y%m%d_%H%M")
# Set filename
filename = f"./data/{today}_links.csv"
# Create csv of link segments
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["Segment"])
    # Write each element of the list to the CSV file as a new row
    for segment in segments_master:
        writer.writerow([segment])

print("Process complete.")
