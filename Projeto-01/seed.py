from sqlmodel import Session, select, delete
from database import engine, create_db_and_tables
from models import (
    Usuario, Fibra, Galeria, Post, Comentario, 
    FavoritoFibra, FavoritoPost
)
from datetime import datetime

def limpar_banco(session: Session):
    """
    Remove todos os dados das tabelas para permitir resetar o banco
    """
    print("Iniciando limpeza do banco de dados...")
    session.exec(delete(Comentario))
    session.exec(delete(FavoritoFibra))
    session.exec(delete(FavoritoPost))
    session.exec(delete(Galeria))
    session.exec(delete(Post))
    session.exec(delete(Fibra))
    session.exec(delete(Usuario))
    session.commit()
    print("Banco limpo com sucesso.")

def popular_banco():
    # Criar arquivo db e tabelas
    create_db_and_tables()
    
    with Session(engine) as session:
        limpar_banco(session)

        # USUÁRIOS
        print("Criando usuários...")
        admin = Usuario(
            nome="Gabriela Victor",
            username="gabi_admin",
            email="gabi@exemplo.com",
            senha="123", 
            bio="Estudante de Ciência da Computação e Desenvolvedora do The Science of Fashion."
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)

        # FIBRAS
        print("Populando catálogo de fibras...")
        dados_fibras = [
            {
                "nome": "Algodão",
                "categoria": "Natural",
                "origem": "Vegetal",
                "detalhes_tecnicos": "Fibra de celulose pura. Sob microscopia, apresenta convoluções (torções) características.",
                "uso_performance": "Excelente absorção de umidade e respirabilidade. Baixa elasticidade.",
                "sustentabilidade": "Renovável e biodegradável, mas com alto consumo hídrico.",
                "foto_microscopio_url": "/static/imagens/fibras/algodao/microscopio.jpg"
            },
            {
                "nome": "Poliéster",
                "categoria": "Sintética",
                "origem": "Polímero",
                "detalhes_tecnicos": "Polímero de cadeia longa. Filamentos lisos e uniformes, altamente resistentes.",
                "uso_performance": "Alta durabilidade, resistência a rugas e secagem rápida.",
                "sustentabilidade": "Derivado de petróleo. Desafio na reciclagem e liberação de microplásticos.",
                "foto_microscopio_url": "/static/imagens/fibras/poliester/microscopio.jpg"
            }
        ]

        fibras_criadas = {}
        for item in dados_fibras:
            fibra = Fibra(**item)
            session.add(fibra)
            session.commit()
            session.refresh(fibra)
            fibras_criadas[fibra.nome] = fibra

        # GALERIA (Fotos extras de cada fibra)
        print("Adicionando imagens à galeria...")
        fotos = [
            Galeria(url="/static/imagens/fibras/algodao/etiqueta.jpg", legenda="Instruções de lavagem: Algodão", fibra_id=fibras_criadas["Algodão"].id),
            Galeria(url="/static/imagens/fibras/algodao/jeans.jpg", legenda="Denim 100% Algodão", fibra_id=fibras_criadas["Algodão"].id),
            Galeria(url="/static/imagens/fibras/poliester/esportivo.jpg", legenda="Tecido dry-fit esportivo", fibra_id=fibras_criadas["Poliéster"].id)
        ]
        for foto in fotos:
            session.add(foto)

        # BLOG POSTS
        print("Criando posts do blog...")
        dados_posts = [
            {
                "titulo": "A Ciência por trás das Fibras Naturais",
                "conteudo": "Exploramos como a estrutura molecular da celulose define o conforto do algodão...",
                "foto_url": "/static/imagens/blog/post1.jpg"
            },
            {
                "titulo": "Sustentabilidade e o Futuro da Moda",
                "conteudo": "Analisamos o ciclo de vida das fibras têxteis e os novos biopolímeros...",
                "foto_url": "/static/imagens/blog/post2.jpg"
            }
        ]

        posts_criados = []
        for item in dados_posts:
            post = Post(**item)
            session.add(post)
            session.commit()
            session.refresh(post)
            posts_criados.append(post)

        # INTERAÇÕES (Comentários e Favoritos)
        print("Gerando interações iniciais...")
        
        # Comentário de teste
        comentario = Comentario(
            conteudo="Excelente post! A explicação técnica sobre polímeros ajudou muito.",
            usuario_id=admin.id,
            post_id=posts_criados[0].id
        )
        session.add(comentario)

        # Favoritos de teste
        fav_fibra = FavoritoFibra(usuario_id=admin.id, fibra_id=fibras_criadas["Algodão"].id)
        fav_post = FavoritoPost(usuario_id=admin.id, post_id=posts_criados[1].id)
        
        session.add(fav_fibra)
        session.add(fav_post)

        session.commit()
        print("\n FINALIZADO: Banco de dados pronto para o The Science of Fashion! ")

if __name__ == "__main__":
    popular_banco()