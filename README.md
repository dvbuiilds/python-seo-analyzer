
# Find Site Rank and Page Load Speed with Python - Python SEO Analyzer

Here is a free tool to help you find your site's loading speed and rank for a corresponding keyword.
This project contains a python shell script, that automates rank checking from Google and speed checking also.
The script does not uses proxies to check the site ranking for a keyword.

Note. Using large number of keywords may lead to google stopping our process.

The inspiration for this project came from : [Google-rank-tracker](https://github.com/sundios/Google-rank-tracker)

## Table of Contents 

- [Installation](#installation)
- [Running Tests](#running-tests)
- [Contributing & Questions](#contributing-and-questions)

---

## Installation

Installation of all Python dependencies

```shell
pip install requirements.txt
```

This project also uses `robobrowser` package for scraping the data from Google SERPs.

After all, dependencies are installed, we can start testing if the script is working fine.

## Running tests

Before executing the job, first write some keywords related to your site in `keywords.csv` file to help the automation script find the rank of the site for specific keywords. 
Any number of keywords can be added to the file but too much keywords may make us appear suspicious to Google and they may block us.
The results will appear in a json file.
You might recieve unexpected results because of `request.exceptions.ConnectionError` that arises due to surpassing the timely limit of requests to Google, or because of improper scraping results by `robobrowser` instance.

After that, we open the terminal and go to the folder that `analyzer.py` is saved and give the script executing rights.

```shell
python3 ./analyzer.py [website] [device] 
```

### For example 
We want to check the website www.ieee.org on desktop against the keyword **conferences** we need to include the keyword on keywords.csv file and run:

```shell
python3 ./analyzer.py www.ieee.org desktop
```

This will generate a JSON output including the page loading speed and the ranking of site for individual keywords on Google.
*Keep the `site url` and `device` in small cases.*

## Contributing and Questions
If you wish to contribute via some idea or some improvement, feel free to do so. 
I'll be active for any help.
You can always create an issue if you want to know something. :D

### Getting `werkzeug.utils import cached_property` error
This error can be resolved by installing the older version (0.16.1) of `Werkzeug` package.