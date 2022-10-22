import psycopg2 as db


class Config:
    def __init__(self):
        self.config = {
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
            self.conn = db.connect(**self.config["postgres"])
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Error:", e)
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

    @property
    def commit(self):
        return self.connection.commit()

    def fetchall(self):
      return self.cursor.fetchall()

    def execute(self, sql, params=None):
      self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
      self.cursor.execute(sql, params or ())
      return self.fetchall()

class Person(Connection):
  def __init__(self):
    Connection.__init__(self)
    

conexao = db.connect(
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
    print(record[0], "-->", record[1])
