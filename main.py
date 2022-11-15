import psycopg2 as db

from sql_config import sql as sqlInit

errorString = "Error:"
successString = "Cadastrado com sucesso..."

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
            sql = "INSERT INTO usuario (nome, cpf, senha, rua, bairro, numero, complemento) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.execute(sql, args)
            self.commit()
            return successString
        except Exception as e:
            print("Inserir Usuário", errorString, e)
            raise e

    def insertTel(self, *args):
        try:
            sql = "INSERT INTO telefone (num_tel, cpf_usuario) VALUES (%s, %s)"
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Inserir Telefone", errorString, e)

    def insertTipo(self, tipo, *args):
        try:
            if tipo == "Cliente":
                sql = "INSERT INTO cliente (cartao, cpf_usuario) VALUES (%s, %s)"
                self.execute(sql, args)
                self.commit()
            else:
                sql = "INSERT INTO funcionario (cargo, cpf_usuario) VALUES (%s, %s)"
                self.execute(sql, args)
                self.commit()
        except Exception as e:
            print("Inserir Telefone", errorString, e)

    def delete(self, cpf):
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

    def update(self, cpf, *args):
        try:
            sql = f"UPDATE usuario SET nome = %s WHERE cpf = {cpf}"
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
            sql = "SELECT * FROM usuario U, funcionario F WHERE U.cpf = %s AND U.senha = %s AND U.cpf = F.cpf_usuario"
            data = self.query(sql, args)
            if data:
                return {'login': True, 'data': data}
            return {'login': False, 'data': 'Usuário não encontrado'}
        except Exception as e:
            print("Login Usuário", errorString, e)


# Classe Filme
class Filme(Connection):
    # @params nome, dublagem, legenda, duracao, direcao, genero
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
                direcao VARCHAR(30),
                genero VARCHAR(40)
              )"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Criar Filme", errorString, e)

    def insert(self, *args):
        try:
            sql = """INSERT INTO filme (nome, dublagem, legenda, duracao, direcao, genero) 
            VALUES (%s, %s, %s, %s, %s, %s)"""
            self.execute(sql, args)
            self.commit()
            return successString
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
            sql = """UPDATE filme SET nome = %s, dublagem = %s, legenda = %s, duracao = %s, direcao = %s, genero = %s WHERE cod_filme = %s"""
            self.execute(sql, args + (cod_filme,))
            self.commit()
            return f"Dados Atualizados do Filme: {cod_filme}"
        except Exception as e:
            print("Atualizar Filme", errorString, e)

    def search(self, *args, type_s="nome"):
        try:
            sql = "SELECT * FROM filme WHERE nome LIKE '%s'"
            if type_s == "genero":
                sql = "SELECT * FROM filme WHERE genero LIKE '%s'"
            data = self.query(sql, args)
            if data:
                return data
            return "Filme não encontrado"
        except Exception as e:
            print("Pesquisar Filme", errorString, e)

    def find_all(self):
        try:
            sql = "SELECT * FROM filme"
            data = self.query(sql)
            lines = ""
            if data:
                for line in data:
                    lines += "Cod: {0[0]} | Título: {0[1]} | Dublagem: {0[2]} | Legenda: {0[3]} | Duração: {0[4]} | Direção: {0[5]} | Gênero: {0[6]}".format(line)
                return lines 
            return "Filme não encontrado"
        except Exception as e:
            print("Filmes cadastrados", errorString, e)

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
                    valor_meia DOUBLE PRECISION DEFAULT (valor / 2)
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
            return successString
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
            sql = "UPDATE venda_ingresso SET valor = %s, horario = %s, sala = %s WHERE cod_venda = %s"
            self.execute(sql, args + (cod_venda,))
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

    def find_all(self):
        try:
            sql = "SELECT * FROM venda_ingresso"
            data = self.query(sql)
            lines = ""
            if data:
                for line in data:
                    valorInteriaFormatado = "R${:,.2f}".format(line[1]).replace(",", "X").replace(".", ",").replace("X", ".")
                    valorMeiaFormatado = "R${:,.2f}".format(line[1]).replace(",", "X").replace(".", ",").replace("X", ".")
                    lines += "Cod: {0[0]} | Valor Inteira: {1} | Valor Meia: {2} | Horário: {0[3]} | Sala: {0[4]}".format(line, valorInteriaFormatado, valorMeiaFormatado)
                return lines 
            return "Vendas não encontradas"
        except Exception as e:
            print("Vendas cadastrados", errorString, e)

