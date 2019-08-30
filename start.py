#! /usr/bin/env python3
# coding: UTF-8


import json
import requests

import mysql.connector

import settings as st
import database as db


class Application:
    """ Main class """
    def __init__(self):
        """ Initialize """
        self.database = db.MyDatabase()

        self.my_categories = [st.SEARCH_1, st.SEARCH_2, st.SEARCH_3]

        start = self.database.first_connection()

        if not start:
            self.database.create_database()
            self.my_requests()

        self.start_menu()


    def start_menu(self):
        print ("\nMENU > Entrer le chiffre correspondant à votre choix. ")
        print ("\n1 - Quel aliment souhaitez-vous remplacer ? ")
        print ("2 - Retrouver mes aliments substitués ")

        choice = input("\nVotre choix : ")
        if str(choice) == "1":
            categories = self.database.show_categories()
            self.category_menu(categories)

        elif str(choice) == "2":
            self.save_product_menu()
            self.start_menu()

        else:
            print ("Erreur : Entrer un numéro valide.")
            self.start_menu()

    def category_menu(self, number_of_category):
        category_choice = input("\nEntrez le numéro de la catégorie : ")
        if category_choice in number_of_category:
            products = self.database.show_products(category_choice)
            self.select_product_menu(products, category_choice)
            
        else:
            print ("Erreur : Entrer un numéro valide.")
            self.category_menu(number_of_category)

    def select_product_menu(self, products, category_choice):
        print(products)

        choice = input("\nEntrez le numéro de l'aliment : ")
        if choice in products:
            
            proposition = self.database.proposition(choice, category_choice)
            if proposition:
                self.save_menu(choice, proposition)
            else:
                self.select_product_menu(products, category_choice)

        else:
            print ("Erreur : Entrer un numéro valide.")
            self.select_product_menu(products, category_choice)


    def save_menu(self, product, new_product):
        print ("\nMENU > Voulez-vous enregistrer cet aliment ? ")
        print ("\n1 - Oui ")
        print ("2 - Non, je veux choisir un autre aliment ")
        print ("3 - Retourner au menu principal ")

        choice = input("\nVotre choix : ")
        if choice == "1":
            self.database.save(product, new_product)
            self.start_menu()
            
        elif choice == "2":
            categories = self.database.show_categories()
            self.category_menu(categories)

        elif choice == "3":
            self.start_menu()

        else:
            print ("Erreur : Entrer un numéro valide.")
            self.save_menu(product, new_product)

    def save_product_menu(self):
        self.database.show_new_products()

    def my_requests(self):
        """ Requests GET on API """
        for category in self.my_categories:
            category_id = self.database.insert_category(category)

            i = 0
            nutriscore = "a"
            while i != 3:
                my_research = requests.get(
                    "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_tag=categories"
                    "&sort_by=unique_scans_n&nutrition_grades={}&page_size=6&json=1".format(category, nutriscore))

                results = my_research.json()
                products = results["products"]
                
                try:
                    for product in products:
                        product_name = product["product_name_fr"]
                        ingredients = product["ingredients_text"]
                        store = str(product['stores_tags']).replace("'", "").replace("[", "").replace("]", "")
                        url = product["url"]
                        nutrition_grade = str(product['nutrition_grade_fr']).replace("'", "").replace("[", "").replace("]", "")

                        self.database.insert_food(product_name, ingredients, category_id, store, url, nutrition_grade)

                except KeyError:
                    continue

                # letter + 1
                c = ord(nutriscore[0]) + 1
                nutriscore = chr(c)
                i += 1
        self.database.new_connection_close()


def main():
    start = Application()


if __name__ == "__main__":
    main()