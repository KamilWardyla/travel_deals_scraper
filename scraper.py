import datetime
import re
import time
from difflib import SequenceMatcher

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from db_utils import DataBaseUtils
from discordbot import discord_bot_send_message
from email_sender import email_sender
from fly_dict import fly_dict, price_dict

# class Database:
#     def database_cursor(self):
#         con = sqlite3.connect("scraper.db")
#         cur = con.cursor()
#         cur.execute("""CREATE TABLE IF NOT EXIST Holiday (
#                     id INTEGER PRIMARY KEY ASC,
#                     text TEXT NOT NULL,
#                     link TEXT NOT NULL,
#                     )""")
#         cur.execute("""CREATE TABLE IF NOT EXIST Fly(
#         id INTEGER PRIMARY KEY ASC,
#         date TEXT NOT NULL,
#         link TEXT NOT NULL,
#         price INTEGER,
#         )""")


class WebScraper(DataBaseUtils):
    def __init__(
        self,
    ):
        super().__init__()
        self.destination_list = [
            "Dominikana",
            "Lanka",
            "Meksyk",
            "Zanzibar",
            "Tanzania",
            " Malediwy",
            "Wyspy Zielonego przyladka",
            "Kuba",
            "Aruba",
            "Bali",
            "Indonezja",
            "Tajlandia",
            "Bangkok",
            "Wietnam",
            "Fuertaventura",
            "Phuket",
            "Krabi",
            "Phu Quoc",
            "Mombasa",
            "Kenia",
            "Mauritius",
            "Varadero",
            "Majowka",
            "Czarnogóra",
            "Turcja",
        ]
        self.fly_dict = fly_dict
        self.price_dict = price_dict

    @staticmethod
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def web_scraper_last_minuter(self):
        """
        Scrapes the 'https://lastminuter.pl' website for last-minute
        holiday deals.

        Retrieves information about last-minute holiday deals from the
        website, compares
        the destination with a predefined list, and adds new deals to
        the 'Holiday' table
        in the database. It also sends email notifications using the
        'email_sender' function
        and sends a Discord message using the 'discord_bot_send_message
        ' function.

        Returns:
        - str: A string indicating the status of the lastminuter job
        along with a timestamp,
          e.g., "2024-02-28 12:34:56, --- lastminuter job: done".

        Note:
        - The function relies on external functions 'email_sender' and
        'discord_bot_send_message'.
        - The similarity comparison between destination and words in
        the deal text is performed
          using the 'similar' method.
        """
        response = requests.get("https://lastminuter.pl")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            body = soup.body
            last_minuter_h2_tag = body.find_all("h2")
            for last in last_minuter_h2_tag:
                try:
                    link = str("https://lastminuter.pl" + last.find("a")["href"])
                    text = str(last.find("a").contents[0])
                    for destination in self.destination_list:
                        for word in text.split():
                            if self.similar(destination.lower(), word.lower()) > 0.8:
                                if (
                                    text,
                                    link,
                                ) not in self.get_data_from_table_holiday():
                                    self.insert_data_to_holiday_table(text, link)
                                    email_sender(text, link)
                                    message = f"""Wlasnie wleciala nowa promka
                                                {text}
                                                Link: {link}
                                                """
                                    discord_bot_send_message(message)
                                    print(f"Dodano okazje: {text}, {link}")
                finally:
                    continue
            return f"{datetime.datetime.now()}, --- lastminuter job: done"
        else:
            print(f"{datetime.datetime.now()} --- Error::Response status code != 200: {response.status_code}")

    def web_scraper_fly4free(self):
        """
        Scrapes the 'https://fly4free.pl' website for flight deals.

        Retrieves information about flight deals from the website, compares
        the destination with a predefined list, and adds new deals to the 'Holiday' table
        in the database. It also sends email notifications using the 'email_sender' function
        and sends a Discord message using the 'discord_bot_send_message' function.

        Returns:
        - str: A string indicating the status of the fly4free job along with a timestamp,
          e.g., "2024-02-28 12:34:56, --- fly4free job: done".

        Note:
        - The function relies on external functions 'email_sender' and 'discord_bot_send_message'.
        - The similarity comparison between destination and words in the deal text is performed
          using the 'similar' method.
        """
        response = requests.get("https://fly4free.pl")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            body = soup.body
            fly4free_h2_class_item_title = body.find_all("h2", {"class": "item__title"})
            for last in fly4free_h2_class_item_title:
                link = str(last.find("a")["href"])
                text = str(last.find("a").contents[0])
                for destination in self.destination_list:
                    for word in text.split():
                        if self.similar(destination.lower(), word.lower()) > 0.8:
                            if (
                                text,
                                link,
                            ) not in self.get_data_from_table_holiday():
                                self.insert_data_to_holiday_table(text, link)
                                email_sender(text, link)
                                # sms
                                message = f"""Wlasnie wleciala nowa promka
                                            {text}
                                            Link: {link}
                                                                                """
                                discord_bot_send_message(message)
                                print(f"Dodano okazje: {text}, {link}")
            fly4free_div_class_item_title = body.find_all("div", {"class": "col-xs-12 col-md-8"})
            for last in fly4free_div_class_item_title:
                last = last.find("h2", {"class": "item__title"})
                link = str(last.find("a")["href"])
                text = str(last.find("a").contents[0])
                for destination in self.destination_list:
                    for word in text.split():
                        if self.similar(destination.lower(), word.lower()) > 0.8:
                            if (
                                text,
                                link,
                            ) not in self.get_data_from_table_holiday():
                                self.insert_data_to_holiday_table(text, link)
                                email_sender(text, link)
                                print(f"Dodano okazje: {text}, {link}")

            return f"{datetime.datetime.now()}, --- fly4free job: done"
        else:
            print(f"{datetime.datetime.now()} --- Error::Response status code != 200: {response.status_code}")

    def web_scraper_wakacyjni_piraci(self):
        """
        Scrapes the 'https://wakacyjnipiraci.pl' website for holiday deals.

        Retrieves information about holiday deals from the website, compares
        the destination with a predefined list, and adds new deals to the 'Holiday' table
        in the database. It also sends email notifications using the 'email_sender' function
        and sends a Discord message using the 'discord_bot_send_message' function.

        Returns:
        - str: A string indicating the status of the wakacyjni piraci job along with a timestamp,
          e.g., "2024-02-28 12:34:56, --- wakacyjni piraci job: done".

        Note:
        - The function relies on external functions 'email_sender' and 'discord_bot_send_message'.
        - The similarity comparison between destination and words in the deal text is performed
          using the 'similar' method.
        """
        response = requests.get("https://wakacyjnipiraci.pl")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            body = soup.body
            piraci_div_class = body.find_all("div", {"class": "hp__sc-1lylu39-1 feUKcC"})
            for last in piraci_div_class:
                link = str(last.find("a")["href"])
                text = str(last.find("span", {"class": "hp__sc-ro12w0-8 kWnkGU"}).contents[0])
                for destination in self.destination_list:
                    for word in text.split():
                        if self.similar(destination.lower(), word.lower()) > 0.8:
                            if (
                                text,
                                link,
                            ) not in self.get_data_from_table_holiday():
                                self.insert_data_to_holiday_table(text, link)
                                email_sender(text, link)
                                # sms
                                message = f"""Wlasnie wleciala nowa promka
                                            {text}
                                            Link: {link}
                                                                                """
                                discord_bot_send_message(message)
                                print(f"Dodano okazje: {text}, {link}")
            return f"{datetime.datetime.now()}, --- wakacyjni piraci job: done"
        else:
            print(f"{datetime.datetime.now()} --- Error::Response status code != 200: {response.status_code}")

    def r_scraper_fly(self):
        """
        Scrapes flight information from the specified URLs in the 'fly_dict' attribute.

        For each destination and corresponding URL in 'fly_dict', the function uses Selenium
        to navigate to the website, retrieve flight details, and updates the 'Fly' table in
        the database with the information. It also checks for price changes and sends
        notifications using the 'email_sender' and 'discord_bot_send_message' functions.

        Returns:
        - str: A string indicating the status of the r job along with a timestamp,
          e.g., "2024-02-28 12:34:56, --- r job: done".

        Note:
        - The function relies on external functions 'email_sender' and 'discord_bot_send_message'.
        - It uses Selenium with Firefox WebDriver to interact with the websites.
        - The 'get_date_from_table_fly', 'get_price_from_table_fly', 'insert_data_to_fly_table',
          and 'update_price_in_fly_table' methods are assumed to be implemented in the class.
        """
        for destination in self.fly_dict.keys():
            for url in self.fly_dict[destination]:
                driver = webdriver.Firefox()
                driver.get(url)
                time.sleep(7)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                body = soup.body
                r_result = body.find_all("div", {"class": "termin active"})
                date_list = []
                price = 0
                if r_result:
                    for x in r_result:
                        date = x.text[0:11]
                        if date[-1].isnumeric():
                            date_list.append(date[:-1])
                        else:
                            date_list.append(date)
                        price += int(re.sub("[^0-9]", "", x.text[10:-3].replace(" ", "")))
                    date_str = f"Wylot: {date_list[0]} Powrot: {date_list[1]}"
                    if (
                        destination,
                        date_str,
                    ) not in self.get_date_from_table_fly():
                        self.insert_data_to_fly_table(destination, date_str, price, url)
                        print(f"Dodano lot do {destination}, termin: {date_str,} cena: {price}, link: {url}")
                    if (
                        (destination, date_str) in self.get_date_from_table_fly()
                        and price != self.get_price_from_table_fly(destination=destination, date=date_str)
                        and price <= self.price_dict[destination]
                    ):
                        self.update_price_in_fly_table(
                            destination=destination,
                            date=date_str,
                            new_price=price,
                        )
                        result = self.get_all_data_from_table_fly(destination=destination, date=date_str)
                        text = f"""
                        Hejka! :)
                        Mam dla Ciebie dobra wiadomosc, wlasnie wleciala super cena za loty do {destination}:)
                        Termin: {result[1]}
                        Cena: {result[2]}
                        """
                        link = result[-1]
                        message = f"""
                        Hejka! :)
                        Mam dla Ciebie dobra wiadomosc, wlasnie wleciala super cena za loty do {result[0]}:)
                        Termin: {result[1]}
                        Cena: {result[2]}
                        Link: {result[-1]}
                        """
                        email_sender(text, link)
                        discord_bot_send_message(message)
                        print(f"{datetime.datetime.now()}, --- NOWA CENA NA LOTY :)")
                time.sleep(5)
                driver.quit()
        return f"{datetime.datetime.now()}, --- r job: done"


# last = WebScraper()
# last.database_cursor()
# last.test_insert_data_to_fly_table()
# print(last.get_all_data_from_table_fly("Tajlandia", "22.03"))
# a = last.get_date_from_table_fly()
# last.update_price_in_fly_table("Tajlandia", "Wylot: sob, 13 sty Powrot: ndz, 21 sty", 20000)
# print(last.r_scraper_fly())
# # b = last.get_date_from_table_fly()
# print(a[0])
# last.r_scraper_fly(url_list)
# print(last.get_all_data_from_table_fly("Wylot: sob, 13 sty Powrot: ndz, 21 sty"))

# last.web_scraper_last_minuter()
# last.web_scraper_wakacyjni_piraci()
# last.web_scraper_fly4free()
# print(last.get_data_from_table_holiday())
