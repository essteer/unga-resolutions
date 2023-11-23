# -*- coding: utf-8 -*-
import csv
import logging
import numpy as np
import pandas as pd
import re

##########################################################################
# Prepare files
##########################################################################

logging.basicConfig(filename="./logs/error.log", 
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s: %(message)s")
ENCODING = "utf-8"
DATA_FOLDER = "./data"

prefix = "20231028_2318"

df = pd.read_csv(f"{DATA_FOLDER}/{prefix}_records.csv")

##########################################################################
# Inspect data
##########################################################################

df.info()
df.describe()

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
    "Non-Voting" 
]

df = df[columns]
df.info()
df.describe()

##########################################################################
# Clean data
##########################################################################

# Drop rows where votes = "Undisclosed"
df = df[df["Yes Votes"] != "['Undisclosed']"]
# Convert dates to datetime
df["Vote Date"] = pd.to_datetime(df["Vote Date"], dayfirst=True)
# Sort by date, then by resolution reference
df = df.sort_values(by=["Vote Date", "Resolution"])
# Reset index and drop previous index
df = df.reset_index(drop=True)

##########################################################################
# Format country entries and get list of unique countries
##########################################################################

def process_vote_column(vote_column):
    """
    Formats the country names in vote record columns
    Extends the set of unique country names
    Returns the formatted column to the dataframe
    """
    # Split, strip, and filter out empty values
    formatted_column = [country.strip(" '[]") for country in vote_column.split(",") if country.strip(" '[]") != ""]
    
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
"""
NOTE: use a merge function later to consolidate vote records
"""
aliases = {
    'BYELORUSSIAN SSR': "BELARUS", 
    'BOLIVIA (PLURINATIONAL STATE OF)': "BOLIVIA", 
    'BRUNEI DARUSSALAM': "BRUNEI", 
    'CABO VERDE': "CAPE VERDE", 
    'CENTRAL AFRICAN EMPIRE': "CENTRAL AFRICAN REPUBLIC", 
    'CEYLON': "SRI LANKA", 
    'CONGO': "CONGO (ROC)", 
    'CONGO (BRAZZAVILLE)': "CONGO (ROC)", 
    'CONGO (DEMOCRATIC REPUBLIC OF)': "CONGO (DRC)",
    'CONGO (LEOPOLDVILLE)': "CONGO (DRC)", 
    '"CÔTE D\'IVOIRE"': "IVORY COAST", 
    '"COTE D\'IVOIRE"': "IVORY COAST", 
    'CZECH REPUBLIC': "CZECHIA", 
    'DAHOMEY': "BENIN", 
    'DEMOCRATIC KAMPUCHEA': "CAMBODIA", 
    '"DEMOCRATIC PEOPLE\'S REPUBLIC OF KOREA"': "NORTH KOREA", 
    'DEMOCRATIC REPUBLIC OF THE CONGO': "CONGO (DRC)", 
    'GERMAN DEMOCRATIC REPUBLIC': "EAST GERMANY", 
    'FEDERAL REPUBLIC OF': "GERMANY", 
    'KHMER REPUBLIC': "CAMBODIA", 
    'IRAN (ISLAMIC REPUBLIC OF)': "IRAN", 
    '"LAO PEOPLE\'S DEMOCRATIC REPUBLIC"': "LAOS", 
    '"LAO PEOPLE\'s DEMOCRATIC REPUBLIC"': "LAOS", 
    'LAO': "LAOS", 
    'LIBYAN ARAB JAMAHIRIYA': "LIBYA", 
    'LIBYAN ARAB REPUBLIC': "LIBYA", 
    'MALDIVE ISLANDS': "MALDIVES", 
    'MICRONESIA (FEDERATED STATES OF)': "MICRONESIA", 
    'PHILIPPINE REPUBLIC': "PHILIPPINES", 
    'REPUBLIC OF KOREA': "SOUTH KOREA", 
    'REPUBLIC OF MOLDOVA': "MOLDOVA", 
    'RUSSIAN FEDERATION': "RUSSIA", 
    'SAINT CHRISTOPHER AND NEVIS': "ST KITTS AND NEVIS", 
    'SIAM': "THAILAND", 
    'SURINAM': "SURINAME", 
    'SWAZILAND': "ESWATINI", 
    'SYRIAN ARAB REPUBLIC': "SYRIA", 
    'TANGANYIKA': "TANZANIA",   
    'THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA': "NORTH MACEDONIA", 
    'TÜRKİYE': "TURKIYE", 
    'TURKEY': "TURKIYE", 
    'UKRAINIAN SSR': "UKRAINE", 
    'UNION OF SOUTH AFRICA': "SOUTH AFRICA",
    'UNITED REPUBLIC OF CAMEROON': "CAMEROON", 
    'UNITED REPUBLIC OF TANZANIA': "TANZANIA", 
    'UPPER VOLTA': "BURKINA FASO", 
    'USSR': "RUSSIA", 
    'VENEZUELA (BOLIVARIAN REPUBLIC OF)': "VENEZUELA", 
    'VIET NAM': "VIETNAM", 
    'ZAIRE': "CONGO (DRC)", 
    'ZANZIBAR': "TANZANIA"
}

countries_renamed = [aliases[country] if country.upper() in aliases else country.upper() for country in countries]
countries_renamed = list(set(countries_renamed))
countries_renamed.sort()

##########################################################################
# 
##########################################################################

# # Create columns from renamed countries
# country_columns = {country: ["N/A"] * len(df) for country in countries_renamed}
# # Initialise columns on right of dataframe
# df = pd.concat([df, pd.DataFrame(country_columns)], axis=1)



