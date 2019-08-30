#! /usr/bin/env python3
# coding: UTF-8

import sys
import random
import mysql.connector

import settings as st


class MyDatabase:
    """ Main class """
    def first_connection(self):
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

            print("La base de données", st.DATABASE,"n\'existe pas.")
            database_exist = False

        except mysql.connector.errors.InterfaceError:
            print("Impossible de se connecter. MySQL est-il actif ?")
            sys.exit()
            
        if self.connection.is_connected():
            if database_exist:
                self.new_connection_close()
            else:
                self.cursor = self.connection.cursor()

        return database_exist

    def new_connection(self):
        self.connection = mysql.connector.connect(
            user=st.USERNAME, 
            password=st.PASSWORD, 
            host=st.HOST, 
            database=st.DATABASE)

        if self.connection.is_connected():
            self.cursor = self.connection.cursor()

    def new_connection_close(self):
        self.connection.close()

    def create_database(self):
        print ("BDD : CRÉATION.")
        with open("script.sql", "r") as file:
            base = file.read()
            results = self.cursor.execute(base, multi=True)
            try:
                for result in results:
                    pass
            except Exception as e:
                pass

    def insert_category(self, category):
        
        self.cursor.execute("""
            INSERT INTO Category (category) 
            VALUES (%s)
            """, (category, ))

        self.connection.commit()
        print("\nLa catégorie", category, "a été ajoutée avec succès.")

        self.cursor.execute("SELECT id FROM Category WHERE category = '{}';".format(category))
        _category = self.cursor.fetchone()

        # donne l'id de la catégorie
        return _category[0]

    def insert_food(self, product_name, ingredients, category_id, store, url, nutrition_grade):

        try:
            self.cursor.execute("""
                INSERT INTO Product (name, description, category, store, url, nutrition_grade) 
                VALUES (%s, %s, %s, %s, %s, %s)""", 
                (product_name, ingredients, category_id, store, url, nutrition_grade))

            self.connection.commit()
            print("Ajout :", product_name)

        except mysql.connector.errors.IntegrityError as e:
            print("Erreur :", e)

    def show_categories(self):

        self.new_connection()
        self.cursor.execute("""
            SELECT id, category 
            FROM Category 
            ORDER BY id;
            """)

        results = self.cursor.fetchall()
        self.new_connection_close()

        categories_id = []

        for _id, _category in results:
            categories_id.append(str(_id))
            print("[", _id, "] -", _category)

        return categories_id

    def show_products(self, category_id):
        
        self.new_connection()
        self.cursor.execute("""
            SELECT category 
            FROM Category 
            WHERE id = {};"""
            .format(category_id))

        results = self.cursor.fetchone()
        print("\nVoici les aliments de la catégorie :", results[0])

        self.cursor.execute("""
            SELECT id, name 
            FROM Product 
            WHERE category = '{}' 
            ORDER BY id;"""
            .format(category_id))

        results = self.cursor.fetchall()
        self.new_connection_close()

        products_id = []

        for _id, _name in results:
            products_id.append(str(_id))
            print("[", _id, "] -", _name)

        return products_id


    def select_by_nutriscore(self, category_id, nutriscore="a"):

        while True:
            self.cursor.execute("""
                SELECT id, name, nutrition_grade, description, store, url 
                FROM Product 
                WHERE nutrition_grade = '{}' 
                AND category = '{}';"""
                .format(nutriscore, category_id))

            results = self.cursor.fetchall()

            # If results is empty or if the selected product
            # is the only one with this nutriscore.
            if not results or (self.nutriscore_selected == nutriscore and len(results) == 1):
                print ("Nous avons aucun substitut avec un nutriscore", \
                        nutriscore.upper(), "à vous proposer pour cet aliment.")

                # Stop searching if the nutriscore = the nutriscore of the product
                if self.nutriscore_selected == nutriscore:
                    return False

                # letter + 1
                c = ord(nutriscore[0]) + 1
                nutriscore = chr(c)
            else:
                break

        return results

    def proposition(self, id_product, category_id):
        self.new_connection()
       
        self.cursor.execute("""
            SELECT id, name, nutrition_grade
            FROM Product 
            WHERE id = {};"""
            .format(id_product))

        product = self.cursor.fetchone()

        self.nutriscore_selected = product[2]

        search = self.select_by_nutriscore(category_id)
        self.new_connection_close()

        if search is False:
            return False

        new_product_list = []
        
        i = 0
        for _id, _name, _nutrition_grade, _description, _store, _url in search:
            if int(id_product) == _id:
                search.remove(search[i])
            
            new_product_list.append(str(search[i][0]))
            i += 1

        propose = random.randrange(len(new_product_list))

        my_proposition = search[int(propose)][0]

        print ("\n->", product[1], "( nutriscore", product[2], ")")
        print ("peut être remplacé par :", search[int(propose)][1], \
                "( nutriscore", search[int(propose)][2], ")\n")

        print ("Description :", search[int(propose)][3], "\n")
        print ("Magasin(s) :", search[int(propose)][4], "\n")
        print ("Lien :", search[int(propose)][5], "\n---")

        return my_proposition

    def save(self, product_id, new_product_id):
        self.new_connection()

        try:
            self.cursor.execute("""
                INSERT INTO Save (id_product, id_new_product) 
                VALUES (%s, %s)""", 
                (product_id, new_product_id))

            self.connection.commit()
            print("\nVotre choix est enregistré.")

        except mysql.connector.errors.IntegrityError as e:
            print ("\nL'aliment a déjà un subtitut.")

        self.new_connection_close()
        

    def show_new_products(self):
        self.new_connection()
       
        self.cursor.execute("""
            SELECT Product.name 
            FROM Product 
            JOIN Save 
            ON Product.id = Save.id_product 
            WHERE Product.id = Save.id_product 
            ORDER BY Save.id;""")
        _all = self.cursor.fetchall()

        self.cursor.execute("""
            SELECT Product.name 
            FROM Product 
            JOIN Save 
            ON Product.id = Save.id_new_product 
            WHERE Product.id = Save.id_new_product 
            ORDER BY Save.id;""")
        _alln = self.cursor.fetchall()

        self.new_connection_close()

        if not _all:
            print ("\nVous n'avez rien enregistré.")
        else:
            for _name, _name2 in zip(_all,_alln):
                print(_name[0], "est remplacé par", _name2[0])

