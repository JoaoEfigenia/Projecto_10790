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
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            vitorias INTEGER DEFAULT 0
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_jogo INTEGER,
            data TEXT,
            vencedor_id INTEGER,
            FOREIGN KEY (id_jogo) REFERENCES Jogos(id),
            FOREIGN KEY (vencedor_id) REFERENCES Jogadores(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Partidas_Jogadores (
            id_partida INTEGER,
            id_jogador INTEGER,
            FOREIGN KEY (id_partida) REFERENCES Partidas(id),
            FOREIGN KEY (id_jogador) REFERENCES Jogadores(id)
        );
    ''')

    conn.commit()
    conn.close()

def adicionar_jogo():
    nome = input("Nome do jogo: ")
    genero = input("Género: ")
    max_jogadores = int(input("Número máximo de jogadores: "))
    dependencia_lingua = input("Dependência de língua (S/N): ").upper()
    complexidade = float(input("Complexidade (1 a 5): "))
    link_bgg = input("Link BGG: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Jogos (nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg))

    conn.commit()
    conn.close()
    print(f"Jogo '{nome}' adicionado com sucesso!")

def listar_jogos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg FROM Jogos")
    jogos = cursor.fetchall()

    conn.close()
    if not jogos:
        print("Não há jogos registados.")
    else:
        for jogo in jogos:
            print(f"ID: {jogo[0]}, Nome: {jogo[1]}, Género: {jogo[2]}, Max Jogadores: {jogo[3]}, Dependência de Língua: {jogo[4]}, Complexidade: {jogo[5]}, Link BGG: {jogo[6]}")

def editar_jogo():
    listar_jogos()
    jogo_id = input("ID do jogo que quer editar: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Jogos WHERE id = ?", (jogo_id,))
    jogo = cursor.fetchone()
    if not jogo:
        print("Jogo não encontrado.")
        conn.close()
        return

    nome = input(f"Nome ({jogo[1]}): ") or jogo[1]
    genero = input(f"Género ({jogo[2]}): ") or jogo[2]
    max_jogadores = input(f"Número máximo de jogadores ({jogo[3]}): ") or jogo[3]
    dependencia_lingua = input(f"Dependência de língua (S/N) ({jogo[4]}): ").upper() or jogo[4]
    complexidade = input(f"Complexidade (1 a 5) ({jogo[5]}): ") or jogo[5]
    link_bgg = input(f"Link BGG ({jogo[6]}): ") or jogo[6]

    try:
        max_jogadores = int(max_jogadores)
        complexidade = float(complexidade)
    except ValueError:
        print("Número máximo de jogadores deve ser inteiro e complexidade deve ser número (float).")
        conn.close()
        return

    cursor.execute('''
        UPDATE Jogos SET nome = ?, genero = ?, max_jogadores = ?, dependencia_lingua = ?, complexidade = ?, link_bgg = ?
        WHERE id = ?
    ''', (nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg, jogo_id))

    conn.commit()
    conn.close()
    print("Jogo atualizado com sucesso!")

def eliminar_jogo():
    listar_jogos()
    jogo_id = input("ID do jogo que quer eliminar: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Jogos WHERE id = ?", (jogo_id,))
    jogo = cursor.fetchone()
    if not jogo:
        print("Jogo não encontrado.")
        conn.close()
        return

    confirm = input(f"Tem certeza que quer eliminar o jogo '{jogo[1]}'? (S/N): ").upper()
    if confirm == 'S':
        cursor.execute("DELETE FROM Jogos WHERE id = ?", (jogo_id,))
        conn.commit()
        print("Jogo eliminado com sucesso!")
    else:
        print("Eliminação cancelada.")
    conn.close()

def adicionar_jogador():
    nome = input("Nome do jogador: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Jogadores (nome, vitorias) VALUES (?, ?)", (nome, 0))

    conn.commit()
    conn.close()
    print(f"Jogador '{nome}' adicionado com sucesso!")

def listar_jogadores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, vitorias FROM Jogadores")
    jogadores = cursor.fetchall()

    conn.close()
    if not jogadores:
        print("Não há jogadores registados.")
    else:
        for jogador in jogadores:
            print(f"ID: {jogador[0]}, Nome: {jogador[1]}, Vitórias: {jogador[2]}")

def eliminar_jogador():
    listar_jogadores()
    jogador_id = input("ID do jogador que quer eliminar: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Jogadores WHERE id = ?", (jogador_id,))
    jogador = cursor.fetchone()
    if not jogador:
        print("Jogador não encontrado.")
        conn.close()
        return

    confirm = input(f"Tem certeza que quer eliminar o jogador '{jogador[1]}'? (S/N): ").upper()
    if confirm == 'S':
        cursor.execute("DELETE FROM Jogadores WHERE id = ?", (jogador_id,))
        conn.commit()
        print("Jogador eliminado com sucesso!")
    else:
        print("Eliminação cancelada.")
    conn.close()

def registar_partida():
    listar_jogos()
    id_jogo = input("ID do jogo jogado: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Jogos WHERE id = ?", (id_jogo,))
    jogo = cursor.fetchone()
    if not jogo:
        print("Jogo não encontrado.")
        conn.close()
        return

    data = input("Data da partida (YYYY-MM-DD): ")
    listar_jogadores()
    vencedor_id = input("ID do vencedor: ")

    cursor.execute("SELECT * FROM Jogadores WHERE id = ?", (vencedor_id,))
    vencedor = cursor.fetchone()
    if not vencedor:
        print("Jogador vencedor não encontrado.")
        conn.close()
        return

    cursor.execute("INSERT INTO Partidas (id_jogo, data, vencedor_id) VALUES (?, ?, ?)", (id_jogo, data, vencedor_id))
    partida_id = cursor.lastrowid

    jogadores_partida = input("IDs dos jogadores participantes (separados por vírgula): ").split(",")
    for j_id in jogadores_partida:
        j_id = j_id.strip()
        cursor.execute("SELECT * FROM Jogadores WHERE id = ?", (j_id,))
        if cursor.fetchone():
            cursor.execute("INSERT INTO Partidas_Jogadores (id_partida, id_jogador) VALUES (?, ?)", (partida_id, j_id))

    conn.commit()
    conn.close()
    print("Partida registada com sucesso!")

def listar_partidas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.id, j.nome, p.data, jog.nome
        FROM Partidas p
        LEFT JOIN Jogos j ON p.id_jogo = j.id
        LEFT JOIN Jogadores jog ON p.vencedor_id = jog.id
    ''')
    partidas = cursor.fetchall()

    if not partidas:
        print("Não há partidas registadas.")
        conn.close()
        return

    for partida in partidas:
        partida_id = partida[0]
        jogo_nome = partida[1]
        data = partida[2]
        vencedor_nome = partida[3]

        cursor.execute('''
            SELECT jog.nome
            FROM Partidas_Jogadores pj
            JOIN Jogadores jog ON pj.id_jogador = jog.id
            WHERE pj.id_partida = ?
        ''', (partida_id,))
        jogadores = cursor.fetchall()
        nomes_jogadores = ", ".join([j[0] for j in jogadores])

        print(f"ID: {partida_id}, Jogo: {jogo_nome}, Data: {data}, Vencedor: {vencedor_nome}, Jogadores: {nomes_jogadores}")

    conn.close()

