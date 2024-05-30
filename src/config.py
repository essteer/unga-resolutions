import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
BASE_URL = "https://digitallibrary.un.org/record/"
ERROR_LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "error_logs")
ENCODING = "utf-8"

# ===========================================
# NOTE: change prefixes to match latest file versions of
# "_records.csv" and "_processed_segments.csv" in assets dir

# Change only after running segments.py
SEGMENT_PREFIX = "YYYYMMDD_HHMM"
# Change only after running records.py
RECORDS_PREFIX = "YYYYMMDD_HHMM"
# Get paths to latest versions
LATEST_SEGMENTS = os.path.join(ASSETS_DIR, f"{SEGMENT_PREFIX}_url_segments.csv")
LATEST_PROCESSED_SEGMENTS = os.path.join(
    ASSETS_DIR, f"{RECORDS_PREFIX}_processed_segments.csv"
)
LATEST_RECORDS = os.path.join(ASSETS_DIR, f"{RECORDS_PREFIX}_records.csv")
# ===========================================

countries = set()
countries_renamed = set()
COUNTRY_ALIASES = {
    "BOLIVIA (PLURINATIONAL STATE OF)": "BOLIVIA",
    "BRUNEI DARUSSALAM": "BRUNEI",
    "BURMA": "MYANMAR",
    "BYELORUSSIAN SSR": "BELARUS",
    "CABO VERDE": "CAPE VERDE",
    "CENTRAL AFRICAN EMPIRE": "CENTRAL AFRICAN REPUBLIC",
    "CEYLON": "SRI LANKA",
    "CONGO": "CONGO (ROC)",
    "CONGO (BRAZZAVILLE)": "CONGO (ROC)",
    "CONGO (DEMOCRATIC REPUBLIC OF)": "CONGO (DRC)",
    "CONGO (LEOPOLDVILLE)": "CONGO (DRC)",
    '"CÔTE D\'IVOIRE"': "IVORY COAST",
    '"COTE D\'IVOIRE"': "IVORY COAST",
    "CZECH REPUBLIC": "CZECHIA",
    "DAHOMEY": "BENIN",
    "DEMOCRATIC KAMPUCHEA": "CAMBODIA",
    '"DEMOCRATIC PEOPLE\'S REPUBLIC OF KOREA"': "NORTH KOREA",
    "DEMOCRATIC REPUBLIC OF THE CONGO": "CONGO (DRC)",
    "DEMOCRATIC YEMEN": "YEMEN (PDR)",
    "GERMAN DEMOCRATIC REPUBLIC": "EAST GERMANY",
    "FEDERAL REPUBLIC OF": "GERMANY",
    "KHMER REPUBLIC": "CAMBODIA",
    "IRAN (ISLAMIC REPUBLIC OF)": "IRAN",
    '"LAO PEOPLE\'S DEMOCRATIC REPUBLIC"': "LAOS",
    '"LAO PEOPLE\'s DEMOCRATIC REPUBLIC"': "LAOS",
    "LAO": "LAOS",
    "LIBYAN ARAB JAMAHIRIYA": "LIBYA",
    "LIBYAN ARAB REPUBLIC": "LIBYA",
    "MALDIVE ISLANDS": "MALDIVES",
    "MICRONESIA (FEDERATED STATES OF)": "MICRONESIA",
    "NETHERLANDS (KINGDOM OF THE)": "NETHERLANDS",
    "PHILIPPINE REPUBLIC": "PHILIPPINES",
    "REPUBLIC OF KOREA": "SOUTH KOREA",
    "REPUBLIC OF MOLDOVA": "MOLDOVA",
    "RUSSIAN FEDERATION": "RUSSIA",
    "SAINT CHRISTOPHER AND NEVIS": "SAINT KITTS AND NEVIS",
    "SIAM": "THAILAND",
    "SOUTHERN YEMEN": "YEMEN (PDR)",
    "SURINAM": "SURINAME",
    "SWAZILAND": "ESWATINI",
    "SYRIAN ARAB REPUBLIC": "SYRIA",
    "TANGANYIKA": "TANZANIA",
    "THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA": "NORTH MACEDONIA",
    "TÜRKİYE": "TURKIYE",
    "TURKEY": "TURKIYE",
    "UKRAINIAN SSR": "UKRAINE",
    "UNION OF SOUTH AFRICA": "SOUTH AFRICA",
    "UNITED ARAB REPUBLIC": "EGYPT",
    "UNITED REPUBLIC OF CAMEROON": "CAMEROON",
    "UNITED REPUBLIC OF TANZANIA": "TANZANIA",
    "UPPER VOLTA": "BURKINA FASO",
    "USSR": "RUSSIA",
    "VENEZUELA (BOLIVARIAN REPUBLIC OF)": "VENEZUELA",
    "VIET NAM": "VIETNAM",
    "ZAIRE": "CONGO (DRC)",
    "ZANZIBAR": "TANZANIA",
}

"""
Unrequired columns: Record URL, Segment, Agenda, 
Meeting Record, Draft Resolution, Committee Report, Note
"""
KEEP_COLUMNS = [
    "Resolution",
    "Vote Date",
    "Num Yes",
    "Num No",
    "Num Abstentions",
    "Num Non-Voting",
    "Total Votes",
    "Title",
    "Yes Votes",
    "No Votes",
    "Abstentions",
    "Non-Voting",
]

TEST_SEGMENTS = [
    "4016932",  # normal record
    "671259",  # missing figure
    "3996092",  # encoding "\u0130"
    "454783",  # no voting data
]
