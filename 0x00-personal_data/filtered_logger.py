#!/usr/bin/env python3
""" Protecting PII """

from typing import List
import logging
import re  # needed 2
from mysql.connector import connection
from os import environ

PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')

# 0. Regex-ing


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    temp = message
    for field in fields:
        temp = re.sub(field + "=.*?" + separator,
                      field + "=" + redaction + separator, temp)
    return temp

# 2. Create logger


def get_logger() -> logging.Logger:
    """ Returns logger obj  """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


# 3 connect to secure database
"""Always run all my sql command before attempting to connect"""


def get_db() -> connection.MySQLConnection:
    """
    Connect to mysql server with environmental using environment variables.
    Returns a MySQLConnection object.
    """

    # Fetch the credentials from the environment variables, with defaults if
    # not set

    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get(
        "PERSONAL_DATA_DB_PASSWORD",
        "FGCIcisco15$")  # leave empty
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME",
                          "holberton")  # if local include: ,"holberton"
    connector = connection.MySQLConnection(
        user=username,
        password=password,
        host=db_host,
        database=db_name)
    return connector

# 1. Log formatter


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ inits class instance """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filters values in incoming log records """
        return filter_datum(
            self.fields, self.REDACTION, super(
                RedactingFormatter, self).format(record),
            self.SEPARATOR)

# 4 Read and filter data


def main() -> None:
    """
    Obtain a database connection using get_db
    and retrieve all rows in the users table and display each row
    """
    db = get_db()
    cur = db.cursor()

    query = ('SELECT * FROM users;')
    cur.execute(query)
    fetch_data = cur.fetchall()

    logger = get_logger()

    for row in fetch_data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3],
                               row[4], row[5], row[6], row[7])
        logger.info(fields)

    cur.close()
    db.close()


if __name__ == "__main__":
    main()
