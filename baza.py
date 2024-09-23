import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self, host, user, password, database, port):
        try:
            connect = mysql.connector.connect(host=host, user=user, password=password, port=port)
            self.conn = connect
            self.cursor = self.conn.cursor()

            self.cursor.execute(f"create database if not exists {database}")
            self.conn.commit()

            self.conn.database = database

            self.create_tables()

        except Error as e:
            print(f"Błąd przy utworzeniu bazy lub połączeniu: {e}")
            self.conn = None

    def create_tables(self):
        try:
            self.cursor.execute("""
                create table if not exists uzytkownik (
                    id int auto_increment primary key,
                    login VARCHAR(255) UNIQUE NOT NULL,
                    pass VARCHAR(255) NOT NULL
                )
            """)

            self.cursor.execute("""
                create table if not exists note (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    zawartosc TEXT NOT NULL,
                    user_id INT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.conn.commit()

        except Error as e:
            print(f"Błąd przy utworzeniu tabel: {e}")
            self.conn = None

    def check_user(self, login, password):
        query = "select * from users where login = %s and password = %s"
        self.cursor.execute(query, (login, password))
        user = self.cursor.fetchone()
        return user

    def insert_user(self, login, password):
        try:
            query = "INSERT INTO users (login, password) VALUES (%s, %s)"
            self.cursor.execute(query, (login, password))
            self.conn.commit()
        except mysql.connector.IntegrityError:
            return False
        return True

    def get_user_id(self, login):
        query = "SELECT id FROM users WHERE login = %s"
        self.cursor.execute(query, (login,))
        user_id = self.cursor.fetchone()
        return user_id[0] if user_id else None

    def select_notes_by_user(self, user_id):
        query = "SELECT * FROM notes WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        notes = self.cursor.fetchall()
        return notes

    def insert_note(self, tresc, user_id):
        query = "INSERT INTO notes (tresc, user_id) VALUES (%s, %s)"
        self.cursor.execute(query, (tresc, user_id))
        self.conn.commit()

    def delete_note(self, note_id):
        query = "DELETE FROM notes WHERE id = %s"
        self.cursor.execute(query, (note_id,))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()