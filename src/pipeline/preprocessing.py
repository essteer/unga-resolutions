import logging
import pandas as pd
from datetime import datetime
from tqdm import tqdm

##########################################################################
# Prepare files
##########################################################################

logging.basicConfig(
    filename="./logs/error.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)
ENCODING = "utf-8"
DATA_FOLDER = "./data"
# NOTE: update prefix before running to match the most recent completed
# "..._records.csv" file in data folder
prefix = "20240113_1341"
# Get latest version
df = pd.read_csv(f"{DATA_FOLDER}/{prefix}_records.csv")

##########################################################################
# Inspect data
##########################################################################

# df.info()
# df.describe()

##########################################################################
# Remove unused features
##########################################################################
"""
Unrequired columns: Record URL, Segment, Agenda, 
Meeting Record, Draft Resolution, Committee Report, Note
"""
columns = [
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

df = df[columns]
# df.info()
# df.describe()

##########################################################################
# Clean data
##########################################################################

# Drop rows where votes = "Undisclosed"
df = df[df["Yes Votes"] != "['Undisclosed']"]
# Convert dates to unified datetime format
df["Vote Date"] = pd.to_datetime(df["Vote Date"], format="%Y-%m-%d", errors="coerce")
# Sort by date, then by resolution reference
df = df.sort_values(by=["Vote Date", "Resolution"])
# Reset index and drop previous index
df = df.reset_index(drop=True)

df.info()
df.describe()

##########################################################################
# Format vote-count columns
##########################################################################

int_cols = ["Num Yes", "Num No", "Num Abstentions", "Num Non-Voting", "Total Votes"]
# Convert format of vote-count columns from int64 to int32
for col in int_cols:
    df[col] = df[col].astype("int32")

df.info()

##########################################################################
# Format country entries and get list of unique countries
##########################################################################


def process_vote_column(column):
    """
    Formats country names in vote record columns
    Extends set of unique country names
    Returns formatted column to the dataframe
    """
    formatted_column = [
        c.strip(" '[]") for c in column.split(",") if c.strip(" '[]") != ""
    ]

    global countries
    countries.update(formatted_column)

    return formatted_column


countries = set()
vote_categories = ["Yes Votes", "No Votes", "Abstentions", "Non-Voting"]

# Apply process_vote_column to format country names
for vote_category in vote_categories:
    df[vote_category] = df[vote_category].apply(process_vote_column)

##########################################################################
# Consolidate country names
##########################################################################


def process_country_names(column):
    """
    Removes "Zanzibar" entries as per README.md
    Updates historic country names to modern equivalents
    Returns formatted column to the dataframe
    """
    aliases = {
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

    filtered_col = [c for c in column if c != "ZANZIBAR"]

    new_col = [aliases[c] if c.upper() in aliases else c.upper() for c in filtered_col]

    global countries_renamed
    countries_renamed.update(new_col)

    return new_col


countries_renamed = set()
vote_categories = ["Yes Votes", "No Votes", "Abstentions", "Non-Voting"]

# Apply process_vote_column to format country names
for vote_category in vote_categories:
    df[vote_category] = df[vote_category].apply(process_country_names)

countries_renamed = sorted(countries_renamed)

# Save updated country names to file
with open("./data/member_states_consolidated.csv", "w", encoding=ENCODING) as file:
    for country in countries_renamed:
        file.write(f"{country}\n")

##########################################################################
# Extract voting data into country columns
##########################################################################

# Create DataFrame with new country columns
country_columns = {country: ["N/A"] * len(df) for country in countries_renamed}
new_df = pd.DataFrame(country_columns)

# Concatenate new DataFrame to the original
df = pd.concat([df, new_df], axis=1)

vote_abbreviations = {
    "Yes Votes": "Y",
    "No Votes": "N",
    "Abstentions": "A",
    "Non-Voting": "X",
}

# Populate country columns
df_copy = df.copy()
for i in tqdm(range(len(df_copy)), desc="Counting votes..."):
    for category in vote_categories:
        for country in df_copy.loc[i, category]:
            df.loc[i, country] = vote_abbreviations[category]

##########################################################################
# Save to csv
##########################################################################

# Get datetime as "yyyymmdd_hhmm"
current_datetime = datetime.now().strftime("%Y%m%d_%H%M")
# Set filename
filepath = f"./data/{current_datetime}_UNGA_votes.csv"

try:
    # Save to csv
    df.to_csv(filepath, encoding=ENCODING, index=False)
    print(f"File saved successfully: {filepath}")

except Exception as e:
    logging.exception(f"Error: {str(e)}")
    print("File save unsuccessful: review log for error details")
