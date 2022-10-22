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
            print("Config", errorString, e)
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
                  name varchar(100),
                  cpf varchar(11),
                  password varchar(20) UNIQUE,
                  street varchar(80),
                  district varchar(40),
                  number int,
                  tel_number int,
                  user_type varchar(40),
                  PRIMARY KEY(cpf)
                )"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Create", errorString, e)

    def insert(self, *args):
        try:
            sql = "INSERT INTO usuario (name, cpf, ) VALUES (%s, %s)"
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Insert", errorString, e)


if __name__ == "__main__":
    usuario = Usuario()
    usuario.create()
    usuario.insert(
        "Italo", '12345678912')

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
