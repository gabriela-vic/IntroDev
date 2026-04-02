CREATE TABLE Usuarios (
    usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    bio TEXT
);
CREATE TABLE Favoritos (
    usuario_id INTEGER,
    fibra_id INTEGER,
    PRIMARY KEY (usuario_id, fibra_id), 
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (fibra_id) REFERENCES Fibras(fibra_id)
);

CREATE TABLE Posts (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    foto_url TEXT,
    horario DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Comentarios (
    comentario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    post_id INTEGER, 
    conteudo TEXT NOT NULL,
    horario DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);

CREATE TABLE Fibras (
    fibra_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    foto_url TEXT,
    origem TEXT 
);


CREATE TABLE Composicoes (
    composicao_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fibra_pai_id INTEGER, 
    fibra_mistura_id INTEGER, 
    porcentagem INTEGER, 
    FOREIGN KEY (fibra_pai_id) REFERENCES Fibras(fibra_id),
    FOREIGN KEY (fibra_mistura_id) REFERENCES Fibras(fibra_id)
);
