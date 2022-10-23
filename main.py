import string
from unittest import result
from xml.dom.minidom import Identified
import psycopg2 as db

errorString = "Error:"


class Config:
    def __init__(self):
        self.configs = {
            "postgres": {
                "user": "postgres",
                "password": "postgres",
                "host": "localhost",
                "port": "5432",
                "database": "teste",
            }
        }


class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        try:
            self.conn = db.connect(**self.configs["postgres"])
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Connection Config", errorString, e)
            exit(1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        return self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()


class Usuario(Connection):
    def __init__(self):
        Connection.__init__(self)

    def create(self, *args):
        try:
            sql = """CREATE TABLE IF NOT EXISTS usuario(
                  nome VARCHAR(100),
                  cpf VARCHAR(11),
                  senha VARCHAR(20) UNIQUE,
                  rua VARCHAR(80),
                  bairro VARCHAR(40),
                  numero INT,
                  tel_numero BIGINT,
                  tipo_usuario VARCHAR(40),
                  PRIMARY KEY(cpf)
                )"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Criar Usuário", errorString, e)

    def insert(self, *args):
        try:
            sql = "INSERT INTO usuario (nome, cpf, senha, rua, bairro, numero, tel_numero, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Inserir Usuário", errorString, e)

    def delete(self, cpf: string):
        try:
            sql_s = f"SELECT * FROM usuario WHERE cpf = '{cpf}'"
            if not self.query(sql_s):
                return "Usuário não encontrado"
            sql_d = f"DELETE FROM usuario WHERE cpf = '{cpf}'"
            self.execute(sql_d)
            self.commit()
            return "Usuário deletado"
        except Exception as e:
            print("Deletar Usuário", errorString, e)

    def update(self, cpf: string, *args):
        try:
            sql = f"UPDATE usuario SET nome = %s WHERE cpf = '{cpf}'"
            self.execute(sql, args)
            self.commit()
            return f"Dados Atualizados do Usuario do CPF: {cpf}"
        except Exception as e:
            print("Atualizar Usuario", errorString, e)

    def search(self, *args, type_s="nome"):
        try:
            sql = "SELECT * FROM usuario WHERE nome LIKE %s"
            if type_s == "cpf":
                sql = "SELECT * FROM usuario WHERE cpf = %s"
            data = self.query(sql, args)
            if data:
                return data
            return "Usuário não encontrado"
        except Exception as e:
            print("Atualizar Usuário", errorString, e)


class Filme(Connection):
    def __init__(self):
        Connection.__init__(self)

    def create(self, *args):
        try:
            sql = """CREATE TABLE IF NOT EXISTS filme(
                cod_filme SMALLSERIAL PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                dublagem VARCHAR(20) DEFAULT 'Português',
                legenda VARCHAR(3) DEFAULT 'Não',
                duracao TIME,
                direcao varchar(30)
              )"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Criar Filme", errorString, e)

    def insert(self, *args):
        try:
            sql = """INSERT INTO filme (name, dublagem, legenda, duracao, direcao) 
            VALUES (%s, %s, %s, %s, %s)"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Inserir Filme", errorString, e)

    def delete(self, cod_filme: int):
        try:
            sql_s = f"SELECT * FROM filme WHERE cod_filme = '{cod_filme}'"
            if not self.query(sql_s):
                return "Filme não encontrado"
            sql_d = f"DELETE FROM filme WHERE cod_filme = '{cod_filme}'"
            self.execute(sql_d)
            self.commit()
            return "Filme deletado"
        except Exception as e:
            print("Deletar Filme", errorString, e)

    def update(self, cod_filme: int, *args):
        try:
            sql = f"UPDATE filme SET nome = %s WHERE cod_filme = '{cod_filme}'"
            self.execute(sql, args)
            self.commit()
            return f"Dados Atualizados do Filme: {cod_filme}"
        except Exception as e:
            print("Atualizar Filme", errorString, e)

    def search(self, *args, type_s="nome"):
        try:
            sql = "SELECT * FROM filme WHERE nome LIKE %s"
            if type_s == "dublagem":
                sql = "SELECT * FROM filme WHERE dublagem = %s"
            data = self.query(sql, args)
            if data:
                return data
            return "Filme não encontrado"
        except Exception as e:
            print("Pesquisar Filme", errorString, e)


class VendaIngresso(Connection):
    def __init__(self):
        Connection.__init__(self)

    def create(self, *args):
        try:
            sql = """CREATE TABLE IF NOT EXISTS venda_ingresso(
                    cod_venda SMALLSERIAL PRIMARY KEY,
                    valor DOUBLE PRECISION CHECK (valor >= 10.0) DEFAULT 10.0,
                    horario TIME,
                    sala int,
                  )"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Criar Venda de Ingresso", errorString, e)

    def insert(self, *args):
        try:
            sql = """INSERT INTO venda_ingresso (valor, horario, sala) VALUES (%s, %s, %s)"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Inserir Venda de Ingresso", errorString, e)

    def delete(self, cod_venda: int):
        try:
            sql_s = f"SELECT * FROM venda_ingresso WHERE cod_venda = '{cod_venda}'"
            if not self.query(sql_s):
                return "Usuário não encontrado"
            sql_d = f"DELETE FROM venda_ingresso WHERE cod_venda = '{cod_venda}'"
            self.execute(sql_d)
            self.commit()
            return "Venda de Ingresso deletada"
        except Exception as e:
            print("Deletar Venda de Ingresso", errorString, e)

    def update(self, cod_venda: int, *args):
        try:
            sql = f"UPDATE venda_ingresso SET valor = %s WHERE cod_venda = '{cod_venda}'"
            self.execute(sql, args)
            self.commit()
            return f"Dados Atualizados da Venda de Ingresso: {cod_venda}"
        except Exception as e:
            print("Pesquisar Venda de Ingresso", errorString, e)

    def search(self, *args):
        try:
            sql = "SELECT * FROM venda_ingresso WHERE sala = %s"
            data = self.query(sql, args)
            if data:
                return data
            return "Usuário não encontrado"
        except Exception as e:
            print("Atualizar Usuário", errorString, e)


class Sala(Connection):
    def __init__(self):
        Connection.__init__(self)

    def create(self, *args):
        try:
            sql = """CREATE TABLE IF NOT EXISTS sala(
              cod_sala INT PRIMARY KEY,
              capacidade_max INT,
              categoria_sala categoria
            )"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Criar Sala", errorString, e)

    def insert(self, *args):
        try:
            sql = "INSERT INTO sala (cod_sala, capacidade_max, categoria_sala) VALUES (%s, %s, %s)"
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Inserir dados da Sala", errorString, e)

    def delete(self, cod_sala: int):
        try:
            sql_s = f"SELECT * FROM sala WHERE cod_sala = '{cod_sala}'"
            if not self.query(sql_s):
                return "Sala não encontrada"
            sql_d = f"DELETE FROM sala WHERE cod_sala = '{cod_sala}'"
            self.execute(sql_d)
            self.commit()
            return "Sala deletada"
        except Exception as e:
            print("Deletar Sala", errorString, e)

    def update(self, cod_sala: int, *args):
        try:
            sql = f"UPDATE sala SET capacidade_max = %s WHERE cod_sala = '{cod_sala}'"
            self.execute(sql, args)
            self.commit()
            return f"Dados Atualizados da Sala: {cod_sala}"
        except Exception as e:
            print("Atualizar Sala", errorString, e)

    def search(self, *args):
        try:
            sql = "SELECT * FROM sala WHERE cod_sala = %s"
            data = self.query(sql, args)
            if data:
                return data
            return "Sala não encontrada"
        except Exception as e:
            print("Pesquisar Sala", errorString, e)


if __name__ == "__main__":
    """ usuario = Usuario()
    usuario.insert(
        'Italo', '12345678912', 'senha', 'Rua Tal', 'Centro', 0, 99999999999, 'cliente') """
    sala = Sala()
    print(sala.search(1))

""" conexao = db.connect(
    host="localhost",
    database="teste",
    port=5432,
    user="postgres",
    password="postgres")
# Criando um cursor
cursor = conexao.cursor()
# Realizando a consulta na tabela do postgres
cursor.execute("SELECT * FROM aluno")
# Pega o resultset como uma tupla

result = cursor.fetchall()

# Navega pelo resultset
for record in result:
    print(record[0], "-->", record[1]) """
