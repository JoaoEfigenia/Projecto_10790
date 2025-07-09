import sqlite3

conn = sqlite3.connect("db/biblioteca_jogos.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Jogos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        genero TEXT,
        max_jogadores INTEGER,
        dependencia_lingua TEXT,
        complexidade INTEGER CHECK(complexidade BETWEEN 1 AND 5),
        link_bgg TEXT
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Jogadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Partidas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jogo_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        jogadores TEXT NOT NULL,
        FOREIGN KEY (jogo_id) REFERENCES Jogos(id)
    );
''')

conn.commit()
conn.close()

print("Base de dados criada com sucesso!")