# Classe de Sala


class Sala(Connection):
    # @params cod_sala, capacidade_max, categoria_sala
    def __init__(self):
        Connection.__init__(self)

    def create(self, *args):
        # categoria é um tipo personalizado, trata-se de um enum(lista) com os valores: standard, imax e deluxe
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
            return successString
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
            sql = "UPDATE sala SET cod_sala = %s, capacidade_max = %s, categoria_sala = %s WHERE cod_sala = %s"
            self.execute(sql, args + (cod_sala,))
            self.commit()
            return f"Dados Atualizados da Sala: {cod_sala}"
        except Exception as e:
            print("Atualizar Sala", errorString, e)

    def find_all(self):
        try:
            sql = "SELECT * FROM sala"
            data = self.query(sql)
            lines = ""
            if data:
                for line in data:
                    lines += "Cod: {0[0]} | Capacidade Máxima: {0[1]} | Categoria: {0[2]}".format(line)
                return lines 
            return "Salas não encontradas"
        except Exception as e:
            print("Salas cadastradas", errorString, e)

    def search(self, *args):
        try:
            sql = "SELECT * FROM sala WHERE cod_sala = %s"
            data = self.query(sql, args)
            if data:
                return data
            return "Sala não encontrada"
        except Exception as e:
            print("Pesquisar Sala", errorString, e)


