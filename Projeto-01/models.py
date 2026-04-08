from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

# --- TABELAS DE LIGAÇÃO (MANY-TO-MANY) ---

class FavoritoFibra(SQLModel, table=True):
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id", primary_key=True)
    fibra_id: Optional[int] = Field(default=None, foreign_key="fibra.id", primary_key=True)

class FavoritoPost(SQLModel, table=True):
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id", primary_key=True)
    post_id: Optional[int] = Field(default=None, foreign_key="post.id", primary_key=True)


# --- MODELOS PRINCIPAIS ---

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    senha: str
    bio: Optional[str] = None

    # Relacionamentos
    comentarios: List["Comentario"] = Relationship(back_populates="usuario")
    fibras_favoritas: List["Fibra"] = Relationship(back_populates="usuarios_que_favoritaram", link_model=FavoritoFibra)
    posts_favoritos: List["Post"] = Relationship(back_populates="usuarios_que_favoritaram", link_model=FavoritoPost)


class Fibra(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True) 
    categoria: str  # Ex: "Natural" ou "Sintética"
    origem: str     # Ex: "Vegetal", "Animal" ou "Polímero"
    
    detalhes_tecnicos: str
    uso_performance: str
    sustentabilidade: str
    
    foto_microscopio_url: str 
    fibras_relacionadas: Optional[str] = Field(default=None)

    # Relacionamentos
    fotos: List["Galeria"] = Relationship(back_populates="fibra")
    usuarios_que_favoritaram: List[Usuario] = Relationship(back_populates="fibras_favoritas", link_model=FavoritoFibra)


class Galeria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(nullable=False)
    legenda: Optional[str] = None
    fibra_id: int = Field(default=None, foreign_key="fibra.id")
    
    fibra: Optional[Fibra] = Relationship(back_populates="fotos")


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    conteudo: str
    foto_url: Optional[str] = None
    data_publicacao: datetime = Field(default_factory=datetime.now)

    # Relacionamentos
    comentarios: List["Comentario"] = Relationship(back_populates="post")
    usuarios_que_favoritaram: List[Usuario] = Relationship(back_populates="posts_favoritos", link_model=FavoritoPost)


class Comentario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conteudo: str
    data_postagem: datetime = Field(default_factory=datetime.now)
    
    usuario_id: int = Field(foreign_key="usuario.id")
    post_id: int = Field(foreign_key="post.id")

    usuario: Usuario = Relationship(back_populates="comentarios")
    post: Post = Relationship(back_populates="comentarios")