# jwst-api-client
A simple Python command-line tool for accessing public James Webb Space Telescope data

## Installation

To use this tool, you will need to have [Python 3](https://www.python.org/downloads/) installed on your system.

1.  Clone this repository to your local machine using `git clone https://github.com/etfriedman/jwst-api-client.git`
2.  Navigate to the directory where you cloned the repository
3.  Install the required dependencies by running `pip install -r requirements.txt`
	- Note: if the python requests library is already installed this step is not required.
See [requirements](https://github.com/etfriedman/jwst-api-client/edit/master/README.md#requirements) for more information

## Usage

To run the tool, open a terminal or command prompt and navigate to the directory where you cloned the repository. Then run the following command:
`python3 JWST_DE.py --key YOUR_API_KEY` (replacing YOUR_API_KEY with the key you requested)
- If you do not yet have a key, run `python3 JWST_DE.py` and the program will walk you through generating one.
Once you have run the program with your API key, type `help` to learn more on how to use the program.

### Example Usage:
https://user-images.githubusercontent.com/32680186/206341951-f2a2a4b6-9c2e-4ae9-9e9a-3afb0f50c9fa.mp4

#### Requirements:
- Python 3+
- requests 2.25.1 (https://pypi.org/project/requests/)
	- run `pip install requests`
	- Alternatively, after cloning and navigating to the folder run:
		-  `pip install -r requirements.txt`
- A JWST API Key, this program can request one for you, all you need is an email address. Alternatively, if you would like to request one yourself, go to https://jwstapi.com and scroll down.

This tool uses the API built by [Kyle Redelinghuys](https://www.ksred.com/) called [JWST API](https://jwstapi.com/)
