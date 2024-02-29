# Travel Deals Scraper README

## Description

The `scraper.py` module provides a web scraping solution for retrieving last-minute holiday deals and flight offers from
various travel-related websites. The scraper is designed to compare the extracted information with predefined lists of
destinations, adding new deals to a SQLite database and sending notifications via email and Discord. The module includes
the following functionalities:

- **`WebScraper` Class**: A class that inherits from `DataBaseUtils`, initialized with predefined destination
  lists (`destination_list`), flight information (`fly_dict` and `price_dict`), and includes methods for scraping
  last-minute deals and flight information from specific websites.

### Web Scraper Methods

#### `web_scraper_last_minuter`

- Scrapes the 'https://lastminuter.pl' website for last-minute holiday deals.
- Compares destinations with the predefined list and adds new deals to the 'Holiday' table in the database.
- Sends email notifications and Discord messages for new deals.

#### `web_scraper_fly4free`

- Scrapes the 'https://fly4free.pl' website for flight deals.
- Compares destinations with the predefined list and adds new deals to the 'Holiday' table in the database.
- Sends email notifications and Discord messages for new deals.

#### `web_scraper_wakacyjni_piraci`

- Scrapes the 'https://wakacyjnipiraci.pl' website for holiday deals.
- Compares destinations with the predefined list and adds new deals to the 'Holiday' table in the database.
- Sends email notifications and Discord messages for new deals.

#### `r_scraper_fly`

- Scrapes flight information from specified URLs in the 'fly_dict' attribute.
- Uses Selenium to navigate to websites, retrieve flight details, and update the 'Fly' table in the database.
- Checks for price changes and sends notifications for significant price drops.

### Scheduler

- Uses the `apscheduler` library to schedule and automate scraping jobs at specified intervals.

## Setup

Install the required libraries using

```bash
pip install -r requirements.txt.
```

Ensure you have a GeckoDriver installed and added to your system's PATH if using Selenium with Firefox.
To install the required dependencies, use the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. **Database Setup**: Ensure the SQLite database file `scraper.db` is created and tables are set up using
   the `create_database` method in `DataBaseUtils`.

2. **Environment Variables**: Create a `.env` file with the following variables:
   ```
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_email_password
   EMAIL_RECEIVER=receiver_email1@gmail.com
   EMAIL_RECEIVER2=receiver_email2@gmail.com
   DISCORD_TOKEN=your_discord_bot_token
   ```

3. **Scheduler Initialization**: Run the `scheduler_job` function to start the scraping scheduler.

```python
from apscheduler.schedulers.background import BlockingScheduler
from scraper import WebScraper


def scheduler_job():
    sched = BlockingScheduler()

    @sched.scheduled_job('interval', minutes=12)
    def scraping():
        web = WebScraper()
        print(web.web_scraper_last_minuter())
        print(web.web_scraper_fly4free())
        print(web.web_scraper_wakacyjni_piraci())
        print(web.r_scraper_fly())

    sched.start()


scheduler_job()
```

4. **Run the Scheduler**: Execute the script to start the scheduled scraping jobs.

```bash
python your_script_name.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.