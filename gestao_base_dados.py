import sqlite3
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

DB_PATH = "db/biblioteca_jogos.db"

def criar_bd():
    if not os.path.exists("db"):
        os.makedirs("db")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS Jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            vitorias INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_jogo INTEGER NOT NULL,
            data TEXT NOT NULL,
            jogadores TEXT NOT NULL,
            vencedor_id INTEGER,
            FOREIGN KEY(id_jogo) REFERENCES Jogos(id),
            FOREIGN KEY(vencedor_id) REFERENCES Jogadores(id)
        )
    ''')
    conn.commit()
    conn.close()

class BibliotecaJogosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca de Jogos de Tabuleiro")
        self.geometry("900x600")
        self.resizable(False, False)

        self.create_widgets()
        criar_bd()
        self.carregar_todos()

    def create_widgets(self):
        self.tabControl = ttk.Notebook(self)
        self.tab_jogos = ttk.Frame(self.tabControl)
        self.tab_jogadores = ttk.Frame(self.tabControl)
        self.tab_partidas = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_jogos, text='Jogos')
        self.tabControl.add(self.tab_jogadores, text='Jogadores')
        self.tabControl.add(self.tab_partidas, text='Partidas')
        self.tabControl.pack(expand=1, fill="both")

        self.setup_tab_jogos()
        self.setup_tab_jogadores()
        self.setup_tab_partidas()

    ### --- Jogos Tab ---
    def setup_tab_jogos(self):
        frame = self.tab_jogos

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(btn_frame, text="Adicionar Jogo", command=self.adicionar_jogo_popup).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Editar Jogo", command=self.editar_jogo_popup).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Eliminar Jogo", command=self.eliminar_jogo).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Filtrar Jogos", command=self.filtrar_jogos_popup).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Atualizar Lista", command=self.listar_jogos).pack(side='left', padx=5)

        columns = ("id", "nome", "genero", "max_jogadores", "dependencia_lingua", "complexidade", "link_bgg")
        self.tree_jogos = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            self.tree_jogos.heading(col, text=col.capitalize())
            self.tree_jogos.column(col, width=110 if col!="link_bgg" else 200)
        self.tree_jogos.pack(expand=True, fill='both', padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_jogos.yview)
        self.tree_jogos.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def listar_jogos(self, filtros=None):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        query = "SELECT id, nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg FROM Jogos"
        params = []
        if filtros:
            where_clauses = []
            if filtros.get('nome'):
                where_clauses.append("nome LIKE ?")
                params.append(f"%{filtros['nome']}%")
            if filtros.get('genero'):
                where_clauses.append("genero LIKE ?")
                params.append(f"%{filtros['genero']}%")
            if filtros.get('max_jogadores'):
                where_clauses.append("max_jogadores >= ?")
                params.append(filtros['max_jogadores'])
            if filtros.get('dependencia_lingua'):
                where_clauses.append("dependencia_lingua = ?")
                params.append(filtros['dependencia_lingua'])
            if filtros.get('complexidade_max'):
                where_clauses.append("complexidade <= ?")
                params.append(filtros['complexidade_max'])
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()

        self.tree_jogos.delete(*self.tree_jogos.get_children())
        for row in rows:
            self.tree_jogos.insert("", "end", values=row)

    def adicionar_jogo_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Adicionar Jogo")
        popup.geometry("400x350")
        popup.resizable(False, False)

        labels = ["Nome", "Gênero", "Número máximo de jogadores", "Dependência de língua (S/N)", "Complexidade (1-5)", "Link BGG"]
        entries = []

        for i, label in enumerate(labels):
            ttk.Label(popup, text=label).pack(pady=3)
            ent = ttk.Entry(popup, width=40)
            ent.pack()
            entries.append(ent)

        def salvar():
            try:
                nome = entries[0].get().strip()
                genero = entries[1].get().strip()
                max_jog = int(entries[2].get().strip())
                dep_lingua = entries[3].get().strip().upper()
                if dep_lingua not in ('S', 'N'):
                    raise ValueError("Dependência de língua deve ser 'S' ou 'N'")
                complexidade = float(entries[4].get().strip())
                if not (1 <= complexidade <= 5):
                    raise ValueError("Complexidade deve estar entre 1 e 5")
                link = entries[5].get().strip()

                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('''
                    INSERT INTO Jogos (nome, genero, max_jogadores, dependencia_lingua, complexidade, link_bgg)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (nome, genero, max_jog, dep_lingua, complexidade, link))
                conn.commit()
                conn.close()
                popup.destroy()
                self.listar_jogos()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(popup, text="Salvar", command=salvar).pack(pady=10)
        ttk.Button(popup, text="Cancelar", command=popup.destroy).pack()

    def editar_jogo_popup(self):
        selected = self.tree_jogos.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um jogo para editar.")
            return
        values = self.tree_jogos.item(selected, 'values')

        popup = tk.Toplevel(self)
        popup.title("Editar Jogo")
        popup.geometry("400x350")
        popup.resizable(False, False)

        labels = ["Nome", "Gênero", "Número máximo de jogadores", "Dependência de língua (S/N)", "Complexidade (1-5)", "Link BGG"]
        entries = []

        for i, label in enumerate(labels):
            ttk.Label(popup, text=label).pack(pady=3)
            ent = ttk.Entry(popup, width=40)
            ent.insert(0, values[i+1])
            ent.pack()
            entries.append(ent)

        def salvar():
            try:
                nome = entries[0].get().strip()
                genero = entries[1].get().strip()
                max_jog = int(entries[2].get().strip())
                dep_lingua = entries[3].get().strip().upper()
                if dep_lingua not in ('S', 'N'):
                    raise ValueError("Dependência de língua deve ser 'S' ou 'N'")
                complexidade = float(entries[4].get().strip())
                if not (1 <= complexidade <= 5):
                    raise ValueError("Complexidade deve estar entre 1 e 5")
                link = entries[5].get().strip()

                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('''
                    UPDATE Jogos SET nome=?, genero=?, max_jogadores=?, dependencia_lingua=?, complexidade=?, link_bgg=?
                    WHERE id=?
                ''', (nome, genero, max_jog, dep_lingua, complexidade, link, values[0]))
                conn.commit()
                conn.close()
                popup.destroy()
                self.listar_jogos()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(popup, text="Salvar", command=salvar).pack(pady=10)
        ttk.Button(popup, text="Cancelar", command=popup.destroy).pack()

    def eliminar_jogo(self):
        selected = self.tree_jogos.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um jogo para eliminar.")
            return
        values = self.tree_jogos.item(selected, 'values')
        res = messagebox.askyesno("Confirmar", f"Tem certeza que deseja eliminar o jogo '{values[1]}'?")
        if res:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM Jogos WHERE id=?", (values[0],))
            conn.commit()
            conn.close()
            self.listar_jogos()

    def filtrar_jogos_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Filtrar Jogos")
        popup.geometry("350x400")
        popup.resizable(False, False)

        labels = [
            "Nome contém",
            "Gênero contém",
            "Número mínimo de jogadores",
            "Dependência de língua (S/N)",
            "Complexidade máxima"
        ]
        entries = []
        for label in labels:
            ttk.Label(popup, text=label).pack(pady=3)
            ent = ttk.Entry(popup)
            ent.pack()
            entries.append(ent)

        def aplicar_filtro():
            filtros = {}
            if entries[0].get().strip():
                filtros['nome'] = entries[0].get().strip()
            if entries[1].get().strip():
                filtros['genero'] = entries[1].get().strip()
            if entries[2].get().strip():
                try:
                    filtros['max_jogadores'] = int(entries[2].get().strip())
                except:
                    messagebox.showerror("Erro", "Número máximo de jogadores inválido")
                    return
            if entries[3].get().strip().upper() in ('S', 'N'):
                filtros['dependencia_lingua'] = entries[3].get().strip().upper()
            if entries[4].get().strip():
                try:
                    filtros['complexidade_max'] = float(entries[4].get().strip())
                except:
                    messagebox.showerror("Erro", "Complexidade máxima inválida")
                    return
            self.listar_jogos(filtros)
            popup.destroy()

        ttk.Button(popup, text="Aplicar", command=aplicar_filtro).pack(pady=10)
        ttk.Button(popup, text="Cancelar", command=popup.destroy).pack()

    ### --- Jogadores Tab ---
    def setup_tab_jogadores(self):
        frame = self.tab_jogadores

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(btn_frame, text="Adicionar Jogador", command=self.adicionar_jogador_popup).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Editar Jogador", command=self.editar_jogador_popup).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Eliminar Jogador", command=self.eliminar_jogador).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Atualizar Lista", command=self.listar_jogadores).pack(side='left', padx=5)

        columns = ("id", "nome", "vitorias")
        self.tree_jogadores = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            self.tree_jogadores.heading(col, text=col.capitalize())
            self.tree_jogadores.column(col, width=200 if col=="nome" else 100)
        self.tree_jogadores.pack(expand=True, fill='both', padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_jogadores.yview)
        self.tree_jogadores.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def listar_jogadores(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, nome, vitorias FROM Jogadores")
        rows = c.fetchall()
        conn.close()

        self.tree_jogadores.delete(*self.tree_jogadores.get_children())
        for row in rows:
            self.tree_jogadores.insert("", "end", values=row)

    def adicionar_jogador_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Adicionar Jogador")
        popup.geometry("300x150")
        popup.resizable(False, False)

        ttk.Label(popup, text="Nome do jogador").pack(pady=10)
        nome_entry = ttk.Entry(popup, width=40)
        nome_entry.pack()

        def salvar():
            nome = nome_entry.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Nome não pode estar vazio")
                return
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO Jogadores (nome, vitorias) VALUES (?, 0)", (nome,))
            conn.commit()
            conn.close()
            popup.destroy()
            self.listar_jogadores()

        ttk.Button(popup, text="Salvar", command=salvar).pack(pady=10)
        ttk.Button(popup, text="Cancelar", command=popup.destroy).pack()

    def editar_jogador_popup(self):
        selected = self.tree_jogadores.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um jogador para editar.")
            return
        values = self.tree_jogadores.item(selected, 'values')

        popup = tk.Toplevel(self)
        popup.title("Editar Jogador")
        popup.geometry("300x180")
        popup.resizable(False, False)

        ttk.Label(popup, text="Nome do jogador").pack(pady=5)
        nome_entry = ttk.Entry(popup, width=40)
        nome_entry.insert(0, values[1])
        nome_entry.pack()

        ttk.Label(popup, text="Número de vitórias").pack(pady=5)
        vitorias_entry = ttk.Entry(popup, width=40)
        vitorias_entry.insert(0, str(values[2]))
        vitorias_entry.pack()

        def salvar():
            nome = nome_entry.get().strip()
            try:
                vitorias = int(vitorias_entry.get().strip())
                if vitorias < 0:
                    raise ValueError
            except:
                messagebox.showerror("Erro", "Vitórias deve ser um inteiro não negativo")
                return
            if not nome:
                messagebox.showerror("Erro", "Nome não pode estar vazio")
                return
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("UPDATE Jogadores SET nome=?, vitorias=? WHERE id=?", (nome, vitorias, values[0]))
            conn.commit()
            conn.close()
            popup.destroy()
            self.listar_jogadores()

        ttk.Button(popup, text="Salvar", command=salvar).pack(pady=10)
        ttk.Button(popup, text="Cancelar", command=popup.destroy).pack()

    def eliminar_jogador(self):
        selected = self.tree_jogadores.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um jogador para eliminar.")
            return
        values = self.tree_jogadores.item(selected, 'values')
        res = messagebox.askyesno("Confirmar", f"Tem certeza que deseja eliminar o jogador '{values[1]}'?")
        if res:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM Jogadores WHERE id=?", (values[0],))
            conn.commit()
            conn.close()
            self.listar_jogadores()

    ### --- Partidas Tab ---
    def setup_tab_partidas(self):
        frame = self.tab_partidas

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(btn_frame, text="Registar Partida", command=self.registar_partida_popup).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Editar Partida", command=self.editar_partida_popup).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Eliminar Partida", command=self.eliminar_partida).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Atualizar Lista", command=self.listar_partidas).pack(side='left', padx=5)

        columns = ("id", "jogo", "data", "jogadores", "vencedor")
        self.tree_partidas = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            self.tree_partidas.heading(col, text=col.capitalize())
            self.tree_partidas.column(col, width=150 if col!="id" else 50)
        self.tree_partidas.pack(expand=True, fill='both', padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_partidas.yview)
        self.tree_partidas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def listar_partidas(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        query = '''
            SELECT p.id, j.nome, p.data, p.jogadores,
                (SELECT nome FROM Jogadores WHERE id = p.vencedor_id) 
            FROM Partidas p
            JOIN Jogos j ON p.id_jogo = j.id
        '''
        c.execute(query)
        rows = c.fetchall()
        conn.close()

        self.tree_partidas.delete(*self.tree_partidas.get_children())
        for row in rows:
            vencedor = row[4] if row[4] else ""
            self.tree_partidas.insert("", "end", values=(row[0], row[1], row[2], row[3], vencedor))

    def registar_partida_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Registar Partida")
        popup.geometry("400x450")
        popup.resizable(False, False)

        ttk.Label(popup, text="Jogo").pack(pady=3)
        jogos = self.get_jogos()
        jogo_var = tk.StringVar()
        jogo_combo = ttk.Combobox(popup, textvariable=jogo_var, values=[f"{j[0]}: {j[1]}" for j in jogos], state='readonly')
        jogo_combo.pack()

        ttk.Label(popup, text="Data (YYYY-MM-DD)").pack(pady=3)
        data_entry = ttk.Entry(popup)
        data_entry.pack()

        ttk.Label(popup, text="Jogadores (IDs separados por vírgula)").pack(pady=3)
        jogadores_entry = ttk.Entry(popup)
        jogadores_entry.pack()

        ttk.Label(popup, text="Vencedor (ID)").pack(pady=3)
        vencedor_entry = ttk.Entry(popup)
        vencedor_entry.pack()

        def salvar():
            try:
                if not jogo_var.get():
                    raise ValueError("Selecione um jogo")
                id_jogo = int(jogo_var.get().split(":")[0])
                data = data_entry.get().strip()
                jogadores_str = jogadores_entry.get().strip()
                vencedor_str = vencedor_entry.get().strip()
                if not jogadores_str:
                    raise ValueError("Informe os IDs dos jogadores")
                jogadores = ",".join([j.strip() for j in jogadores_str.split(",")])
                vencedor_id = int(vencedor_str) if vencedor_str else None

                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('''
                    INSERT INTO Partidas (id_jogo, data, jogadores, vencedor_id) VALUES (?, ?, ?, ?)
                ''', (id_jogo, data, jogadores, vencedor_id))
                conn.commit()
                conn.close()
                popup.destroy()
                self.listar_partidas()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(popup, text="Salvar", command=salvar).pack(pady=10)
        ttk.Button(popup, text="Cancelar", command=popup.destroy).pack()

    def editar_partida_popup(self):
        selected = self.tree_partidas.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma partida para editar.")
            return
        values = self.tree_partidas.item(selected, 'values')

        popup = tk.Toplevel(self)
        popup.title("Editar Partida")
        popup.geometry("400x450")
        popup.resizable(False, False)

        ttk.Label(popup, text="Jogo").pack(pady=3)
        jogos = self.get_jogos()
        jogo_var = tk.StringVar()
        jogo_combo = ttk.Combobox(popup, textvariable=jogo_var, values=[f"{j[0]}: {j[1]}" for j in jogos], state='readonly')
        for j in jogos:
            if j[1] == values[1]:
                jogo_var.set(f"{j[0]}: {j[1]}")
                break
        jogo_combo.pack()

        ttk.Label(popup, text="Data (YYYY-MM-DD)").pack(pady=3)
        data_entry = ttk.Entry(popup)
        data_entry.insert(0, values[2])
        data_entry.pack()

        ttk.Label(popup, text="Jogadores (IDs separados por vírgula)").pack(pady=3)
        jogadores_entry = ttk.Entry(popup)
        jogadores_entry.insert(0, values[3])
        jogadores_entry.pack()

        ttk.Label(popup, text="Vencedor (ID)").pack(pady=3)
        vencedor_id = self.get_id_jogador_por_nome(values[4])
        vencedor_entry = ttk.Entry(popup)
        vencedor_entry.insert(0, str(vencedor_id) if vencedor_id else "")
        vencedor_entry.pack()

        def salvar():
            try:
                if not jogo_var.get():
                    raise ValueError("Selecione um jogo")
                id_jogo = int(jogo_var.get().split(":")[0])
                data = data_entry.get().strip()
                jogadores_str = jogadores_entry.get().strip()
                vencedor_str = vencedor_entry.get().strip()
                if not jogadores_str:
                    raise ValueError("Informe os IDs dos jogadores")
                jogadores = ",".join([j.strip() for j in jogadores_str.split(",")])
                vencedor_id_val = int(vencedor_str) if vencedor_str else None

                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('''
                    UPDATE Partidas SET id_jogo=?, data=?, jogadores=?, vencedor_id=?
                    WHERE id=?
                ''', (id_jogo, data, jogadores, vencedor_id_val, values[0]))
                conn.commit()
                conn.close()
                popup.destroy()
                self.listar_partidas()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(popup, text="Salvar", command=salvar).pack(pady=10)
        ttk.Button(popup, text="Cancelar", command=popup.destroy).pack()

    def eliminar_partida(self):
        selected = self.tree_partidas.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma partida para eliminar.")
            return
        values = self.tree_partidas.item(selected, 'values')
        res = messagebox.askyesno("Confirmar", f"Tem certeza que deseja eliminar a partida ID {values[0]}?")
        if res:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM Partidas WHERE id=?", (values[0],))
            conn.commit()
            conn.close()
            self.listar_partidas()

    ### --- Utilitários ---
    def get_jogos(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, nome FROM Jogos")
        jogos = c.fetchall()
        conn.close()
        return jogos

    def get_id_jogador_por_nome(self, nome):
        if not nome:
            return None
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id FROM Jogadores WHERE nome = ?", (nome,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    def carregar_todos(self):
        self.listar_jogos()
        self.listar_jogadores()
        self.listar_partidas()

if __name__ == "__main__":
    app = BibliotecaJogosApp()
    app.mainloop()
