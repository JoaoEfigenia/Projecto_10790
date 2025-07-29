import sqlite3
import os

DB_PATH = "db/biblioteca_jogos.db"

def criar_bd():
    if not os.path.exists("db"):
        os.makedirs("db")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            genero TEXT,
            max_jogadores INTEGER,
            dependencia_lingua TEXT,
            complexidade REAL CHECK(complexidade BETWEEN 1 AND 5),
            link_bgg TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            vitorias INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('DROP TABLE IF EXISTS Partidas')

    cursor.execute('''
        CREATE TABLE Partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_jogo INTEGER NOT NULL,
            data TEXT NOT NULL,
            jogadores TEXT NOT NULL,
            vencedor_id INTEGER,
            FOREIGN KEY (id_jogo) REFERENCES Jogos(id),
            FOREIGN KEY (vencedor_id) REFERENCES Jogadores(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de dados criada/atualizada com sucesso.")

if __name__ == "__main__":
    criar_bd()