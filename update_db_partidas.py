import sqlite3
import os

DB_PATH = "db/biblioteca_jogos.db"

def atualizar_bd_partidas():
    if not os.path.exists("db"):
        os.makedirs("db")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_jogo INTEGER NOT NULL,
            data TEXT NOT NULL,
            vencedor_id INTEGER NOT NULL,
            FOREIGN KEY (id_jogo) REFERENCES Jogos(id),
            FOREIGN KEY (vencedor_id) REFERENCES Jogadores(id)
        );
    ''')

    conn.commit()
    conn.close()
    print("Base de dados atualizada com a tabela Partidas.")

if __name__ == "__main__":
    atualizar_bd_partidas()
