#! /usr/bin/env python3
# coding: UTF-8

import sys

import json
import requests
import random
import mysql.connector

import sett as st


class MyDatabase:
    """ Main class """
    def __init__(self):
        """ Initialize """
        self.details = st.DETAILS
        self.my_categories = [st.SEARCH_1, st.SEARCH_2, st.SEARCH_3, st.SEARCH_4, st.SEARCH_5]

        # connection MySQL
        self.connection()

        # database creation
        self.make_database()

        # requests on API
        self.my_requests()

    def connection(self):
        try:
            self.connection = mysql.connector.connect(user=st.USERNAME, password=st.PASSWORD, host=st.HOST)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()

                if self.details:
                    server_info = self.connection.get_server_info()
                    print("Connecté... MySQL Server version : ", server_info)

        except Error as e:
            print ("Erreur pendant la connection : ", e)

    def make_database(self):
        with open("script.sql", "r") as file:
            base2 = file.read()
            results = self.cursor.execute(base2, multi=True)
            try:
                for result in results:
                    pass
            except Exception as e:
                pass

    def insert_category(self, category):
        self.cursor.execute("USE Database_test;")
        insert = "INSERT IGNORE INTO Category (category) VALUES (%s)"
        self.cursor.execute(insert, (category, ))
        self.connection.commit()
        if self.details:
            print("\nLa catégorie :", category, "a été ajoutée avec succès.")

    def insert_food(self, product_name, ingredients, category, store_tags, url):
        self.cursor.execute("USE Database_test;")
        insert = "INSERT IGNORE INTO Food (name_food, description, category, store, url) VALUES (%s, %s, %s, %s, %s)"
        values = (product_name, ingredients, category, store_tags, url)
        self.cursor.execute(insert, values)
        self.connection.commit()
        if self.details:
            print("L'aliment :", product_name, "a été ajouté avec succès.")

    def all_categories(self):
        self.cursor.execute("USE Database_test;")
        #self.cursor.execute("""SELECT id, name_food FROM Food ORDER BY id;""")
        self.cursor.execute("SELECT id, category FROM Category ORDER BY id;")
        _all = self.cursor.fetchall()
        for _id, _name in _all:
            print("[", _id, "] -", _name)

    def products_list(self, category_id):
        _list = []
        self.cursor.execute("USE Database_test;")

        self.cursor.execute("SELECT category FROM Category WHERE id = {};".format(category_id))
        _category = self.cursor.fetchone()
        print("\nVoici les aliments de la catégorie :", _category[0])

        self.cursor.execute("SELECT id, name_food FROM Food WHERE category = '{}';".format(_category[0]))
        _all = self.cursor.fetchall()
        for _id, _name in _all:
            _list.append(str(_id))
            print("[", _id, "] -", _name)

        return _list

    def proposition(self, id_food, choice):
        self.cursor.execute("USE Database_test;")
        self.cursor.execute("SELECT name_food FROM Food WHERE id = {};".format(choice))
        _food = self.cursor.fetchone()
        print (_food[0],"peut être remplacé par l\'aliment suivant : \n")

        self.cursor.execute("SELECT name_food, description, store, url FROM Food WHERE id = {};".format(id_food))
        _food = self.cursor.fetchone()
        print (_food[0])
        print ("Description :",_food[1])
        print ("Magasin :",_food[2])
        print ("Lien :",_food[3])



    def my_requests(self):
        """ Requests GET on API """
        for category in self.my_categories:
            self.insert_category(category)

            my_research = requests.get(
                "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_tag=categories"
                "&sort_by=unique_scans_n&page_size=20&json=1".format(category))

            results = my_research.json()
            products = results["products"]
            
            for product in products:
                product_name = product["product_name_fr"]
                ingredients = product["ingredients_text"]
                store = product["stores_tags"]
                store_tags = "\'"+", ".join(product['stores_tags']).replace("'", "")+"\'"
                url = product["url"]
                self.insert_food(product_name, ingredients, category, store_tags, url)




                
class MyApplication:
    """ Main class """
    def __init__(self):
        """ Initialize """
        self._db = MyDatabase()
        self.start_menu()

    def start_menu(self):
        print ("\nMENU > Entrer le chiffre correspondant à votre choix. ")
        print ("\n1 - Quel aliment souhaitez-vous remplacer ? ")
        print ("2 - Retrouver mes aliments substitués ")

        choice = input("\nVotre choix : ")
        if str(choice) == "1":
            self._db.all_categories()
            self.category_menu()

        elif str(choice) == "2":
            pass

    def category_menu(self):
        choice = input("\nLe numéro de la catégorie : ")
        if str(choice) == "1":
            _list = self._db.products_list(choice)
            self.select_food_menu(_list)
        elif str(choice) == "2":
            _list = self._db.products_list(choice)
            self.select_food_menu()
        elif str(choice) == "3":
            _list = self._db.products_list(choice)
            self.select_food_menu()
        elif str(choice) == "4":
            _list = self._db.products_list(choice)
            self.select_food_menu()
        elif str(choice) == "5":
            _list = self._db.products_list(choice)
            self.select_food_menu()
        else:
            print("Erreur : Entrer un numéro")
            self.category_menu()

    def select_food_menu(self, list_of):
        choice = input("\nLe numéro de l'aliment : ")
        if choice in list_of:
            print("Oui : ", choice)
            list_of.remove(choice)

            new = random.sample(list_of, 1)
            print("new : ", new[0])
            print(list_of)
            list_of.remove(new[0])
            print(list_of)
            
            self._db.proposition(new[0], choice)
            
            self.select_food_menu(list_of)
        else:
            print("Non")
            print(choice)
            print(list_of)
            self.select_food_menu(list_of)


def main():
    start = MyApplication()


if __name__ == "__main__":
    main()