import logging
import os
import pandas as pd
import sys
from tqdm import tqdm
from utils.load import save_to_csv
from utils.transform import process_vote_column, process_country_names

sys.path.append("..")
from config import (
    ASSETS_DIR,
    countries_renamed,
    ERROR_LOGS_DIR,
    ENCODING,
    KEEP_COLUMNS,
)

##########################################################################
# Prepare files
##########################################################################

os.makedirs(os.path.join(ERROR_LOGS_DIR), exist_ok=True)
error_log = os.path.join(ERROR_LOGS_DIR, "error.log")
logging.basicConfig(
    filename=error_log,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)
# NOTE: update prefix before running to match the most recent completed
# "..._records.csv" file in data folder
prefix = "2024MMDD_HHMM"
# Get latest version
df = pd.read_csv(os.path.join(ASSETS_DIR, f"{prefix}_records.csv"), engine="pyarrow")

##########################################################################
# Inspect data
##########################################################################

# Uncomment to inspect data
# df.info()
# df.describe()

##########################################################################
# Remove unused features
##########################################################################

df = df[KEEP_COLUMNS]
# Uncomment to inspect data
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

vote_categories = ["Yes Votes", "No Votes", "Abstentions", "Non-Voting"]
# Apply process_vote_column to format country names
for vote_category in vote_categories:
    df[vote_category] = df[vote_category].apply(process_vote_column)

##########################################################################
# Consolidate country names
##########################################################################

vote_categories = ["Yes Votes", "No Votes", "Abstentions", "Non-Voting"]

# Apply process_vote_column to format country names
for vote_category in vote_categories:
    df[vote_category] = df[vote_category].apply(process_country_names)

countries_renamed = sorted(countries_renamed)

# Save updated country names to file
with open(
    os.path.join(ASSETS_DIR, "member_states_consolidated.csv"), "w", encoding=ENCODING
) as file:
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

save_successful = save_to_csv(df, "_UNGA_votes.csv")
if save_successful:
    print("Processed vote records saved to CSV")
