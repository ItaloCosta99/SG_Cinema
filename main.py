import string
from unicodedata import category
from unittest import result
from xml.dom.minidom import Identified
import psycopg2 as db

errorString = "Error:"

# Classe de configurações
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

# Classe de Conexão com o banco
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

# Classe Usuario
class Usuario(Connection):
    # @params nome, cpf, senha, rua, bairro, numero, tel_numero, tipo_usuario
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
            return "Usuário Cadastrado com Sucesso..."
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

    def login(self, *args):
        try:
            sql = "SELECT * FROM usuario WHERE nome = %s AND senha = %s"
            data = self.query(sql, args)
            if data:
                return {'login': True, 'data': data}
            return {'login': False, 'data': 'Usuário não encontrado'}
        except Exception as e:
            print("Login Usuário", errorString, e)

# Classe Filme
class Filme(Connection):
    # @params nome, dublagem, legenda, duracao, direcao
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
                direcao VARCHAR(30)
              )"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Criar Filme", errorString, e)

    def insert(self, *args):
        try:
            sql = """INSERT INTO filme (nome, dublagem, legenda, duracao, direcao) 
            VALUES (%s, %s, %s, %s, %s)"""
            self.execute(sql, args)
            self.commit()
            return "Cadastrado com sucesso..."
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

