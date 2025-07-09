import sqlite3

DB_PATH = "db/biblioteca_jogos.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Partidas;")

print("Tabela 'Partidas' eliminada com sucesso.")

conn.commit()
conn.close()
