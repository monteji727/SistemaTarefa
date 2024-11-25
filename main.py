import mysql.connector
import datetime

config = {
    'host':"LOCALHOST",
    'user':"root",
    'password':"0000",
    'database':"sistemaTarefa"
}


class Tarefa:
    def __init__(self, index, id_usuario, categoria, prioridade, descricao, data_prazo, data_cricao, estado):
        self.id = index
        self.id_usuario = id_usuario
        self.categoria = categoria
        self.prioridade = prioridade
        self.descricao = descricao
        self.data_prazo = data_prazo
        self.data_criacao = data_cricao
        self.estado=estado

    def mudar_prioridade(self, novaPrioridade):
        self.prioridade = novaPrioridade

    def mudar_estado(self, novoEstado):
        self.estado = novoEstado

    def mudar_categoria(self, novaCategoria):
        self.categoria = novaCategoria

    def mudar_data_prazo(self, novaDataPrazo):
        self.data_prazo = novaDataPrazo


class Usuario:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome


class Banco:

    def __init__(self):
        self.conn = mysql.connector.connect(config)
        self.cursor = self.conn.cursor()

    def adicionar_tarefa(self, tarefa: Tarefa):
        insertTarefa = (
            "INSERT INTO tarefa "
            "("
                "id_usuario,"
                "categoria,"
                "prioridade,"
                "estado,"
                "descricao,"
                "data_prazo,"
                "data_cricao"
            ") "
            "VALUES "
            "("
                "%(id_usuario)d,"
                "%(categoria)s,"
                "%(prioridade)s,"
                "%(estado)s,"
                "%(descricao)s,"
                "%(data_prazo)s,"
                "%(data_criacao)s"
            ");"
        )

        tarefaInformacao = {
            'id_usuario': tarefa.id_usuario,
            'categoria': tarefa.categoria,
            'prioridade': tarefa.prioridade,
            'estado': tarefa.estado,
            'descricao': tarefa.descricao,
            'data_prazo': tarefa.data_prazo,
            'data_criacao': tarefa.data_criacao
        }

        self.cursor.execute(insertTarefa, tarefaInformacao)

    def adicionar_usuario(self, usuario: Usuario, senha: str):
        insertUsuario = "INSERT INTO usuario (nome, senha) VALUES (%(nome)s, %(senha)s)"

        informacaoUsuario = {
            'nome': usuario.nome,
            'senha': senha
        }
        self.cursor.execute(insertUsuario, informacaoUsuario)

    def validar_usuario(self, usuario, senha):
        selectUserMatching = "SELECT * FROM usuario WHERE nome=%s AND senha=%s"

    def close_conection(self):
        self.conn.close()
        self.cursor.close()

    def open_conection(self):
        self.conn = mysql.connector.connect(config)
        self.cursor = self.conn.cursor()


db = Banco()

db.close_conection()
