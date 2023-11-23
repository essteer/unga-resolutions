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
Unrequired columns:
Record URL, Segment, Agenda, Meeting Record,
Draft Resolution, Committee Report, Note
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
# Convert dates and sort
##########################################################################

df["Vote Date"] = pd.to_datetime(df["Vote Date"], dayfirst=True)
# Sort by date, then by resolution reference
df = df.sort_values(by=["Vote Date", "Resolution"])
# Reset index and drop previous index
df = df.reset_index(drop=True)

##########################################################################
# Get list of country names
##########################################################################

countries = []
vote_categories = ["Yes Votes", "No Votes", "Abstentions", "Non-Voting"]

# Get list of all countries with name variations
for category in vote_categories:
    for group in df[category]:
        for country in group.split(","):
            country = country.strip(" '[]")
            if country == "" or country == "Undisclosed":
                continue
            elif country not in countries:
                countries.append(country)

##########################################################################
# Consolidate country names
##########################################################################
"""
NOTE: use a merge function here later to consolidate vote records
"""
aliases = {'BYELORUSSIAN SSR': "BELARUS", 
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
           'ZANZIBAR': "TANZANIA"}

countries_renamed = [aliases[country] if country.upper() in aliases else country.upper() for country in countries]
countries_renamed = list(set(countries_renamed))
countries_renamed.sort()

##########################################################################
# 
##########################################################################


            
