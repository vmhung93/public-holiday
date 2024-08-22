# Public Holiday Fetcher

This project provides a Python script to fetch public holidays for a given country within a specified date range using the Google Calendar API.

## Features

Fetches public holiday data for a specific country within a date range.

## Requirements

- Python 3.x
- `requests` library
- Google API Key with access to the Google Calendar API

## Installation

#### Install Dependencies

`pip install -r requirements.txt`

#### Create a .env File

Open the .env file in a text editor and add your Google API key like this:

`GOOGLE_API_KEY=your_api_key_here`

Replace your_api_key_here with the actual API key you obtained from the Google Cloud Console.

## Usage

#### Creating virtual environments

`python -m venv ./env`

#### Active

CMD `<venv>\Scripts\activate.bat`
PowerShell `<venv>\Scripts\Activate.ps1`

#### Running the Script

Run the script using Python: `python main.py`

#### Deactivate

`deactivate`

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss changes.
