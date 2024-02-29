import sqlite3


class DataBaseUtils:
    def __init__(self):
        self.con = sqlite3.connect("scraper.db")
        self.cursor = self.con.cursor()

    def create_database(self):
        """
        Creates or verifies the existence of the required tables in the
        database.

        This function is responsible for creating the 'Holiday' and 'Fly'
        tables in the database
        if they do not already exist. The 'Holiday' table stores information
        about holidays,
        including an identifier ('id'), text description ('text'),
        and a link ('link').
        The 'Fly' table stores information about flights, including
        an identifier ('id'),
        destination ('destination'), date ('date'), price ('price'),
        and a link ('link').

        Returns:
        - cur (sqlite3.Cursor): The SQLite cursor object to the database,
        allowing further operations.
        """
        cur = self.con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Holiday (
                    id INTEGER PRIMARY KEY,
                    text TEXT NOT NULL,
                    link TEXT NOT NULL
                    )"""
        )
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Fly(
        id INTEGER PRIMARY KEY,
        destination TEXT NOT NULL,
        date TEXT NOT NULL,
        price INTEGER,
        link TEXT NOT NULL
        )"""
        )
        return cur

    def test_insert_data_to_fly_table(
        self,
        destination="Tajlandia",
        date="22.03",
        price=8888,
        link="https://wp.pl",
    ):
        """
        This function is a test method designed to insert data into the
        'Fly' table
        of the database. It takes optional parameters for the destination,
        date, price,
        and link of the flight. Default values are provided
        for ease of testing.

        """
        con = self.con
        cur = self.cursor
        cur.execute(
            """INSERT INTO Fly(destination, date, price, link)
            VALUES (?, ?, ?, ?)""",
            (destination, date, price, link),
        )
        con.commit()

    def test_get_data_from_table_fly(self):
        """
        This function performs a SELECT query to fetch all rows and columns
        from the 'Fly' table.
        It then processes the results to create a list containing only the
        relevant information,
        excluding the primary key 'id' field.
        Returns:
        - lst (list): A list containing tuples with data from the 'Fly' table.
          Each tuple represents a row with the format
          (destination, date, price).
        """
        cur = self.cursor
        cur.execute(
            """
        SELECT * FROM
        Fly
        """
        )
        all_fly = cur.fetchall()
        lst = [x[1:4] for x in all_fly]
        return lst

    def insert_data_to_holiday_table(self, text, link):
        """
        Insert data into the 'Holiday' table with the provided text and link.

        Args:
        - text (str): Text description of the holiday.
        - link (str): Link related to the holiday.
        """
        con = self.con
        cur = self.cursor
        cur.execute(
            """
        INSERT
        INTO
        Holiday(text, link)
        VALUES(?, ?)""",
            (text, link),
        )
        con.commit()

    def insert_data_to_fly_table(self, destination, date, price, link):
        """
        Insert data into the 'Fly' table with the provided destination,
        date, price, and link.

        Args:
        - destination (str): Destination of the flight.
        - date (str): Date of the flight.
        - price (int): Price of the flight.
        - link (str): Link related to the flight.
        """
        con = self.con
        cur = self.cursor
        cur.execute(
            """
        INSERT
        INTO
        Fly(destination, date, price, link)
        VALUES(?, ?, ?, ?)""",
            (destination, date, price, link),
        )
        con.commit()

    def get_data_from_table_holiday(self):
        """
        Retrieve all data from the 'Holiday' table.

        Returns:
        - lst (list): A list containing tuples with data
        from the 'Holiday' table.
          Each tuple represents a row with the format (text, link).
        """
        cur = self.cursor
        cur.execute(
            """
        SELECT * FROM
        Holiday
        """
        )
        all_holiday = cur.fetchall()
        lst = [x[1:] for x in all_holiday]
        return lst

    def get_all_data_from_table_fly(self, destination, date):
        """
        Retrieve all data from the 'Fly' table for a specific
        estination and date.

        Args:
        - destination (str): Destination of the flight.
        - date (str): Date of the flight.

        Returns:
        - data (tuple): A tuple with data from the 'Fly'
        table for the specified destination and date.
          The format is (destination, date, price, link).
        """
        cur = self.cursor
        # date_tuple = (date,)
        cur.execute(
            """
        SELECT * FROM
        Fly
        Where
        destination = ? and date = ?
        """,
            (destination, date),
        )
        all_data = cur.fetchone()
        print(all_data)
        return all_data[1:5]

    def get_date_from_table_fly(self):
        """
        Retrieve destination and date information from the 'Fly' table.

        Returns:
        - lst (list): A list containing tuples with destination and date
        information from the 'Fly' table.
        """
        cur = self.cursor
        cur.execute(
            """
        SELECT
        destination, date
        FROM
        Fly
        """
        )
        all_fly = cur.fetchall()
        lst = [x for x in all_fly]
        return lst

    def get_price_from_table_fly(self, destination, date):
        """
        Retrieve the price of a flight from the 'Fly' table for a
        specific destination and date.

        Args:
        - destination (str): Destination of the flight.
        - date (str): Date of the flight.

        Returns:
        - price (int): Price of the flight.
        """
        cur = self.cursor
        cur.execute(
            "SELECT price FROM Fly WHERE destination = ? and date = ?",
            (destination, date),
        )
        price = cur.fetchone()
        return price[0]

    def update_price_in_fly_table(self, destination, date, new_price):
        """
        Update the price of a flight in the 'Fly' table for a
        specific destination and date.

        Args:
        - destination (str): Destination of the flight.
        - date (str): Date of the flight.
        - new_price (int): New price for the flight.
        """
        con = self.con
        cur = self.cursor
        try:
            new_price = int(new_price)
            cur.execute(
                "UPDATE Fly SET price = ? WHERE destination = ? " "AND date = ?",
                (new_price, destination, date),
            )
            con.commit()

        except ValueError as e:
            print(f"Error converting new_price: {e}")
