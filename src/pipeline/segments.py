import requests
from bs4 import BeautifulSoup
from masquer import masq
from tqdm import tqdm
from utils.extract import get_segments
from utils.load import save_to_csv


# ~~~ URL components ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BASE_URL = "https://digitallibrary.un.org/search?ln=en&c=Voting+Data&rg="
LINKS_PER_PAGE = 100  # options = {10, 25, 50, 100}
LINK_LOC_BASE = "&jrec="
YEAR_BASE = "&fct__3="
FILTERS = "&fct__2=General+Assembly&cc=Voting+Data&fct__9=Vote"
PRESENT_SESSION = 2024

# ~~~ Updates ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Cannot paginate >500 records, so iterate by year (~100 records per year)
SESSIONS_LIST = list(range(1946, PRESENT_SESSION + 1))
# No records available for 1964
SESSIONS_LIST.remove(1964)
# Records with data missing from archive
MISSING_RECORDS = ["454783"]
# Max no. of records was 170, in 1952
MAX_LINKS_PER_SESSION = 170


def fetch(segments_list: list, session) -> list:
    """
    Gets link segments from search pages for a given year

    Parameters
    ----------
    segments_list : list
        segments retrieved

    session : int
        current year of records

    Returns
    -------
    segments_list : list
        URL segments retrieved from page crawl
    """
    # Reset link_loc to 1 for each session (year)
    link_loc = 1
    # Get record links displayed on each page for that session (year)
    for _ in range((MAX_LINKS_PER_SESSION // LINKS_PER_PAGE) + 1):
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
            break

        segments_list.extend(segments)

        if len(segments) < LINKS_PER_PAGE:
            break

        # Iterate link_loc by LINKS_PER_PAGE
        link_loc += LINKS_PER_PAGE

    return segments_list


def fetch_segments() -> list:
    """
    Calls fetch per session in SESSIONS_LIST
    to retrieve URL link segments

    Returns
    -------
    segments_list : list
        URL segments retrieved across each session
    """
    # Master list for URL record segments
    segments_list = []

    for session in tqdm(SESSIONS_LIST, desc="Fetching segments"):
        segments_list = fetch(segments_list, session)

    return segments_list


# Get segments
segments_master = fetch_segments()
for missing_segment in MISSING_RECORDS:
    segments_master.remove(missing_segment)

# Save to csv
save_successful = save_to_csv(segments_master, "_url_segments.csv")
if save_successful:
    print("URL segments saved to CSV")
