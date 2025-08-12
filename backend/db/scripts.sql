
CREATE TABLE Pesquisa (
	id_pesquisa serial4 NOT NULL,
	nome_pesquisa varchar(30) NULL,
	resultado varchar(60) NULL,
	fonte varchar(15) NULL,
	url_resultado varchar(200) NULL,
	CONSTRAINT pesquisa_pkey PRIMARY KEY (id_pesquisa)
);

CREATE TABLE Tipo_plano (
	id_tipo_plano serial4 NOT NULL,
	nome_tipo_plano varchar(40) NULL,
	preco numeric(10, 2) NULL,
	duracao_dias int4 NULL,
	CONSTRAINT tipo_plano_pkey PRIMARY KEY (id_tipo_plano)
);

CREATE TABLE Usuario (
	id_usuario serial4 NOT NULL,
	id_role int4 NULL,
	tipo bpchar(1) NULL,
	rg varchar(10) NULL,
	email varchar(100) NULL,
	telefone varchar(20) NULL,
	celular varchar(20) NULL,
	cep varchar(8) NULL,
	n int4 NULL,
	complemento varchar(20) NULL,
	razao_social varchar(60) NULL,
	cnpj varchar(14) NULL,
	nome_usuario varchar(60) NULL,
	cpf varchar(11) NULL,
	CONSTRAINT usuario_cnpj_key UNIQUE (cnpj),
	CONSTRAINT usuario_cpf_key UNIQUE (cpf),
	CONSTRAINT usuario_email_key UNIQUE (email),
	CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario),
	CONSTRAINT usuario_tipo_check CHECK ((tipo = ANY (ARRAY['F'::bpchar, 'J'::bpchar]))),
	CONSTRAINT usuario_id_role_fkey FOREIGN KEY (id_role) REFERENCES Role(id_role)
);

CREATE TABLE Estado (
    id_estado INTEGER PRIMARY KEY,
    nome_estado VARCHAR(45),
    sigla_estado VARCHAR(2)
);

CREATE TABLE Conta (
	id_conta serial4 NOT NULL,
	id_usuario int4 NULL,
	data_criacao date NULL,
	login varchar(30) NULL,
	senha varchar(60) NOT NULL,
	CONSTRAINT conta_login_key UNIQUE (login),
	CONSTRAINT conta_pkey PRIMARY KEY (id_conta),
	CONSTRAINT conta_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Plano (
	id_plano serial4 NOT NULL,
	id_tipo_plano int4 NULL,
	id_conta int4 NULL,
	data_inicio_plano date NULL,
	data_fim_plano date NULL,
	ativa boolean,
	CONSTRAINT plano_pkey PRIMARY KEY (id_plano),
	CONSTRAINT plano_id_conta_fkey FOREIGN KEY (id_conta) REFERENCES Conta(id_conta),
	CONSTRAINT plano_id_tipo_plano_fkey FOREIGN KEY (id_tipo_plano) REFERENCES Tipo_plano(id_tipo_plano)
);

INSERT INTO Estado (id_estado, nome_estado, sigla_estado) VALUES
(1, 'Acre', 'AC'),
(2, 'Alagoas', 'AL'),
(3, 'Amapá', 'AP'),
(4, 'Amazonas', 'AM'),
(5, 'Bahia', 'BA'),
(6, 'Ceará', 'CE'),
(7, 'Distrito Federal', 'DF'),
(8, 'Espírito Santo', 'ES'),
(9, 'Goiás', 'GO'),
(10, 'Maranhão', 'MA'),
(11, 'Mato Grosso', 'MT'),
(12, 'Mato Grosso do Sul', 'MS'),
(13, 'Minas Gerais', 'MG'),
(14, 'Pará', 'PA'),
(15, 'Paraíba', 'PB'),
(16, 'Paraná', 'PR'),
(17, 'Pernambuco', 'PE'),
(18, 'Piauí', 'PI'),
(19, 'Rio de Janeiro', 'RJ'),
(20, 'Rio Grande do Norte', 'RN'),
(21, 'Rio Grande do Sul', 'RS'),
(22, 'Rondônia', 'RO'),
(23, 'Roraima', 'RR'),
(24, 'Santa Catarina', 'SC'),
(25, 'São Paulo', 'SP'),
(26, 'Sergipe', 'SE'),
(27, 'Tocantins', 'TO');

insert into tipo_plano (id_tipo_plano, nome_tipo_plano, preco, duracao_dias) values 
(1, 'Redot Test', 2500, 30),
(2, 'Redot', 2500, 365),
(3, 'Redot Note', 2500, 365)