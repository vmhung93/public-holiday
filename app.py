import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlencode

import requests

load_dotenv()  # Take environment variables from .env


# Retrieves the region ID associated with a country code from a JSON file
def get_region_id(country_code):
    # Opening JSON file
    with open("countries.json", "r") as data:
        countries = json.load(data)

        # Convert list to dictionary for faster lookups
        country_dict = {c["countryCode"]: c["regionId"] for c in countries}

        return country_dict.get(country_code)


# Fetches public holidays for a given country within a date range using Google Calendar API
def get_public_holiday(country_code, from_date, to_date):
    api_key = os.getenv("GOOGLE_API_KEY")

    base_url = "https://www.googleapis.com/calendar/v3/calendars"
    calendar_id = "holiday@group.v.calendar.google.com"
    date_format = "%Y/%m/%d"

    try:
        # Time range
        time_min = datetime.strptime(from_date, date_format).isoformat() + "Z"
        time_max = datetime.strptime(to_date, date_format).isoformat() + "Z"

        # RegionId
        region_id = get_region_id(country_code)

        if not region_id:
            logging.error(f"No region ID found for country code: {country_code}")
            return []

        # URL builder
        params = {
            "key": api_key,
            "timeMin": time_min,
            "timeMax": time_max,
            "singleEvents": "true",  # Ensure single events are fetched
        }
        url = f"{base_url}/{region_id}%23{calendar_id}/events?{urlencode(params)}"

        holidays = requests.get(url).json()

        if "items" not in holidays:
            logging.warning(f"No public holiday data found for {country_code}")
            return []

        data = {
            "summary": holidays["summary"],
            "description": holidays["description"],
            "kind": holidays["kind"],
            "items": [
                {
                    "summary": item["summary"],
                    "description": item["description"],
                    "startDate": item["start"]["date"],
                    "endDate": item["end"]["date"],
                    "status": item["status"],
                    "visibility": item["visibility"],
                }
                for item in holidays["items"]
            ],
        }

        # Sort ascending
        data["items"].sort(key=lambda item: item["startDate"])

        return data
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error: {req_err}")
        return []
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        return []


def main():
    data = get_public_holiday("vn", "2024/01/01", "2024/12/31")
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
