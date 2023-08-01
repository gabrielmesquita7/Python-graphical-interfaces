DROP DATABASE IF EXISTS lista;
CREATE DATABASE lista;

USE lista;

CREATE TABLE usuarios (
    id INTEGER NOT NULL,
    nome_usuario VARCHAR (64) NOT NULL,
    senha CHAR (64) NOT NULL,
    nome VARCHAR (64),
    telefone VARCHAR (32),
    email VARCHAR (64),
    CONSTRAINT PRIMARY KEY (id)
);

CREATE TABLE lista_tarefas (
    id INTEGER NOT NULL,
    nome_lista VARCHAR (64),
    data_criacao DATETIME NOT NULL,
    data_modificacao DATETIME NOT NULL,
    id_usuario INTEGER NOT NULL,
    CONSTRAINT fk_usuario_lista FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
    CONSTRAINT PRIMARY KEY (id)
);

CREATE TABLE compartilha (
    id_dono INTEGER NOT NULL,
    id_convidado INTEGER NOT NULL,
    id_tarefa INTEGER NOT NULL,
    aceita BOOLEAN,
    CONSTRAINT PRIMARY KEY (id_dono, id_convidado, id_tarefa),
    CONSTRAINT fk_usuariod FOREIGN KEY (id_dono) REFERENCES usuarios (id),
    CONSTRAINT fk_usuarioc FOREIGN KEY (id_convidado) REFERENCES usuarios (id),
    CONSTRAINT fk_lista FOREIGN KEY (id_tarefa) REFERENCES lista_tarefas (id)
);

CREATE TABLE tarefa (
    id INTEGER NOT NULL,
    descricao TEXT,
    data_criacao DATETIME NOT NULL,
    data_vencimento DATETIME,
    conclusao BOOLEAN,
    id_lista INTEGER NOT NULL,
    CONSTRAINT PRIMARY KEY (id),
    CONSTRAINT fk_lista_tarefa FOREIGN KEY (id_lista) REFERENCES lista_tarefas (id)
);

SHOW TABLES FROM lista;

INSERT INTO usuarios (id, nome_usuario, senha, nome, telefone, email) VALUES
(1, 'joao123', 'senha123', 'João Silva', '123456789', 'joao@example.com'),
(2, 'maria456', 'abc123', 'Maria Santos', '987654321', 'maria@example.com'),
(3, 'pedro789', 'senha456', 'Pedro Oliveira', '555555555', 'pedro@example.com');


INSERT INTO lista_tarefas (id, nome_lista, data_criacao, data_modificacao, id_usuario) VALUES
(1, 'Lista do João', NOW(),  NOW(), 1),
(2, 'Lista da Maria', NOW(),  NOW(), 2),
(3, 'Lista do Pedro',  NOW(),  NOW(), 3);

INSERT INTO tarefa (id, descricao, data_criacao, data_vencimento, conclusao, id_lista) VALUES
(1, 'Tarefa 1 da Lista da Maria',  NOW(),  NOW(), 0, 2),
(2, 'Tarefa 2 da Lista da Maria',  NOW(), NOW(), 0, 2),
(3, 'Tarefa 3 da Lista da Maria',  NOW(),  NOW(), 0, 2);

INSERT INTO compartilha (id_dono, id_convidado, id_tarefa, aceita) VALUES
(2, 1, 2, true),
(2, 3, 2, true);