def eliminar_partida():
    listar_partidas()
    partida_id = input("ID da partida que quer eliminar: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Partidas WHERE id = ?", (partida_id,))
    partida = cursor.fetchone()
    if not partida:
        print("Partida não encontrada.")
        conn.close()
        return

    confirm = input("Tem certeza que quer eliminar esta partida? (S/N): ").upper()
    if confirm == 'S':
        cursor.execute("DELETE FROM Partidas_Jogadores WHERE id_partida = ?", (partida_id,))
        cursor.execute("DELETE FROM Partidas WHERE id = ?", (partida_id,))
        conn.commit()
        print("Partida eliminada com sucesso!")
    else:
        print("Eliminação cancelada.")
    conn.close()

def filtrar_jogos():
    print("Preencha os filtros desejados (deixe vazio para ignorar):")
    nome = input("Nome: ").strip()
    genero = input("Género: ").strip()
    max_jogadores = input("Número máximo de jogadores: ").strip()
    dependencia_lingua = input("Dependência de língua (S/N): ").strip().upper()
    complexidade_min = input("Complexidade mínima (1 a 5): ").strip()
    complexidade_max = input("Complexidade máxima (1 a 5): ").strip()
    
    filtro_nao_jogados = input("Filtrar jogos que o jogador ainda não jogou? (S/N): ").strip().upper()
    
    jogador_id = None
    if filtro_nao_jogados == "S":
        jogador_nome = input("Nome do jogador para filtro: ").strip()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Jogadores WHERE nome = ?", (jogador_nome,))
        resultado = cursor.fetchone()
        if resultado:
            jogador_id = resultado[0]
        else:
            print(f"Jogador '{jogador_nome}' não encontrado. Ignorando filtro de não jogados.")
        conn.close()

    query = "SELECT id, nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg FROM Jogos WHERE 1=1"
    params = []

    if nome:
        query += " AND nome LIKE ?"
        params.append(f"%{nome}%")
    if genero:
        query += " AND genero LIKE ?"
        params.append(f"%{genero}%")
    if max_jogadores:
        try:
            max_jog = int(max_jogadores)
            query += " AND max_jogadores = ?"
            params.append(max_jog)
        except ValueError:
            print("Número máximo de jogadores inválido, ignorando este filtro.")
    if dependencia_lingua in ("S", "N"):
        query += " AND dependencia_lingua = ?"
        params.append(dependencia_lingua)
    if complexidade_min:
        try:
            cmin = float(complexidade_min)
            query += " AND complexidade >= ?"
            params.append(cmin)
        except ValueError:
            print("Complexidade mínima inválida, ignorando este filtro.")
    if complexidade_max:
        try:
            cmax = float(complexidade_max)
            query += " AND complexidade <= ?"
            params.append(cmax)
        except ValueError:
            print("Complexidade máxima inválida, ignorando este filtro.")

    if jogador_id:
        query = f'''
            SELECT j.id, j.nome, j.genero, j.max_jogadores, j.dependencia_lingua, j.complexidade, j.link_bgg
            FROM Jogos j
            WHERE j.id NOT IN (
                SELECT id_jogo FROM Partidas p
                INNER JOIN Partidas_Jogadores pj ON p.id = pj.id_partida
                WHERE pj.id_jogador = ?
            )
        '''
        filtros_restantes = []
        params_restantes = [jogador_id]

        if nome:
            filtros_restantes.append("j.nome LIKE ?")
            params_restantes.append(f"%{nome}%")
        if genero:
            filtros_restantes.append("j.genero LIKE ?")
            params_restantes.append(f"%{genero}%")
        if max_jogadores:
            try:
                max_jog = int(max_jogadores)
                filtros_restantes.append("j.max_jogadores = ?")
                params_restantes.append(max_jog)
            except ValueError:
                pass
        if dependencia_lingua in ("S", "N"):
            filtros_restantes.append("j.dependencia_lingua = ?")
            params_restantes.append(dependencia_lingua)
        if complexidade_min:
            try:
                cmin = float(complexidade_min)
                filtros_restantes.append("j.complexidade >= ?")
                params_restantes.append(cmin)
            except ValueError:
                pass
        if complexidade_max:
            try:
                cmax = float(complexidade_max)
                filtros_restantes.append("j.complexidade <= ?")
                params_restantes.append(cmax)
            except ValueError:
                pass

        if filtros_restantes:
            query += " AND " + " AND ".join(filtros_restantes)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params_restantes)
        jogos = cursor.fetchall()
        conn.close()
    else:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        jogos = cursor.fetchall()
        conn.close()

    if not jogos:
        print("Nenhum jogo encontrado com esses filtros.")
    else:
        for jogo in jogos:
            print(f"ID: {jogo[0]}, Nome: {jogo[1]}, Género: {jogo[2]}, Max Jogadores: {jogo[3]}, Dependência Língua: {jogo[4]}, Complexidade: {jogo[5]}, Link BGG: {jogo[6]}")

