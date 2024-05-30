import sys
from bs4.element import ResultSet

sys.path.append("..")
from config import countries, countries_renamed, COUNTRY_ALIASES, ENCODING


def encode_metadata_as_utf8(data: dict) -> dict:
    """
    Encodes metadata in UTF-8 form

    Parameters
    ----------
    data : dict
        data to be encoded

    Returns
    -------
    encoded_dict : dict
        dict with encoded data
    """
    encoded_dict = dict()

    for res, metadata in data.items():
        encoded_metadata = dict()

        for key, value in metadata.items():
            # Encode byte literals
            if isinstance(value, bytes):
                encoded_value = value.decode(ENCODING)
            else:  # Leave other values unchanged
                encoded_value = value
            encoded_metadata[key] = encoded_value

        encoded_dict[res] = encoded_metadata

    return encoded_dict


def process_country_names(column):
    """
    Removes "Zanzibar" entries as per README.md
    Updates historic country names to modern equivalents
    Returns formatted column to the dataframe

    Parameters
    ----------
    column : list
        column from a Pandas DataFrame

    Returns
    -------
    new_col : list
        formatted column
    """
    filtered_col = [c for c in column if c != "ZANZIBAR"]
    new_col = [
        COUNTRY_ALIASES[c] if c.upper() in COUNTRY_ALIASES else c.upper()
        for c in filtered_col
    ]
    countries_renamed.update(new_col)

    return new_col


def process_vote_column(column):
    """
    Formats country names in vote record columns
    Extends set of unique country names
    Returns formatted column to the dataframe

    Parameters
    ----------
    column : list
        column from a Pandas DataFrame

    Returns
    -------
    new_col : list
        formatted column
    """
    formatted_column = [
        c.strip(" '[]") for c in column.split(",") if c.strip(" '[]") != ""
    ]
    countries.update(formatted_column)

    return formatted_column


def sort_countries(raw_data: ResultSet) -> tuple[list]:
    """
    Sorts countries based on voting record
    Appends countries to corresponding lists

    Parameters
    ----------
    raw_data : BeautifulSoup bs4.element.ResultSet
        data to extract country and vote data from

    Returns
    -------
    yes_list : list[str]
    no_list : list[str]
    abs_list : list[str]
    nv_list : list[str]

    Countries sorted by vote record
    """
    raw = raw_data[:]
    # Lists to store country names by voting record
    yes_list = []  # countries that voted yes
    no_list = []  # no votes
    abs_list = []  # abstentions
    nv_list = []  # non-voting

    for i in range(len(raw)):
        # Separate vote and name values
        split_values = raw[i].split(maxsplit=1)
        # Yes votes
        if split_values[0].upper() == "Y" and len(split_values) == 2:
            yes_list.append(split_values[1].upper())
        # No votes
        elif split_values[0].upper() == "N" and len(split_values) == 2:
            no_list.append(split_values[1].upper())
        # Abstentions
        elif split_values[0].upper() == "A" and len(split_values) == 2:
            abs_list.append(split_values[1].upper())
        # Non-voting
        else:
            nv_list.append(raw[i].strip().upper())

    return yes_list, no_list, abs_list, nv_list