class Sessao(Connection):
    # @params cod_sala, capacidade_max, categoria_sala
    def __init__(self):
        Connection.__init__(self)

    def create(self, *args):
        # categoria é um tipo personalizado, trata-se de um enum(lista) com os valores: standard, imax e deluxe
        try:
            sql = """CREATE TABLE IF NOT EXISTS sessao(
                cod_sessao SMALLSERIAL PRIMARY KEY,
                num_sala int,
                hr_sessao TIME,
                dt_sessao DATE,
                faixa_etaria int,
                FOREIGN KEY(num_sala) REFERENCES sala(cod_sala)
            );"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Criar Sessao", errorString, e)

    def insert(self, *args):
        try:
            sql = "INSERT INTO sessao (num_sala, hr_sessao, dt_sessao, faixa_etaria) VALUES (%s, %s, %s, %s)"
            self.execute(sql, args)
            self.commit()
            return successString
        except Exception as e:
            print("Inserir dados da Sala", errorString, e)

    def delete(self, cod_sessao):
        try:
            sql_s = "SELECT * FROM sessao WHERE cod_sessao = '{cod_sessao}'"
            if not self.query(sql_s):
                return "Cinema não encontrada"
            sql_d = f"DELETE FROM Cinema WHERE cod_sessao = '{cod_sessao}'"
            self.execute(sql_d)
            self.commit()
            return "Sessão deletado"
        except Exception as e:
            print("Deletar Sessão", errorString, e)

    def update(self, cod_sessao, *args):
        try:
            sql = "UPDATE sessao SET num_sala = %s, hr_sessao = %s, dt_sessao = %s, faixa_etaria = %s WHERE cod_sessao = %s"
            self.execute(sql, args + (cod_sessao,))
            self.commit()
            return f"Dados Atualizados da Sessão: {cod_sessao}"
        except Exception as e:
            print("Atualizar Sessão", errorString, e)

    def search(self, *args):
        try:
            sql = "SELECT * FROM sessao WHERE cod_sessao = %s"
            data = self.query(sql, args)
            if data:
                return data
            return "Sala não encontrada"
        except Exception as e:
            print("Pesquisar Sessão", errorString, e)
    
    def find_all(self):
        try:
            sql = "SELECT * FROM sessao"
            data = self.query(sql)
            lines = ""
            if data:
                for line in data:
                    lines += "Cod: {0[0]} | N° Sala: {0[1]} | Hora: {0[2]} | Data: {0[3]} | Faixa Etária: {0[4]} | Número: {0[5]}".format(line)
                return lines
            return "Sessão não encontrado"
        except Exception as e:
            print("Pesquisar Sessão", errorString, e)

class Cinema(Connection):
    # @params cod_sala, capacidade_max, categoria_sala
    def __init__(self):
        Connection.__init__(self)

    def create(self, *args):
        # categoria é um tipo personalizado, trata-se de um enum(lista) com os valores: standard, imax e deluxe
        try:
            sql = """CREATE TABLE IF NOT EXISTS cinema(
                cod_cinema SMALLSERIAL PRIMARY KEY,
                nome VARCHAR(50),
                rua VARCHAR(40),
                complemento VARCHAR(40),
                numero int
            );"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Criar Cinema", errorString, e)

    def insert(self, *args):
        try:
            sql = "INSERT INTO cinema (nome, rua, complemento, numero) VALUES (%s, %s, %s, %s)"
            self.execute(sql, args)
            self.commit()
            return successString
        except Exception as e:
            print("Inserir dados da Cinema", errorString, e)

    def delete(self, cod_cinema):
        try:
            sql_s = f"SELECT * FROM cinema WHERE cod_cinema = '{cod_cinema}'"
            if not self.query(sql_s):
                return "Cinema não encontrada"
            sql_d = f"DELETE FROM Cinema WHERE cod_cinema = '{cod_cinema}'"
            self.execute(sql_d)
            self.commit()
            return "Cinema deletado"
        except Exception as e:
            print("Deletar cinema", errorString, e)

    def update(self, cod_cinema, *args):
        try:
            sql = "UPDATE cinema SET nome = %s, rua = %s, complemento = %s, numero = %s WHERE cod_cinema = %s"
            self.execute(sql, args + (cod_cinema,))
            self.commit()
            return f"Dados Atualizados do cinema: {cod_cinema}"
        except Exception as e:
            print("Atualizar cinema", errorString, e)

    def search(self, *args):
        try:
            sql = "SELECT * FROM cinema WHERE cod_cinema = %s"
            data = self.query(sql, args)
            if data:
                return data
            return "Cinema não encontrado"
        except Exception as e:
            print("Pesquisar cinema", errorString, e)

    def find_all(self):
        try:
            sql = "SELECT * FROM cinema"
            data = self.query(sql)
            lines = ""
            if data:
                for line in data:
                    lines += "Cod: {0[0]} | Nome: {0[1]} | Rua: {0[2]} | Bairro: {0[3]} | Complemento: {0[4]} | Número: {0[5]}".format(line)
                return lines
            return "Cinema não encontrado"
        except Exception as e:
            print("Pesquisar Cinema", errorString, e)

