#!/usr/bin/env python3
"""
This script defines a function and classes
 to obfuscate PII (Personally Identifiable Information)
  in log messages.
It includes functions to filter data,
 configure loggers, and connect to a MySQL database.
"""

from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (List[str]): List of field names to obfuscate.
        redaction (str): String to replace the field values with.
        message (str): The log message to obfuscate.
        separator (str): The character that separates fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        pattern = f"{field}=.*?{separator}"
        replacement = f"{field}={redaction}{separator}"
        message = re.sub(pattern, replacement, message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class to obfuscate specified fields in log messages.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with the fields to be obfuscated.

        Args:
            fields (List[str]): List of field names to obfuscate.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and obfuscated log message.
        """
        original_message = super().format(record)
        redacted_message = filter_datum(self.fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        return redacted_message


def get_logger() -> logging.Logger:
    """
    Configure and return a logger for user data.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establish and return a connection to the MySQL database using environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(user=user,
                                         password=password,
                                         host=host,
                                         database=database)
    return connection


def main():
    """
    Main entry point for the script. Fetches user data from the database and logs it with PII obfuscation.
    """
    db_connection = get_db()
    logger = get_logger()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    column_names = cursor.column_names

    for row in cursor:
        log_message = "".join(f"{column}={value}; " for column, value in zip(column_names, row))
        logger.info(log_message.strip())

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