def menu_jogos():
    while True:
        print("\n--- Menu Jogos ---")
        print("1 - Adicionar Jogo")
        print("2 - Editar Jogo")
        print("3 - Eliminar Jogo")
        print("4 - Listar Jogos")
        print("5 - Filtrar Jogos")
        print("0 - Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            adicionar_jogo()
        elif escolha == "2":
            editar_jogo()
        elif escolha == "3":
            eliminar_jogo()
        elif escolha == "4":
            listar_jogos()
        elif escolha == "5":
            filtrar_jogos()
        elif escolha == "0":
            break
        else:
            print("Opção inválida.")

def menu_jogadores():
    while True:
        print("\n--- Menu Jogadores ---")
        print("1 - Adicionar Jogador")
        print("2 - Listar Jogadores")
        print("3 - Eliminar Jogador")
        print("0 - Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            adicionar_jogador()
        elif escolha == "2":
            listar_jogadores()
        elif escolha == "3":
            eliminar_jogador()
        elif escolha == "0":
            break
        else:
            print("Opção inválida.")

def menu_partidas():
    while True:
        print("\n--- Menu Partidas ---")
        print("1 - Registar Partida")
        print("2 - Listar Partidas")
        print("3 - Eliminar Partida")
        print("0 - Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            registar_partida()
        elif escolha == "2":
            listar_partidas()
        elif escolha == "3":
            eliminar_partida()
        elif escolha == "0":
            break
        else:
            print("Opção inválida.")

def menu_principal():
    criar_bd()
    while True:
        print("\n--- Menu Principal ---")
        print("1 - Jogos")
        print("2 - Jogadores")
        print("3 - Partidas")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            menu_jogos()
        elif escolha == "2":
            menu_jogadores()
        elif escolha == "3":
            menu_partidas()
        elif escolha == "0":
            print("Adeus!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()
