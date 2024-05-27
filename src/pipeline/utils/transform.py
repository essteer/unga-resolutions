from bs4.element import ResultSet


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
