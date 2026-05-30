import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("financeiro.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor REAL NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            mes TEXT,
            nome TEXT,
            valor REAL
        )
        """)

        self.conn.commit()

    def executar(self, sql, parametros=()):
        self.cursor.execute(sql, parametros)
        self.conn.commit()

    def buscar(self, sql, parametros=()):
        self.cursor.execute(sql, parametros)
        return self.cursor.fetchall()
