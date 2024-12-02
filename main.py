import mysql.connector
import datetime

config = {
    'host': "LOCALHOST",
    'user': "root",
    'password': "0000",
    'database': "sistematarefa"
}


class Tarefa:
    def __init__(self, index, id_usuario, id_dono, categoria, prioridade, descricao, data_prazo, data_cricao, estado):
        self.id: int = index
        self.id_usuario: int = id_usuario
        self.id_dono: int = id_dono
        self.categoria: str = categoria
        self.prioridade: str = prioridade
        self.descricao: str = descricao
        self.data_prazo: datetime = data_prazo
        self.data_criacao: datetime = data_cricao
        self.estado: str = estado

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

    def mudar_nome(self, novoNome):
        self.nome = novoNome


class Banco:

    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def adicionar_tarefa(self, tarefa: Tarefa):
        insertTarefa = (
            "INSERT INTO tarefa "
            "("
            "id_usuario,"
            "id_dono, "
            "categoria,"
            "prioridade,"
            "estado,"
            "descricao,"
            "data_prazo,"
            "data_cricao"
            ") "
            "VALUES "
            "("
            "%(id_usuario)d,",
            "%(id_dono)d, "
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
            'id_dono': tarefa.id_dono,
            'categoria': tarefa.categoria,
            'prioridade': tarefa.prioridade,
            'estado': tarefa.estado,
            'descricao': tarefa.descricao,
            'data_prazo': tarefa.data_prazo,
            'data_criacao': tarefa.data_criacao
        }

        self.cursor.execute(insertTarefa, tarefaInformacao)
        self.conn.commit()

        return self.cursor.rowcount > 0

    def adicionar_usuario(self, usuario: Usuario, senha: str, tipo: str):
        selectUsuario = "SELECT ativado FROM usuario WHERE nome LIKE %(nome)s"
        informacaoUsuario = {
            'nome': usuario.nome
        }
        self.cursor.execute(selectUsuario, informacaoUsuario)
        lista = self.cursor.fetchall()
        if len(lista) > 0:
            return False, []

        insertUsuario = "INSERT INTO usuario ( nome, senha) VALUES ( %(nome)s, %(senha)s)"

        informacaoUsuario = {
            'nome': usuario.nome,
            'senha': senha,
            'tipo': tipo
        }
        self.cursor.execute(insertUsuario, informacaoUsuario)
        self.conn.commit()

        return self.cursor.rowcount > 0, [usuario.nome]

    def mudar_tarefa(self, tarefa: Tarefa):
        updateTarefa = (
            "UPDATE tarefa SET"
            " catergoria=%(categoria)s,"
            " prioridade=%(prioridade)s,"
            " estado=%(estado)s,"
            " descricao=%(descricao)s,"
            " data_prazo=%(data_prazo)s"
            " WHERE id=%(id_tarefa)d;"
        )

        informacaoTarefa = {
            'categoria': tarefa.categoria,
            'prioridade': tarefa.prioridade,
            'estado': tarefa.estado,
            'descricao': tarefa.descricao,
            'data_prazo': tarefa.data_prazo,

            'id_tarefa': tarefa.id
        }

        self.cursor.execute(updateTarefa, informacaoTarefa)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def mudar_usuario_nome(self, usuario: Usuario):
        updateUsuario = "UPDATE usuario SET nome=%(nome)s WHERE id=%(id_usuario)d;"
        usuarioInformacao = {
            'nome': usuario.nome,
            'id_usuario': usuario.id
        }
        self.cursor.execute(updateUsuario, usuarioInformacao)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def mudar_usuario_senha(self, usuario: Usuario, novasenha: str):
        updateSenha = "UPDATE usuario SET senha=%(senha)s WHERE id=%(id_usuario)d;"
        senhaInformacao = {
            'senha': novasenha,
            'id_usuario': usuario.id
        }
        self.cursor.execute(updateSenha, senhaInformacao)

        self.conn.commit()
        return self.cursor.rowcount > 0

    def validar_usuario(self, usuario: Usuario, senha: str):
        selectUserMatching = "SELECT id FROM usuario WHERE nome=%(nome)s AND senha=%(senha)s AND ativado IS TRUE;"
        informacaoUsuario = {
            'nome': usuario.nome,
            'senha': senha
        }
        self.cursor.execute(selectUserMatching, informacaoUsuario)
        return self.cursor.fetchall()

    def selecionar_tarefas(self, usuario: Usuario):
        selectTarefas = "SELECT * FROM tarefa WHERE id_usuario=%(id_usuario)d;"
        informacaoTarefa = {
            'id_usuario': usuario.id
        }

        self.cursor.execute(selectTarefas, informacaoTarefa)
        return self.cursor.fetchall()

    def close_conection(self):
        self.conn.close()
        self.cursor.close()

    def open_conection(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

user = Usuario(0, "cavalo")
senha = "1234"

db = Banco()

print(db.adicionar_usuario(user, senha, "BIXO VEIO"))

db.close_conection()
