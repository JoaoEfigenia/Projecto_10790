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
    conn.commit()
    conn.close()

def inserir_jogo(nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg):
    conn = sqlite3.connect("db/biblioteca_jogos.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Jogos (nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg))
    conn.commit()
    conn.close()
    print(f"Jogo '{nome}' inserido com sucesso!")

def listar_jogos(filtro_genero=None, filtro_max_jogadores=None, filtro_dependencia_lingua=None, filtro_complexidade_max=None):
    conn = sqlite3.connect("db/biblioteca_jogos.db")
    cursor = conn.cursor()
    
    query = "SELECT * FROM Jogos WHERE 1=1"
    parametros = []
    
    if filtro_genero:
        query += " AND genero = ?"
        parametros.append(filtro_genero)
    if filtro_max_jogadores:
        query += " AND max_jogadores >= ?"
        parametros.append(filtro_max_jogadores)
    if filtro_dependencia_lingua:
        query += " AND dependencia_lingua = ?"
        parametros.append(filtro_dependencia_lingua)
    if filtro_complexidade_max:
        query += " AND complexidade <= ?"
        parametros.append(filtro_complexidade_max)
    
    cursor.execute(query, parametros)
    jogos = cursor.fetchall()
    conn.close()
    
    if jogos:
        print("\nJogos encontrados:")
        for jogo in jogos:
            print(f"ID: {jogo[0]}, Nome: {jogo[1]}, Género: {jogo[2]}, Max Jogadores: {jogo[3]}, Dependência de Língua: {jogo[4]}, Complexidade: {jogo[5]}, Link BGG: {jogo[6]}")
    else:
        print("Nenhum jogo encontrado com os filtros aplicados.")

def menu():
    criar_bd()
    while True:
        print("\n--- Gestão da Base de Dados de Jogos ---")
        print("1. Inserir novo jogo")
        print("2. Listar todos os jogos")
        print("3. Listar jogos filtrados")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do jogo: ")
            genero = input("Género: ")
            max_jogadores = int(input("Número máximo de jogadores: "))
            dependencia_lingua = input("Dependência de língua (Sim/Não): ")
            complexidade = float(input("Complexidade (1 a 5): "))
            link_bgg = input("Link BGG: ")
            inserir_jogo(nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg)

        elif opcao == "2":
            listar_jogos()

        elif opcao == "3":
            filtro_genero = input("Filtrar por género (deixe vazio para não filtrar): ").strip() or None
            filtro_max_jogadores = input("Filtrar por número mínimo de jogadores (deixe vazio para não filtrar): ").strip()
            filtro_max_jogadores = int(filtro_max_jogadores) if filtro_max_jogadores else None
            filtro_dependencia_lingua = input("Filtrar por dependência de língua (Sim/Não, deixe vazio para não filtrar): ").strip() or None
            filtro_complexidade_max = input("Filtrar por complexidade máxima (1 a 5, deixe vazio para não filtrar): ").strip()
            filtro_complexidade_max = float(filtro_complexidade_max) if filtro_complexidade_max else None

            listar_jogos(filtro_genero, filtro_max_jogadores, filtro_dependencia_lingua, filtro_complexidade_max)

        elif opcao == "0":
            print("A sair...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
