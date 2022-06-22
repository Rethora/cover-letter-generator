# Cover Letter Writer

## Prerequisites
- Make sure you have Python3 installed on your machine
- Make sure you have FireFox installed on your machine

## Installation
1) `$ git clone <url>` to clone project to local
2) `$ cd cover-letter-writer` to get into root directory of project
3) `$ python3 -m venv venv` to create virtual environment
4) `$ source venv/bin/activate` (mac and linux) `$ venv\Scripts\activate` (windows) to activate environment
5) `$ python3 -m pip install -r requirements.txt` to install dependencies
6) `$ python3 main.py` to run the program

## Tip
The virtual environment needs to be active when running the python script. 
If you close out the terminal session or deactivate the environment with `source venv/bin/deactivate`, 
you will need to rerun step 4 from "Installation" above to reenter the environment before running `python3 main.py`.

## Getting Started
- Replace "resume.pdf" with a pdf version on your resume with the name "resume.pdf"
- Open up settings.py and configure your custom settings
- Open up urls.txt and paste urls separated by new lines (Can handle as many urls as you want at once)
- After the program runs, your written cover letter will be appended to your resume with the name of the company in the output folder located in the root directory of the project

## Debugging
Sometimes the driver that handles scraping data from urls gets hung up or likes to open a popup and first load. 
If you would like to see what is happening in the driver open `main.py` and set `DEBUG=True`. 
You can close out any popups that may be unhandled or refresh the page as long as the url is not redirected, 
it should proceed as expected.

## Additional
When the cover letter is being written. A copy of it will be saved to the /tmp directory. 
If you need the cover letter detached from your resume, you can get just the cover letter there. 
The cover letter will overwrite for every url so use one url if you want to get it (or make sure it's the last url).

## Support
Here's a list of all the currently supported domains for this program:
- LinkedIn
