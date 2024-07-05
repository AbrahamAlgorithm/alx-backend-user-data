#!/usr/bin/env python3
"""Deal about filtering data"""

from typing import List
import logging
import re
from os import getenv
import mysql.connector


PII_FIELDS = ('email', 'name', 'ssn', 'password', 'phone')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''
    function called filter_datum that
    returns the log message obfuscated
    '''
    for field in fields:
        mes = re.sub(field+'=.*?'+separator,
                     field+'='+redaction+separator, message)
    return mes


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        format method to filter values in
        incoming log records using filter_datum
        '''
        message = super(RedactingFormatter, self).format(record)
        redact = filter_datum(self.fields, self.REDACTION,
                              message, self.SEPARATOR)
        return redact


def get_logger() -> logging.Logger:
    '''get logging function'''
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logger.StreamHandler()
    fmt = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''get a database securely'''
    user = getenv('PERSONAL_DATA_DB_USERNAME')
    password = getenv('PERSONAL_DATA_DB_PASSWORD')
    host = getenv('PERSONAL_DATA_DB_HOST')
    db = getenv('PERSONAL_DATA_DB_NAME')
    connect = mysql.connector.connect(user=user, password=password,
                                      host=host, database=db)
    return connect


def main():
    '''
    entry point of the program
    '''
    db = get_db()
    logger = get_logger()
    cs = db.cursor()
    cs.execute("SELECT * FROM users;")
    fd = cs.column_names
    for r in cs:
        msg = "".join("{}={}; ".format(k, v) for k, v in zip(fd, r))
    cs.close()
    db.close()


if __name__ == "__main__":
    main()