class CinemaPassaFilme(Connection):
    # @params cod_sala, capacidade_max, categoria_sala
    def __init__(self):
        Connection.__init__(self)

    def create(self, *args):
        # categoria é um tipo personalizado, trata-se de um enum(lista) com os valores: standard, imax e deluxe
        try:
            sql = """CREATE TABLE IF NOT EXISTS cinema_passa_filme(
                id_cinema int,
                id_filme int,
                id_sessao int,
                FOREIGN KEY(id_cinema) REFERENCES cinema(cod_cinema),
                FOREIGN KEY(id_filme) REFERENCES filme(cod_filme),
                FOREIGN KEY(id_sessao) REFERENCES sessao(cod_sessao)
            );"""
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Criar Cinema Passa Filme", errorString, e)

    def insert(self, *args):
        try:
            sql = "INSERT INTO cinema_passa_filme (id_cinema, id_filme, id_sessao) VALUES (%s, %s, %s)"
            self.execute(sql, args)
            self.commit()
            return successString
        except Exception as e:
            print("Inserir dados da CinemaPassaFilme", errorString, e)

    def delete(self, id_cinema_passa_filme):
        try:
            sql_s = f"SELECT * FROM cinema WHERE id_cinema_passa_filme = '{id_cinema_passa_filme}'"
            if not self.query(sql_s):
                return "Cinema não encontrada"
            sql_d = f"DELETE FROM Cinema WHERE id_cinema_passa_filme = '{id_cinema_passa_filme}'"
            self.execute(sql_d)
            self.commit()
            return "Cinema deletado"
        except Exception as e:
            print("Deletar cinema", errorString, e)

    def update(self, id_cinema_passa_filme, *args):
        try:
            sql = "UPDATE cinema_passa_filme SET id_cinema = %s, id_filme = %s, id_sessao = %s WHERE id_cinema_passa_filme = %s"
            self.execute(sql, args + (id_cinema_passa_filme,))
            self.commit()
            return f"Dados Atualizados do cinema: {id_cinema_passa_filme}"
        except Exception as e:
            print("Atualizar cinema", errorString, e)

    def search(self, *args):
        try:
            sql = "SELECT * FROM cinema_passa_filme WHERE cod_cinema = %s"
            data = self.query(sql, args)
            if data:
                return data
            return "Cinema passa filme não encontrado"
        except Exception as e:
            print("Pesquisar Cinema passa filme", errorString, e)

    def find_all(self):
        try:
            sql = "SELECT * FROM cinema_passa_filme"
            data = self.query(sql)
            lines = ""
            if data:
                for line in data:
                    lines += "Cod: {0[0]} | Id_Cinema: {0[1]} | Id_Filme: {0[2]} | Id_Sessao: {0[3]}".format(line)
                return lines
            return "Cinema passa filme não encontrado"
        except Exception as e:
            print("Pesquisar Cinema passa filme", errorString, e)


