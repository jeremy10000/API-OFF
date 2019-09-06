#! /usr/bin/env python3
# coding: UTF-8

import database as db
import tables as tb
import requests_api as req

"""
    This file starts the program.
"""


class Application:
    """ This class displays the menus and and interacts with other classes. """

    def __init__(self):
        """ Initialize """
        self.database = db.MyDatabase()
        self.t_category = tb.Category()
        self.t_save = tb.Save()
        self.t_product = tb.Product()
        self.r_api = req.RequestsApi()

        start = self.database.first_connection()

        if not start:
            self.r_api.my_requests()

        self.start_menu()

    def start_menu(self):
        """ Display the first menu. """

        print("\nMENU > Entrer le chiffre correspondant à votre choix. ")
        print("\n1 - Quel aliment souhaitez-vous remplacer ? ")
        print("2 - Retrouver mes aliments substitués ")

        choice = input("\nVotre choix : ")
        if choice == "1":
            # Display categories.
            categories = self.t_category.show_categories()
            self.category_menu(categories)

        elif choice == "2":
            # View registered products.
            self.t_save.show_new_products()
            self.start_menu()

        else:
            print("Erreur : Entrer un numéro valide.")
            self.start_menu()

    def category_menu(self, number_of_category):
        """ Display categories. """

        category_choice = input("\nEntrez le numéro de la catégorie : ")
        if category_choice in number_of_category:
            products = self.t_product.show_products(category_choice)
            self.select_product_menu(products, category_choice)

        else:
            print("Erreur : Entrer un numéro valide.")
            self.category_menu(number_of_category)

    def select_product_menu(self, products, category_choice):
        """ Ask the user to choose a product. """

        choice = input("\nEntrez le numéro de l'aliment : ")
        if choice in products:

            proposition = self.t_product.proposition(choice, category_choice)
            if proposition:
                self.save_menu(choice, proposition)
            else:
                self.select_product_menu(products, category_choice)

        else:
            print("Erreur : Entrer un numéro valide.")
            self.select_product_menu(products, category_choice)

    def save_menu(self, product, new_product):
        """ Ask the user to register the products. """

        print("\nMENU > Voulez-vous enregistrer cet aliment ? ")
        print("\n1 - Oui ")
        print("2 - Non, je veux choisir un autre aliment ")
        print("3 - Retourner au menu principal ")

        choice = input("\nVotre choix : ")
        if choice == "1":
            self.t_save.save_products(product, new_product)
            self.start_menu()

        elif choice == "2":
            categories = self.t_category.show_categories()
            self.category_menu(categories)

        elif choice == "3":
            self.start_menu()

        else:
            print("Erreur : Entrer un numéro valide.")
            self.save_menu(product, new_product)


def main():
    """ Start """
    start = Application()


if __name__ == "__main__":
    main()
