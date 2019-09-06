#! /usr/bin/env python3
# coding: UTF-8

import requests

from tables import Category, Product

"""
    Make requests on the API.
"""


class RequestsApi(Category, Product):
    """ This class makes requests on the API (OpenFoodFacts)
        to find foods and save them in the database. """
    def __init__(self):
        """ Set categories """
        self.my_categories = ["Fromages", "Gâteaux", "Jus de fruits"]

    def my_requests(self):
        """ Make three requests on the API by categories
            (nutriscore A, B and C) """
        self.new_connection()
        for category in self.my_categories:
            category_id = self.insert_category(category)

            i = 0
            nutriscore = "a"
            while i != 3:
                my_research = requests.get(
                    "https://fr.openfoodfacts.org/cgi/search.pl?"
                    "search_terms={}&search_tag=categories"
                    "&sort_by=unique_scans_n&nutrition_grades={}"
                    "&page_size=6&json=1".format(category, nutriscore))

                results = my_research.json()
                products = results["products"]

                try:
                    for product in products:
                        product_name = product["product_name_fr"]
                        ingredients = product["ingredients_text"]
                        store = str(product['stores_tags']).replace("'", "") \
                                                           .replace("[", "") \
                                                           .replace("]", "")
                        url = product["url"]
                        nutrition_grade = str(product['nutrition_grade_fr']) \
                            .replace("'", "") \
                            .replace("[", "") \
                            .replace("]", "")

                        self.insert_food(product_name, ingredients,
                                         category_id, store,
                                         url, nutrition_grade)

                except KeyError:
                    continue

                # letter + 1
                c = ord(nutriscore[0]) + 1
                nutriscore = chr(c)
                i += 1
        self.new_connection_close()
