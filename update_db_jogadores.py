import sqlite3

def criar_bd():
    conn = sqlite3.connect("db/biblioteca_jogos.db")
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
        );
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            vitorias INTEGER DEFAULT 0
        );
    ''')
    
    conn.commit()
    conn.close()
    print("Base de dados e tabelas criadas!")

def atualizar_tabela_jogadores():
    conn = sqlite3.connect("db/biblioteca_jogos.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Jogadores_novo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            vitorias INTEGER DEFAULT 0
        );
    ''')
    
    cursor.execute('''
        INSERT INTO Jogadores_novo (id, nome)
        SELECT id, nome FROM Jogadores;
    ''')
    
    cursor.execute('DROP TABLE Jogadores;')
    cursor.execute('ALTER TABLE Jogadores_novo RENAME TO Jogadores;')
    
    conn.commit()
    conn.close()
    print("Tabela Jogadores atualizada com sucesso!")

if __name__ == "__main__":
    criar_bd()
    atualizar_tabela_jogadores()
