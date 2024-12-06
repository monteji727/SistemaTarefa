import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
import mysql.connector

# Configuração do banco de dados
config = {
    'host': "localhost",
    'user': "root",
    'password': "0000",
    'database': "sistematarefa"
}

class Banco:
    def __init__(self, configs):
        self.config = configs
        self.conn = mysql.connector.connect(**configs)
        self.cursor = self.conn.cursor()

    def validar_usuario(self, nome, senha):
        query = "SELECT id FROM usuario WHERE nome=%s AND senha=%s AND ativado IS TRUE;"
        self.cursor.execute(query, (nome, senha))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def selecionar_tarefas(self, id_usuario):
        query = "SELECT id, descricao, data_prazo, prioridade, estado FROM tarefa WHERE id_usuario=%s;"
        self.cursor.execute(query, (id_usuario,))
        return self.cursor.fetchall()

    def selecionar_tarefa(self, id_tarefa):
        query = "SELECT id, descricao, data_prazo, prioridade, estado FROM tarefa WHERE id=%s;"
        self.cursor.execute(query, (id_tarefa,))
        return self.cursor.fetchone()

    def adicionar_tarefa(self, id_usuario, descricao, data_prazo, prioridade, estado):
        query = """
        INSERT INTO tarefa (id_usuario, descricao, data_prazo, prioridade, estado, data_cricao)
        VALUES (%s, %s, %s, %s, %s, NOW());
        """
        self.cursor.execute(query, (id_usuario, descricao, data_prazo, prioridade, estado))
        self.conn.commit()

    def editar_tarefa(self, id_tarefa, descricao, data_prazo, prioridade, estado):
        query = """
        UPDATE tarefa
        SET descricao=%s, data_prazo=%s, prioridade=%s, estado=%s
        WHERE id=%s;
        """
        self.cursor.execute(query, (descricao, data_prazo, prioridade, estado, id_tarefa))
        self.conn.commit()

    def apagar_tarefa(self, id_tarefa):
        query = "DELETE FROM tarefa WHERE id=%s;"
        self.cursor.execute(query, (id_tarefa,))
        self.conn.commit()

    def cadastrar_usuario(self, nome, senha):
        query = "INSERT INTO usuario (nome, senha, ativado) VALUES (%s, %s, TRUE);"
        self.cursor.execute(query, (nome, senha))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

class Aplicacao:
    def __init__(self, root):
        self.id_tarefa = None
        self.root = root
        self.root.title("Sistema de Tarefas")
        self.banco = Banco(config)
        self.usuario_id = None
        self.tela_login()

    def tela_login(self):
        self.limpar_tela()

        tk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text="Usuário:").pack()
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.pack()

        tk.Label(self.root, text="Senha:").pack()
        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.pack()

        tk.Button(self.root, text="Entrar", command=self.fazer_login).pack(pady=10)
        tk.Button(self.root, text="Cadastrar", command=self.tela_cadastro).pack()

    def tela_cadastro(self):
        self.limpar_tela()

        tk.Label(self.root, text="Cadastro de Usuário", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Nome:").pack()
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.pack()

        tk.Label(self.root, text="Senha:").pack()
        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.pack()

        def cadastrar():
            nome = self.entry_nome.get()
            senha = self.entry_senha.get()

            if nome and senha:
                try:
                    self.banco.cadastrar_usuario(nome, senha)
                    messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                    self.tela_login()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")

        tk.Button(self.root, text="Cadastrar", command=cadastrar).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.tela_login).pack()

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        usuario_id = self.banco.validar_usuario(usuario, senha)
        if usuario_id:
            self.usuario_id = usuario_id
            self.tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def tela_principal(self):
        self.limpar_tela()

        tk.Label(self.root, text="Tarefas", font=("Arial", 18)).pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Descrição", "Prazo", "Prioridade", "Estado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Prazo", text="Prazo")
        self.tree.heading("Prioridade", text="Prioridade")
        self.tree.heading("Estado", text="Estado")
        self.tree.pack(fill="both", expand=True)

        self.carregar_tarefas()

        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Adicionar Tarefa", command=self.tela_adicionar_tarefa).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Editar Tarefa", command=self.tela_editar_tarefa).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Apagar Tarefa", command=self.apagar_tarefa).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Sair", command=self.tela_login).pack(side="left", padx=5)

    def carregar_tarefas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        tarefas = self.banco.selecionar_tarefas(self.usuario_id)
        for tarefa in tarefas:
            self.tree.insert("", "end", values=tarefa)

    def tela_adicionar_tarefa(self):
        self.tela_formulario_tarefa("Adicionar Tarefa")

    def tela_editar_tarefa(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma tarefa para editar.")
            return

        self.id_tarefa = self.tree.item(selecionado[0], "values")[0]
        self.tela_formulario_tarefa("Editar Tarefa")

    def apagar_tarefa(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma tarefa para apagar.")
            return

        id_tarefa = self.tree.item(selecionado[0], "values")[0]
        try:
            self.banco.apagar_tarefa(id_tarefa)
            messagebox.showinfo("Sucesso", "Tarefa apagada com sucesso!")
            self.carregar_tarefas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao apagar tarefa: {e}")

    def tela_formulario_tarefa(self, titulo):
        self.limpar_tela()

        tk.Label(self.root, text=titulo, font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Descrição:").pack()
        entry_descricao = tk.Entry(self.root)
        entry_descricao.pack()

        tk.Label(self.root, text="Data Prazo (YYYY-MM-DD):").pack()
        entry_prazo = tk.Entry(self.root)
        entry_prazo.pack()

        tk.Label(self.root, text="Prioridade:").pack()
        prioridades=["urgente", "importante", "média", "baixa", "irrelevante"]
        entry_prioridade = ttk.Combobox(self.root, values=prioridades)
        entry_prioridade.set(prioridades[-1])
        entry_prioridade.pack()

        tk.Label(self.root, text="Estado:").pack()
        estados=["pendente", "completa", "espera", "atribuída"]
        entry_estado = ttk.Combobox(self.root, values=estados)
        entry_estado.set(estados[-1])
        entry_estado.pack()

        if titulo == "Editar Tarefa":
            tarefa = self.banco.selecionar_tarefa(self.id_tarefa)
            entry_descricao.insert(0, tarefa[1])  # Description
            entry_estado.insert(0, tarefa[4])     # State
            entry_prioridade.insert(0, tarefa[3]) # Priority
            entry_prazo.insert(0, tarefa[2])

        def salvar():
            data_prazo = entry_prazo.get()
            descricao = entry_descricao.get()
            prioridade = entry_prioridade.get()
            estado = entry_estado.get()

            try:
                date_prazo_obj = datetime.strptime(data_prazo, "%Y-%m-%d")
                data_now = datetime.now()
                if date_prazo_obj<data_now:
                    messagebox.showerror("Erro", "Data inválida: coloque uma data posterior à atual!")
                    return

                if titulo == "Editar Tarefa":
                    self.banco.editar_tarefa(self.id_tarefa, descricao, data_prazo, prioridade, estado)
                else:
                    self.banco.adicionar_tarefa(self.usuario_id, descricao, data_prazo, prioridade, estado)
                messagebox.showinfo("Sucesso", f"{titulo} realizada com sucesso!")
                self.tela_principal()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar tarefa: {e}")

        tk.Button(self.root, text="Salvar", command=salvar).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.tela_principal).pack()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x500")
    app = Aplicacao(root)
    root.mainloop()
