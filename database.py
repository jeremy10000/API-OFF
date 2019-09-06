#! /usr/bin/env python3
# coding: UTF-8

import sys

import mysql.connector

import settings as st

"""
    Creation and/or connection to the database.
"""


class MyDatabase:
    """ This class manages the connection to the database
        and its creation. """

    def first_connection(self):
        """ First connection to check that the database exists.
            If the database does not exist, it is created. """
        try:
            self.connection = mysql.connector.connect(
                user=st.USERNAME,
                password=st.PASSWORD,
                host=st.HOST,
                database=st.DATABASE)

            print("Connection à la base de données :", st.DATABASE)
            database_exist = True

        except mysql.connector.errors.ProgrammingError:
            self.connection = mysql.connector.connect(
                user=st.USERNAME,
                password=st.PASSWORD,
                host=st.HOST)

            print("La base de données", st.DATABASE, "n\'existe pas.")
            database_exist = False

        except mysql.connector.errors.InterfaceError:
            print("Impossible de se connecter. MySQL est-il actif ?")
            sys.exit()

        if self.connection.is_connected():
            if database_exist:
                self.connection.close()
            else:
                self.cursor = self.connection.cursor()
                self.create_database()

        return database_exist

    def create_database(self):
        """ Creation of the database. """
        print("Création de la base de données :", st.DATABASE)
        with open("script.sql", "r") as file:
            base = file.read()
            results = self.cursor.execute(base, multi=True)
            try:
                for result in results:
                    pass
            except Exception as e:
                pass

    def new_connection(self):
        """ Connection to the database. """
        self.connection = mysql.connector.connect(
            user=st.USERNAME,
            password=st.PASSWORD,
            host=st.HOST,
            database=st.DATABASE)

        if self.connection.is_connected():
            self.cursor = self.connection.cursor()

    def new_connection_close(self):
        """ Disconnection from the database. """
        self.connection.close()
