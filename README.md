## NFLScraper - Crawlera Example

A Selenium - Chromedriver - Crawlera example, which demonstrates a basic erroneous example of connecting to a Crawlera proxy through [crawlera-headless-proxy](https://github.com/scrapinghub/crawlera-headless-proxy) and logging into the site. As of the current situation, Chromedriver is unable to load the page successfully, presumably due to [this](https://github.com/webpack/webpack/issues/7502) issue on one of the Resource files for the login page.

## Installation

- It is presumed that an instance of `crawlera-headless-proxy` is installed and running on `localhost:3128`. Instructions can be found [here](https://github.com/scrapinghub/crawlera-headless-proxy).
- Python dependencies can be installed through the requirements file through `pip install -r requirements.txt`.
- A Chromedriver executable must exist on the `PATH` environment variable. Binaries can be found [here](http://chromedriver.chromium.org/downloads).

## Usage

The `NFL_EMAIL` and `NFL_PASS` environment variables must be set. Can be random strings for the purpose of testing.

After that, the scraper can be run using:

```
python scraper.py
```
