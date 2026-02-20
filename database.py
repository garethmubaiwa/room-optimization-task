import mysql.connector

'''
S - Single Responsibility Principle: The Database class has a single responsibility, which is to manage the connection to the MySQL database and provide methods for executing queries and managing transactions.
This module defines a Database class that manages the connection to a MySQL database. 
It provides methods to get a cursor for executing queries, commit transactions, roll back transactions, and close the connection. 
This class serves as a simple wrapper around the mysql.connector library to facilitate database operations in the application.

'''

class Database:

    # Initialize the database connection using provided credentials
    def __init__(self, host, database, user, password):
        self.connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        self.close()

    def get_cursor(self):
        return self.connection.cursor(dictionary=True)
    
    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()

    