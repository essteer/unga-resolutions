import asyncio
import logging
import re
import requests
import time
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from masquer import masq
from tqdm.asyncio import tqdm


def extract_html(html_array: dict) -> dict[str:BeautifulSoup]:
    """
    Extracts html using BeautifulSoup

    Parameters
    ----------
    html_array : list
        html objects to be parsed

    Returns
    -------
    raw_html : dict[str: BeautifulSoup]
        html after parsing by BeautifulSoup
    """
    raw_html = {k: BeautifulSoup(v, "html.parser") for k, v in html_array.items()}
    return raw_html


def extract_metadata(b4s_dict: dict[str:BeautifulSoup]) -> list[dict]:
    """
    Extracts metadata from BeautifulSoup objects
    Adds dicts of metadata to main_list

    Parameters
    ----------
    b4s_dict : dict[str: BeautifulSoup]
        mapping of URL segments to BeautifulSoup objects
        to extract metadata from

    Returns
    -------
    main_metadata_dict : dict[dict]
        dict of extracted metadata dicts
        keys are URL segments
        values are dicts of extracted metadata from those URL segments
    """
    main_metadata_dict = {}

    for b4s in b4s_dict:
        # Voting metadata contained in multiple <div class="metadata-row">
        keys = b4s_dict[b4s].find_all(
            "span", class_="title col-xs-12 col-sm-3 col-md-2"
        )
        values = b4s_dict[b4s].find_all(
            "span", class_="value col-xs-12 col-sm-9 col-md-10"
        )

        # Create dict of metadata for this record
        metadata_dict = {}
        for key, value in zip(keys, values):
            metadata_dict[key.text.strip()] = value.text

        main_metadata_dict[b4s] = metadata_dict

    return main_metadata_dict


async def fetch(rec: str) -> dict[str] | None:
    """
    Fetches HTML from a given URL
    with exponential delays for failures

    Parameters
    ----------
    rec : str
        URL segment for record to scrape

    Returns
    -------
    dict[str] | None
        HTML if successful else None
            dict uses URL segment as key
            HTML as value
    """
    # Make request and catch response errors and retry
    for i in range(3):
        try:
            # Assign weighted random referer and user-agent to header
            header = masq(ua=True, rf=True, hd=True)
            header["Accept-Language"] = "en-US,en;q=0.9;q=0.7,zh-CN;q=0.6,zh;q=0.5"
            # Example record URL "https://digitallibrary.un.org/record/4016932?ln=en"
            r = await asyncio.to_thread(
                requests.get,
                f"https://digitallibrary.un.org/record/{rec}",
                headers=header,
                timeout=10,
            )
            r.raise_for_status()
            return {rec: r.text}

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching record {rec}: {e}")
            time.sleep(10 + 5**i)

    logging.error(
        f"Failed to fetch https://digitallibrary.un.org/record/{rec} after 3 retries"
    )

    return None


async def fetch_all(recs: list) -> dict:
    """
    Passes individual URL segments to be scraped

    Parameters
    ----------
    recs : list
        URL segments to scrape HTML from

    Returns
    -------
    dict[str]
        mapping of URL segment to scraped HTML
    """
    tasks = []
    for rec in recs:
        task = asyncio.create_task(fetch(rec))
        tasks.append(task)
    # use tqdm here in place of asynio for progress bar
    responses = await tqdm.gather(*tasks, desc="Fetching records")
    # filter out None responses
    res = [r for r in responses if r is not None]
    # [{k: v}, {k: v}, {k: v}] -> {k: v, k: v, k: v}
    segment_to_html_dict = {k: v for d in res for k, v in d.items()}

    return segment_to_html_dict


async def fetch_records(records: list) -> list[dict]:
    """
    Passes list of records to scrape functions
    and awaits response

    Parameters
    ----------
    records : list
        list of record locations to scrape from

    Returns
    -------
    htmls : dict
        mapping of URL segment to scraped HTML
    """
    htmls = await fetch_all(records)
    return htmls


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


def get_vote_figures(voting_summary: str) -> list[int]:
    """
    Gets the number of votes per vote type

    Parameters
    ----------
    voting_summary : str
        raw data on vote figures

    Returns
    -------
    voting_figures : list[int]
        number of votes per vote type
    """
    voting_figures = get_figures(voting_summary)
    # Conduct granular extraction if data missing
    if len(voting_figures) != 5:
        voting_figures = get_figures_granular(voting_summary)

    return voting_figures


def get_votes_per_country(seg: str, raw_html: str) -> ResultSet:
    """
    Gets each country name and its vote for current record

    Parameters
    ----------
    seg : str
        current record's segment ID

    raw_html : str
        html to extract country names from

    Returns
    -------
    vote_by_country : ResultSet
        country and vote data
    """
    # Voting metadata contained in multiple <div class="metadata-row">
    keys = raw_html[seg].find_all("span", class_="title col-xs-12 col-sm-3 col-md-2")
    values = raw_html[seg].find_all("span", class_="value col-xs-12 col-sm-9 col-md-10")
    # Extract vote and country string from data
    vote_by_country = get_country_votes(keys, values)

    return vote_by_country
