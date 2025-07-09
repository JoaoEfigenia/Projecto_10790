import sqlite3

DB_PATH = "db/biblioteca_jogos.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ParticipantesPartida (
    id_partida INTEGER,
    id_jogador INTEGER,
    FOREIGN KEY (id_partida) REFERENCES Partidas(id),
    FOREIGN KEY (id_jogador) REFERENCES Jogadores(id)
);
''')

print("Tabela 'ParticipantesPartida' criada com sucesso.")

conn.commit()
conn.close()
