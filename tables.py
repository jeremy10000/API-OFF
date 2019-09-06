#! /usr/bin/env python3
# coding: UTF-8

import random
import mysql.connector

from database import MyDatabase

"""
    Make requests in the database.
"""


class Category(MyDatabase):
    """ This class performs operations in the table : Category """

    def insert_category(self, category):
        """ Insert a category in the database and return its ID. """

        self.cursor.execute("""
            INSERT INTO Category (category)
            VALUES (%s)
            """, (category, ))
        self.connection.commit()

        print("\nLa catégorie", category, "a été ajoutée avec succès.")

        self.cursor.execute("""
            SELECT id
            FROM Category
            WHERE category = '{}';""".format(category))
        category_id = self.cursor.fetchone()

        return category_id[0]

    def show_categories(self):
        """ Display categories. """

        self.new_connection()
        self.cursor.execute("""
            SELECT id, category
            FROM Category
            ORDER BY id;""")
        results = self.cursor.fetchall()
        self.new_connection_close()

        categories_id = []

        for _id, _category in results:
            categories_id.append(str(_id))
            print("[", _id, "] -", _category)

        return categories_id


class Save(MyDatabase):
    """ This class performs operations in the table : Save """

    def save_products(self, product_id, new_product_id):
        """ Register products in the database. """

        self.new_connection()
        try:
            self.cursor.execute("""
                INSERT INTO Save (id_product, id_new_product)
                VALUES (%s, %s)""",
                                (product_id, new_product_id))
            self.connection.commit()

            print("\nVotre choix est enregistré.")

        except mysql.connector.errors.IntegrityError as e:
            print("\nCe choix est déjà enregistré.")
        self.new_connection_close()

    def show_new_products(self):
        """ Display the products registered in the database. """

        self.new_connection()
        self.cursor.execute("""
            SELECT Product.name
            FROM Product
            INNER JOIN Save
            ON Product.id = Save.id_product
            WHERE Product.id = Save.id_product
            ORDER BY Save.id;""")
        products = self.cursor.fetchall()

        self.cursor.execute("""
            SELECT Product.name
            FROM Product
            INNER JOIN Save
            ON Product.id = Save.id_new_product
            WHERE Product.id = Save.id_new_product
            ORDER BY Save.id;""")
        new_products = self.cursor.fetchall()
        self.new_connection_close()

        if not products:
            print("\nVous n'avez rien enregistré.")
        else:
            for p_name, n_name in zip(products, new_products):
                print(p_name[0], "est remplacé par", n_name[0])


class Product(MyDatabase):
    """ This class performs operations in the table : Product """

    def insert_food(self, p_name, ingredients,
                    cat_id, store, url, nutriscore):
        """ Insert products into the database. """

        try:
            self.cursor.execute("""
                INSERT INTO Product (name, description, category,
                                     store, url, nutrition_grade)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                                (p_name, ingredients, cat_id,
                                    store, url, nutriscore))

            self.connection.commit()
            print("Ajout :", p_name)

        except mysql.connector.errors.IntegrityError as e:
            print("Erreur :", e)

    def show_products(self, category_id):
        """ Display the products of a category. """

        self.new_connection()
        self.cursor.execute("""
            SELECT category
            FROM Category
            WHERE id = {};""".format(category_id))
        results = self.cursor.fetchone()

        print("\nVoici les aliments de la catégorie :", results[0])

        self.cursor.execute("""
            SELECT id, name
            FROM Product
            WHERE category = '{}'
            ORDER BY id;""".format(category_id))
        results = self.cursor.fetchall()
        self.new_connection_close()

        products_id = []

        for _id, _name in results:
            products_id.append(str(_id))
            print("[", _id, "] -", _name)

        return products_id

    def proposition(self, id_product, category_id):
        """ Select a new product at random. """

        self.new_connection()
        self.cursor.execute("""
            SELECT id, name, nutrition_grade
            FROM Product
            WHERE id = {};""".format(id_product))
        product = self.cursor.fetchone()

        # The nutriscore of the selected product.
        self.nutriscore_selected = product[2]

        search = self.select_by_nutriscore(category_id)
        self.new_connection_close()

        if search is False:
            return False

        i = 0
        for _id, _name, _nutrition_grade, \
                _description, _store, _url in search:

            # If the selected product is in the list, it is deleted.
            if int(id_product) == _id:
                search.remove(search[i])
            i += 1

        propose = random.randrange(len(search))

        print("\n->", product[1], "( nutriscore", product[2], ")")
        print("peut être remplacé par :", search[propose][1],
              "( nutriscore", search[propose][2], ")\n")

        print("Description :", search[propose][3], "\n")
        print("Magasin(s) :", search[propose][4], "\n")
        print("Lien :", search[propose][5], "\n---")

        my_proposition = search[propose][0]
        return my_proposition

    def select_by_nutriscore(self, category_id, nutriscore="a"):
        """ Select new products by its nutriscore. """

        while True:
            self.cursor.execute("""
                SELECT id, name, nutrition_grade, description, store, url
                FROM Product
                WHERE nutrition_grade = '{}'
                AND category = '{}';""".format(nutriscore, category_id))
            results = self.cursor.fetchall()

            # If results is empty or if the selected product
            # is the only one with this nutriscore.
            if not results or \
                    (self.nutriscore_selected == nutriscore and
                        len(results) == 1):

                print("Nous avons aucun substitut avec un nutriscore",
                      nutriscore.upper(),
                      "à vous proposer pour cet aliment.")

                # Stop if the nutriscore = the nutriscore of the product
                if self.nutriscore_selected == nutriscore:
                    return False

                # letter + 1
                c = ord(nutriscore[0]) + 1
                nutriscore = chr(c)
            else:
                break

        return results
