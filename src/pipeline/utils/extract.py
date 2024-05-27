import re


def get_country_votes(k: list, v: list) -> dict:
    """
    Extracts country vote figures

    Parameters
    ----------
    k : list
        country name keys

    v : list
        country vote values

    Returns
    -------
    vote_by_country : dict
        vote records mapped to country name
    """
    # Extract vote and country string from data
    key_list = [key.text.strip() for key in k]
    vote_index = key_list.index("Vote")
    vote_by_country = v[vote_index].find_all(string=True)

    return vote_by_country


def get_figures(raw_data: str) -> list:
    """
    Extracts a list of string integers within a string object

    Parameters
    ----------
    raw_data : str
        data to extract from

    Returns
    -------
    figures : list[int]
        vote figures parsed from raw_data
    """
    figures = re.findall(r"\d+", raw_data)
    return figures


def get_figures_granular(raw_data: str) -> list:
    """
    Helper function for get_figures for cases where
    expected figures are missing, such as record 671259:
        voting_summary: Voting Summary Yes: 44 | No: | Abstentions: 5 | Non-Voting: 5 | Total voting membership: 54

    Parameters
    ----------
    raw_data : str
        data to extract from

    Returns
    -------
    voting_figures : list
        vote figures parsed from raw_data
    """
    voting_figures = []

    substrings = raw_data.split("|")

    for substring in substrings:
        figure = get_figures(substring)
        if figure == []:
            voting_figures.append("0")
        else:
            voting_figures.append(figure[0])

    return voting_figures


def get_segments(raw_data: str) -> list:
    """
    Extracts URL segments from a string object

    Parameters
    ----------
    raw_data : str
        data to extract from

    Returns
    -------
    segments : list
        URL segments parsed from raw_data
    """
    segments = re.findall(r"record/(\d+)\?", raw_data)
    return segments