if __name__ == "__main__":
    initCon = Connection()
    initCon.execute(sqlInit)
    initCon.commit()

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
                               "Digite o Número da sua Residência:", "Digite o Complemento:", "Digite seu Número de Telefone:", "Selecione o tipo de usuário:"]
                txtCadastroLength = len(txtCadastro)
                user = Usuario()
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
                        complemento = input(txtCadastro[x])
                    if x == 7:
                        qtd_tel = input("Quantos telefones deseja cadastrar?")
                        for v in range(int(qtd_tel)):
                            tel_numero = input(txtCadastro[x])
                    if x == 8:
                        print("1 - Cliente\n2 - Funcionário")
                        tipoOp = input(txtCadastro[x])
                        tipo_usuario = objTipoUsuario.get(
                            int(tipoOp), 'Cliente')
                        if tipo_usuario == 'Cliente':
                            cartao = input("Insira o seu cartão de crédito:")
                            print(user.insert(nome, cpf, senha, rua, bairro,
                                              int(numero), complemento))
                            print(user.insertTipo(tipo_usuario, cpf, cartao))
                            for v in range(int(qtd_tel)):
                                print(user.insertTel(tel_numero, cpf))
                            break
                        else:
                            cargo = input("Insira o seu cargo:")
                            print(user.insert(nome, cpf, senha, rua, bairro,
                                              int(numero), complemento))
                            print(user.insertTipo(tipo_usuario, cpf, cargo))
                            for v in range(int(qtd_tel)):
                                print(user.insertTel(tel_numero, cpf))
                            break

                    x += 1
            # Login
            if int(userOp) == 2:
                txtLogin = ['Insira o CPF:', 'Insira a sua senha:']
                cpf = input(txtLogin[0])
                password = input(txtLogin[1])
                user = Usuario()
                loginResponse = user.login(cpf, password)
                if loginResponse.get('login'):
                    isLogged = True
                    cpf = loginResponse.get('data')[0][0]
                    nome = loginResponse.get('data')[0][1]

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
                print("""\n1 - Cadastrar Filme\n2 - Editar Filme\n3 - Deletar Filme\n4 - Cadastrar Ingresso\n5 - Editar Ingresso\n6 - Deletar Ingresso\n7 - Cadastrar Sala\n8 - Editar Sala\n9 - Deletar Sala\n10 - Cadastrar Cinema\n11 - Editar Cinema\n12 - Deletar Cinema\n13 - Cadastrar Sessão\n14 - Editar Sessão\n15 - Deletar Sessão\n16 - Cadastrar Filme em um Cinema\n17 - Editar Filme em um Cinema\n18 - Deletar Filme em um Cinema\n0 - Voltar para o menu inicial""")
                userOpLogged = input("Escolha uma opção: ")

                # Cadastro de Filme
                if int(userOpLogged) == 1:
                    x = int(0)
                    txtFilme = ["Digite o nome do filme:", "Digite a dublagem:",
                                "Digite a legenda:", "Digite a duração (hh:mm:ss):", "Digite a direção:", "Digite o gênero:"]
                    txtFilmeLength = len(txtFilme)
                    movie = Filme()
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
                            genero = input(txtFilme[x])
                            print(movie.insert(nome, dublagem,
                                  legenda, duracao, direcao, genero))
                            break
                        x += 1

                # Editar Filme
                if int(userOpLogged) == 2:
                    movie = Filme()
                    print(movie.find_all())
                    x = int(0)
                    txtFilme = ["Digite o ID do filme:", "Digite o nome do filme:", "Digite a dublagem:",
                                "Digite a legenda:", "Digite a duração (hh:mm:ss):", "Digite a direção:", "Digite o gênero:"]
                    txtFilmeLength = len(txtFilme)
                    while x < txtFilmeLength and movie.find_all() != "Filme não encontrado":
                        if x == 0:
                            cod_filme = input(txtFilme[x])
                        if x == 1:
                            nome = input(txtFilme[x])
                        if x == 2:
                            dublagem = input(txtFilme[x])
                        if x == 3:
                            legenda = input(txtFilme[x])
                        if x == 4:
                            print(txtFilme[x])
                            h = input("Horas (hh): ")
                            m = input("Minutos (mm): ")
                            s = input("Segundos (ss): ")
                            duracao = f'{int(h):02d}:{int(m):02d}:{int(s):02d}'
                        if x == 5:
                            direcao = input(txtFilme[x])
                        if x == 6:
                            genero = input(txtFilme[x])
                            print(movie.update(int(cod_filme), nome, dublagem,
                                  legenda, duracao, direcao, genero))
                            break
                        x += 1
                
                #Deletar Filme
                if int(userOpLogged) == 3:
                    movie = Filme()
                    print(movie.find_all())
                    cod_filme = input("Insira o Código do Filme")
                    print(movie.delete(int(cod_filme)))

                #Cadastrar Ingresso
                if int(userOpLogged) == 4:
                    # @params valor, horario, sala
                    x = int(0)
                    txtVenda = ["Digite o valor do ingresso:",
                                "Digite o horário que a Sala estará aberta:", "Digite o numero da sala:"]
                    txtVendaLength = len(txtVenda)
                    venda = VendaIngresso()
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
                
                #Editar Ingresso
                if int(userOpLogged) == 5:
                    # @params valor, horario, sala
                    venda = VendaIngresso()
                    print(venda.find_all())
                    x = int(0)
                    txtVenda = ["Digite o Código do Ingresso","Digite o valor do ingresso:",
                                "Digite o horário que a Sala estará aberta:", "Digite o numero da sala:"]
                    txtVendaLength = len(txtVenda)
                    while x < txtVendaLength:
                        if x == 0:
                            cod_venda = input(txtVenda[x])
                        if x == 1:
                            valor = input(txtVenda[x])
                            # Formatação útil para a exibição posteriormente
                            # valorFormatado = "R${:,.2f}".format(float(valor)).replace(",", "X").replace(".", ",").replace("X", ".")
                        if x == 2:
                            print(txtVenda[x])
                            h = input("Horas (hh): ")
                            m = input("Minutos (mm): ")
                            s = input("Segundos (ss): ")
                            horario = f'{int(h):02d}:{int(m):02d}:{int(s):02d}'
                        if x == 3:
                            sala = input(txtVenda[x])
                            print(venda.update(int(cod_venda), float(valor), horario, int(sala)))
                            break

                        x += 1

                #Deletar Ingresso  
                if int(userOpLogged) == 6:
                    # @params valor, horario, sala
                    venda = VendaIngresso()
                    print(venda.find_all())
                    cod_filme = input("Insira o Código do Ingresso")
                    print(venda.delete(int(cod_filme)))

                # Cadastro de Sala
                if int(userOpLogged) == 7:
                    x = int(0)
                    objCategorias = {1: 'imax', 2: 'standard', 3: 'deluxe'}
                    txtSala = ["Digite o código da sala:",
                               "Digite a capacidade máxima:", "Digite a categoria da sala:"]
                    txtSalaLength = len(txtSala)
                    sala = Sala()
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
                
                # Editar de Sala
                if int(userOpLogged) == 8:
                    sala = Sala()
                    print(sala.find_all())
                    x = int(0)
                    objCategorias = {1: 'imax', 2: 'standard', 3: 'deluxe'}
                    txtSala = ["Digite o código da sala:",
                               "Digite a capacidade máxima:", "Digite a categoria da sala:"]
                    txtSalaLength = len(txtSala)
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
                            print(sala.update(int(cod_sala), int(
                                capacidade_max), categoria))
                            break

                        x += 1

                #Deletar Sala  
                if int(userOpLogged) == 9:
                    sala = Sala()
                    print(sala.find_all())
                    cod_sala = input("Insira o Código da Sala:")
                    print(sala.delete(int(cod_sala)))
                
                # Cadastro Cinema
                if int(userOpLogged) == 10:
                    x = int(0)
                    txtCinema = ["Digite o nome do cinema:", "Digite a rua:",
                                "Digite o bairro:", "Digite complemento:", "Digite o número:"]
                    txtCinemaLength = len(txtCinema)
                    cinema = Cinema()
                    while x < txtCinemaLength:
                        if x == 0:
                            nome = input(txtCinema[x])
                        if x == 1:
                            rua = input(txtCinema[x])
                        if x == 2:
                            bairro = input(txtCinema[x])
                        if x == 3:
                            complemento = input(txtCinema[x])
                        if x == 4:
                            numero = input(txtCinema[x])
                            print(cinema.insert(nome, rua,
                                  bairro, complemento, int(numero)))
                            break
                        x += 1

                # Editar Cinema
                if int(userOpLogged) == 11:
                    x = int(0)
                    cinema = Cinema()
                    print(cinema.find_all());
                    txtCinema = ["Digite o Código do Cinema:", "Digite o nome do cinema:", "Digite a rua:",
                                "Digite o bairro:", "Digite complemento:", "Digite o número:"]
                    txtCinemaLength = len(txtCinema)
                    while x < txtCinemaLength:
                        if x == 0:
                            nome = input(txtCinema[x])
                        if x == 1:
                            rua = input(txtCinema[x])
                        if x == 2:
                            bairro = input(txtCinema[x])
                        if x == 3:
                            complemento = input(txtCinema[x])
                        if x == 4:
                            numero = input(txtCinema[x])
                            print(cinema.insert(nome, rua,
                                  bairro, complemento, int(numero)))
                            break
                        x += 1

                # Deletar Cinema
                if int(userOpLogged) == 12:
                    cinema = Cinema()
                    print(cinema.find_all())
                    cod_cinema = input("Insira o Código da Sala:")
                    print(cinema.delete(int(cod_cinema)))

                # Cadastrar Sessao
                if int(userOpLogged) == 13:
                    x = int(0)
                    sessao = Sessao()
                    txtSessao = ["Digite o número da sala:", "Digite a hora sessão:",
                                "Digite a data da sessão:", "Digite a faixa etaria:"]
                    txtSessaoLength = len(txtSessao)
                    while x < txtSessaoLength:
                        if x == 0:
                            num_sala = input(txtSessao[x])
                        if x == 1:
                            print(txtSessao[x])
                            h = input("Horas (hh): ")
                            m = input("Minutos (mm): ")
                            s = input("Segundos (ss): ")
                            hr_sessao = f'{int(h):02d}:{int(m):02d}:{int(s):02d}'
                        if x == 2:
                            print(txtSessao[x])
                            d = input("Dia (dd): ")
                            m = input("Mês (mm): ")
                            y = input("Ano (yyyy): ")
                            dt_sessao = f'{int(y):04d}-{int(m):02d}-{int(d):02d}'
                        if x == 3:
                            faixa_etaria = input(txtSessao[x])
                            print(sessao.insert(nome, hr_sessao,
                                  dt_sessao, faixa_etaria))
                            print(cinema_passa_filme.insert(int(id_cinema), id_filme,
                                  id_sessao))
                            break
                        x += 1


                # Editar Sessao
                if int(userOpLogged) == 14:
                    x = int(0)
                    sessao = Sessao()
                    print(sessao.find_all())
                    txtSessao = ["Digite o código da sessão:", "Digite o número da sala:", "Digite a hora sessão:",
                                "Digite a data da sessão:", "Digite a faixa etaria:"]
                    txtSessaoLength = len(txtSessao)
                    while x < txtSessaoLength:
                        if x == 0:
                            cod_sessao = input(txtSessao[x])
                        if x == 1:
                            num_sala = input(txtSessao[x])
                        if x == 2:
                            print(txtSessao[x])
                            h = input("Horas (hh): ")
                            m = input("Minutos (mm): ")
                            s = input("Segundos (ss): ")
                            hr_sessao = f'{int(h):02d}:{int(m):02d}:{int(s):02d}'
                        if x == 3:
                            print(txtSessao[x])
                            d = input("Dia (dd): ")
                            m = input("Mês (mm): ")
                            y = input("Ano (yyyy): ")
                            dt_sessao = f'{int(y):04d}-{int(m):02d}-{int(d):02d}'
                        if x == 4:
                            faixa_etaria = input(txtSessao[x])
                            print(sessao.update(int(cod_sessao), nome, hr_sessao,
                                  dt_sessao, faixa_etaria))
                            break
                        x += 1
                # Deletar Sessao
                if int(userOpLogged) == 15:
                    sessao = Sessao()
                    print(sessao.find_all())
                    cod_sessao = input("Insira o Código da Sessão:")
                    print(sessao.delete(int(cod_sessao)))

                # Cadastrar Cinema Passa Filme
                if int(userOpLogged) == 16:
                    x = int(0)
                    sessao = Sessao()
                    cinema = Cinema()
                    filme = Filme()
                    cinema_passa_filme = CinemaPassaFilme()
                    txtCPF = ["Digite o id do cinema:", "Digite o id da sessão:",
                                "Digite o id do filme:"]
                    txtCPFLength = len(txtCPF)
                    while x < txtCPFLength:
                        if x == 0:
                            print(cinema.find_all())
                            id_cinema = input(txtCPF[x])
                        if x == 1:
                            print(sessao.find_all())
                            id_sessao = input(txtCPF[x])
                        if x == 2:
                            print(filme.find_all())
                            id_filme = input(txtCPF[x])
                            print(cinema_passa_filme.insert(int(id_cinema), int(id_filme),
                                  int(id_sessao)))
                            break
                        x += 1

                # Editar Cinema Passa Filme
                if int(userOpLogged) == 17:
                    x = int(0)
                    sessao = Sessao()
                    cinema = Cinema()
                    filme = Filme()
                    cinema_passa_filme = CinemaPassaFilme()
                    txtCPF = ["Digite o id do Item que deseja editar:","Digite o id do cinema:", "Digite o id da sessão:",
                                "Digite o id do filme:"]
                    txtCPFLength = len(txtCPF)
                    while x < txtCPFLength:
                        if x == 0:
                            print(cinema_passa_filme.find_all())
                            id_item = input(txtCPF[x])
                        if x == 1:
                            print(cinema.find_all())
                            id_cinema = input(txtCPF[x])
                        if x == 2:
                            print(sessao.find_all())
                            id_sessao = input(txtCPF[x])
                        if x == 3:
                            print(filme.find_all())
                            id_filme = input(txtCPF[x])
                            print(cinema_passa_filme.update(int(id_item), int(id_cinema), int(id_filme),
                                  int(id_sessao)))
                            break
                        x += 1

                # Deletar Cinema Passa Filme
                if int(userOpLogged) == 18:
                    cinema_passa_filme = CinemaPassaFilme()
                    print(cinema_passa_filme.find_all())
                    id_item = input("Insira o id que deseja deletar:")
                    print(sessao.delete(int(id_item)))
                # Sair
                if int(userOpLogged) == 0:
                    print("Encerrando...")
                    isLogged = False
                    break