# Classe Venda de Ingresso
class VendaIngresso(Connection):
    # @params valor, horario, sala
    def __init__(self):
        Connection.__init__(self)

    def create(self, *args):
        try:
            sql = """CREATE TABLE IF NOT EXISTS venda_ingresso(
                    cod_venda SMALLSERIAL PRIMARY KEY,
                    valor DOUBLE PRECISION CHECK (valor >= 10.0) DEFAULT 10.0,
                    horario TIME,
                    sala int
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
            return "Cadastrado com sucesso..."
        except Exception as e:
            print("Inserir Venda de Ingresso", errorString, e)

    def delete(self, cod_venda: int):
        try:
            sql_s = f"SELECT * FROM venda_ingresso WHERE cod_venda = '{cod_venda}'"
            if not self.query(sql_s):
                return "Venda não encontrada"
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
            return "Venda não encontrada"
        except Exception as e:
            print("Atualizar Usuário", errorString, e)

# Classe de Sala
class Sala(Connection):
    # @params cod_sala, capacidade_max, categoria_sala
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
            return "Cadastrado com sucesso..."
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
    isLogged = False
    whileInit = int(1)
    while whileInit != 0:
        if isLogged == False:
            print("--- Menu ---")
            print("1 - Cadastrar Usuario\n2 - Login Usuário\n0 - Sair")
            userOp = input("Escolha uma opção: ")
            # Cadastro de Usuário
            if int(userOp) == 1:
                x = int(0)
                objTipoUsuario = {1: 'Cliente', 2: 'Funcionario'}
                txtCadastro = ["Digite seu nome:", "Digite seu CPF:", "Digite sua Senha:", "Digite sua Rua:", "Digite seu Bairro:",
                               "Digite o Número da sua Residência:", "Digite seu Número de Telefone:", "Digite o Tipo do Usuário('Cliente' ou 'Funcionário'):"]
                txtCadastroLength = len(txtCadastro)
                user = Usuario()
                user.create()
                while x < txtCadastroLength:
                    if x == 0:
                        nome = input(txtCadastro[x])
                    if x == 1:
                        cpf = input(txtCadastro[x])
                    if x == 2:
                        senha = input(txtCadastro[x])
                    if x == 3:
                        rua = input(txtCadastro[x])
                    if x == 4:
                        bairro = input(txtCadastro[x])
                    if x == 5:
                        numero = input(txtCadastro[x])
                    if x == 6:
                        tel_numero = input(txtCadastro[x])
                    if x == 7:
                        print("1 - Cliente\n2 - Funcionário")
                        tipoOp = input(txtCadastro[x])
                        tipo_usuario = objTipoUsuario.get(
                            int(tipoOp), 'Cliente')
                    if x == 8:
                        print(user.insert(nome, int(cpf), senha, rua, bairro,
                                          int(numero), int(tel_numero), tipo_usuario))
                        break

                    x += 1
            # Login
            if int(userOp) == 2:
                txtLogin = ['Insira o Username:', 'Insira a sua senha:']
                username = input(txtLogin[0])
                password = input(txtLogin[1])
                user = Usuario()
                loginResponse = user.login(username, password)
                if loginResponse.get('login'):
                    isLogged = True
                    nome = loginResponse.get('data')[0][0]
                    cpf = loginResponse.get('data')[0][1]

                    print("\nLogado com Sucesso")
                    print(f"Usuário: {nome}\nCpf: {cpf}")
                else:
                    print(loginResponse.get('data'))

            if int(userOp) == 0:
                print("Encerrando...")
                break

        else:
            userOpLogged = int(1)

            while userOpLogged != 0:
                print(
                    "1 - Cadastrar Filme:\n2 - Cadastrar Ingresso:\n3 - Cadastrar Sala:\n0 - Voltar para o menu inicial")
                userOpLogged = input("Escolha uma opção: ")

                # Cadastro de Filme
                if int(userOpLogged) == 1:
                    x = int(0)
                    txtFilme = ["Digite o nome do filme:", "Digite a dublagem:",
                                "Digite a legenda:", "Digite a duração (hh:mm:ss):", "Digite a direção:"]
                    txtFilmeLength = len(txtFilme)
                    movie = Filme()
                    movie.create()
                    while x < txtFilmeLength:
                        if x == 0:
                            nome = input(txtFilme[x])
                        if x == 1:
                            dublagem = input(txtFilme[x])
                        if x == 2:
                            legenda = input(txtFilme[x])
                        if x == 3:
                            print(txtFilme[x])
                            h = input("Horas (hh): ")
                            m = input("Minutos (mm): ")
                            s = input("Segundos (ss): ")
                            duracao = f'{int(h):02d}:{int(m):02d}:{int(s):02d}'
                        if x == 4:
                            direcao = input(txtFilme[x])
                        if x == 5:
                            print(movie.insert(nome, dublagem,
                                  legenda, duracao, direcao))
                            break

                        x += 1
                # Cadastro de Venda de Ingresso
                if int(userOpLogged) == 2:
                    # @params valor, horario, sala
                    x = int(0)
                    txtVenda = ["Digite o valor do ingresso:",
                                "Digite o horário que a Sala estará aberta:", "Digite o numero da sala:"]
                    txtVendaLength = len(txtVenda)
                    venda = VendaIngresso()
                    venda.create()
                    while x < txtVendaLength:
                        if x == 0:
                            valor = input(txtVenda[x])
                            # Formatação útil para a exibição posteriormente
                            # valorFormatado = "R${:,.2f}".format(float(valor)).replace(",", "X").replace(".", ",").replace("X", ".")
                        if x == 1:
                            print(txtVenda[x])
                            h = input("Horas (hh): ")
                            m = input("Minutos (mm): ")
                            s = input("Segundos (ss): ")
                            horario = f'{int(h):02d}:{int(m):02d}:{int(s):02d}'
                        if x == 2:
                            sala = input(txtVenda[x])
                            print(venda.insert(float(valor), horario, int(sala)))
                            break

                        x += 1
                # Cadastro de Sala
                if int(userOpLogged) == 3:
                    x = int(0)
                    objCategorias = {1: 'imax', 2: 'standard', 3: 'deluxe'}
                    txtSala = ["Digite o código da sala:",
                               "Digite a capacidade máxima:", "Digite a categoria da sala:"]
                    txtSalaLength = len(txtSala)
                    sala = Sala()
                    sala.create()
                    while x < txtSalaLength:
                        if x == 0:
                            cod_sala = input(txtSala[x])
                        if x == 1:
                            capacidade_max = input(txtSala[x])
                        if x == 2:
                            print("Categorias:\n1 - Imax\n2 - Standard\n3 - Deluxe")
                            categoryOp = input(txtSala[x])
                            categoria = objCategorias.get(
                                int(categoryOp), 'standard')
                            print(sala.insert(int(cod_sala), int(
                                capacidade_max), categoria))
                            break

                        x += 1
                if int(userOpLogged) == 0:
                    print("Encerrando...")
                    isLogged = False
                    break
