import mysql.connector
import datetime

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

    def adicionar_tarefa(self, tarefa):
        insertTarefa =(
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

        tarefaInformacao= {
            'id_usuario' = tarefa.id_usuario,
            'categoria' = tarefa.categoria,
            'prioridade' = tarefa.prioridade,
            'estado' = tarefa.estado,
            'descricao' = tarefa.descricao,
            'data_prazo' = tarefa.data_prazo,
            'data_criacao' = tarefa.data_criacao
        }


    def adicionar_usuario(self, usuario, senha):

        insertUsuario="INSERT INTO usuario (nome, senha) VALUES (%(nome)s, %(senha)s)"

        informacaoUsuario={
            'nome':usuario.nome,
            'senha':senha
        }
        self.cursor.execute(insertUsuario,informacaoUsuario)

    def validar_usuario(self, usuario, senha):
        selectUserMatching="SELECT * FROM usuario WHERE nome=%s AND senha=%s"

    def close_conection(self):
        self.conn.close()
        self.cursor.close()

    def open_conection(self):
        self.conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        self.cursor=self.conn.cursor()


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


db=Banco()

db.close_conection()