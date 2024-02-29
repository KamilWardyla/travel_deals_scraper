from apscheduler.schedulers.background import BlockingScheduler

from scraper import WebScraper


def scheduler_job():
    sched = BlockingScheduler()

    @sched.scheduled_job("interval", minutes=12)
    def scraping():
        web = WebScraper()
        print(web.web_scraper_last_minuter())
        print(web.web_scraper_fly4free())
        print(web.web_scraper_wakacyjni_piraci())
        print(web.r_scraper_fly())

    sched.start()


scheduler_job()
