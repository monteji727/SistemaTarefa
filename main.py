import mysql.connector

HOST="LOCALHOST"
USER="root"
PASSWORD="0000"
DATABASE="SISTEMATAREFA"

class Banco:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        self.cursor= self.conn.cursor()

    def adicionarTarefa(self):

    def adicionarUsuario(self):

    def validarUsuario(self, usuario, senha):



class Tarefa:
    def __init__(self, id, id_usuario, categoria, prioridade, descricao, data_prazo, data_cricao):
        self.id = id
        self.id_usuario = id_usuario
        self.categoria= categoria
        self.prioridade= prioridade
        self.descricao= descricao
        self.data_prazo= data_prazo
        self.data_criacao= data_cricao

    def mudarPrioridade(self,novaPrioridade):
        self.prioridade=novaPrioridade

    def mudarCategoria(self, novaCategoria):
        self.categoria=novaCategoria

    def mudarDataPrazo(self, novaDataPrazo):
        self.data_prazo=novaDataPrazo

class Usuario:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
