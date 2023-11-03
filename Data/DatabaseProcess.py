import sqlite3
import os

class DatabaseProcess():
    def __init__(self, database):
        """Initialisation de la connexion"""
        database_path = os.path.dirname(os.path.abspath((__file__))) + "/" + database
        self.con = sqlite3.connect(database_path, check_same_thread=False)
        # self.con.row_factory = sqlite3.Row # Retourner a chaque fis le resutat sous forme d'un dictionnaire

    def createUser(self, username, email, password):
        cursor = self.con.cursor() # Permert de communiquer avec la base de donnée
        query = f"INSERT INTO users (username, email, password) VALUES (?, ?, ?);"
        cursor.execute(query, (username, email, password))
        cursor.close()
        self.con.commit() # Appliquer les changements

    def getUsersId(self, username, password):
        cursor = self.con.cursor() # Permert de communiquer avec la base de donnée
        query = "SELECT id FROM users WHERE username = ? and password = ?;"
        cursor.execute(query, (username, password))
        results = cursor.fetchone()

        return results

    def getAll_Users(self):
        cursor = self.con.cursor() # Permert de communiquer avec la base de donnée
        query = "SELECT * FROM users;"
        cursor.execute(query)
        results = cursor.fetchall()

        return results

    def createUserResult(self, date, heure, bilan, prediction, user_id):
        cursor = self.con.cursor() # Permert de communiquer avec la base de donnée
        query = f"INSERT INTO results (date, heure, bilan, prediction, user_id) VALUES (?, ?, ?, ?, ?);"
        cursor.execute(query, (date, heure, bilan, prediction, user_id))
        cursor.close()
        self.con.commit() # Appliquer les changements

    def getUserResults(self, user_id):
        cursor = self.con.cursor() # Permert de communiquer avec la base de donnée
        query = "SELECT date, heure, bilan, prediction FROM results WHERE user_id = ? ORDER BY date;"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        return results

