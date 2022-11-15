sql = """CREATE TABLE IF NOT EXISTS usuario(
  cpf bigint UNIQUE,
  nome VARCHAR(100),
  senha VARCHAR(20) UNIQUE,
  rua VARCHAR(80),
  bairro VARCHAR(40),
  complemento VARCHAR(40),
  numero INT,
  PRIMARY KEY(cpf)
);

CREATE TABLE IF NOT EXISTS telefone(
  id_tel SMALLSERIAL PRIMARY KEY,
  cpf_usuario BIGINT,
  num_tel BIGINT,
  FOREIGN KEY(cpf_usuario) REFERENCES usuario(cpf)
);

CREATE TABLE IF NOT EXISTS cliente(
  id_cliente SMALLSERIAL PRIMARY KEY,
  cpf_usuario BIGINT,
  cartao varchar(20),
  FOREIGN KEY(cpf_usuario) REFERENCES usuario(cpf)
);

CREATE TABLE IF NOT EXISTS funcionario(
  id_funcionario SMALLSERIAL PRIMARY KEY,
  cpf_usuario BIGINT,
  cargo varchar(50),
  FOREIGN KEY(cpf_usuario) REFERENCES usuario(cpf)
);

CREATE TABLE IF NOT EXISTS sala(
  cod_sala INT PRIMARY KEY,
  capacidade_max INT,
  categoria_sala categoria
);

CREATE TABLE IF NOT EXISTS sessao(
  cod_sessao SMALLSERIAL PRIMARY KEY,
  num_sala int,
  hr_sessao TIME,
  dt_sessao DATE,
  faixa_etaria int,
  FOREIGN KEY(num_sala) REFERENCES sala(cod_sala)
);

CREATE TABLE IF NOT EXISTS venda_ingresso(
  cod_venda SMALLSERIAL PRIMARY KEY,
  valor DOUBLE PRECISION CHECK (valor >= 10.0) DEFAULT 10.0,
  valor_meia DOUBLE PRECISION GENERATED ALWAYS AS (valor / 2) STORED,
  horario TIME,
  sala int
);

CREATE TABLE IF NOT EXISTS filme(
  cod_filme SMALLSERIAL PRIMARY KEY,
  nome VARCHAR(50) NOT NULL,
  dublagem VARCHAR(20) DEFAULT 'Português',
  legenda VARCHAR(3) DEFAULT 'Não',
  duracao TIME,
  direcao VARCHAR(30),
  genero VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS cinema(
  cod_cinema SMALLSERIAL PRIMARY KEY,
  nome VARCHAR(50),
  rua VARCHAR(40),
  bairro VARCHAR(40),
  complemento VARCHAR(40),
  numero int
);

CREATE TABLE IF NOT EXISTS cinema_passa_filme(
  id_cinema_passa_filme SMALLSERIAL PRIMARY KEY, 
  id_cinema int,
  id_filme int,
  id_sessao int,
  FOREIGN KEY(id_cinema) REFERENCES cinema(cod_cinema),
  FOREIGN KEY(id_filme) REFERENCES filme(cod_filme),
  FOREIGN KEY(id_sessao) REFERENCES sessao(cod_sessao)
);
"""
