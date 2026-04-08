from sqlmodel import Session, select, delete
from database import engine, create_db_and_tables
from models import (
    Usuario, Fibra, Galeria, Post, Comentario, 
    FavoritoFibra, FavoritoPost
)
from datetime import datetime

# ===== DADOS DAS FIBRAS =====

FIBRAS_NATURAIS = [
    {
        "nome": "Algodão",
        "categoria": "Natural",
        "origem": "Vegetal",
        "detalhes_tecnicos": "Fibra de celulose pura. Sob microscopia, apresenta convoluções (torções) características que conferem maciez e absorvência.",
        "uso_performance": "Excelente absorção de umidade (até 25% do peso), respirabilidade, toque macio. Baixa elasticidade e tendência a amarrotar.",
        "sustentabilidade": "Renovável e biodegradável. Cultivo convencional consome muita água (2.700L por camiseta). Versão orgânica reduz impacto.",
        "foto_microscopio_url": "/static/imagens/fibras/naturais/algodao/microscopio.jpg"
    },
    {
        "nome": "Linho",
        "categoria": "Natural",
        "origem": "Vegetal",
        "detalhes_tecnicos": "Fibra de linho obtida do caule da planta. Fibras longas com nós característicos (nodes) visíveis ao microscópio.",
        "uso_performance": "Alta resistência (2x mais que algodão), toque fresco, boa absorção, amassa facilmente, fica mais forte quando molhado.",
        "sustentabilidade": "Planta resistente que requer pouca água e pesticidas. Totalmente biodegradável.",
        "foto_microscopio_url": "/static/imagens/fibras/naturais/linho/microscopio.jpg"
    },
    {
        "nome": "Seda",
        "categoria": "Natural",
        "origem": "Animal",
        "detalhes_tecnicos": "Fibra proteica produzida pelo bicho-da-seda. Estrutura triangular que cria refração de luz (brilho característico).",
        "uso_performance": "Toque sedoso, brilho natural, boa resistência, leve, termorreguladora, hipoalergênica, sensível à luz UV.",
        "sustentabilidade": "Processo tradicional envolve fervura dos casulos (matando os bichos). Alternativas como seda Ahimsa (não violenta) existem.",
        "foto_microscopio_url": "/static/imagens/fibras/naturais/seda/microscopio.jpg"
    },
    {
        "nome": "Lã",
        "categoria": "Natural",
        "origem": "Animal",
        "detalhes_tecnicos": "Fibra proteica de ovelhas. Apresenta escamas sobrepostas que permitem feltragem e criam bolsas de ar isolantes.",
        "uso_performance": "Excelente isolamento térmico, absorve umidade (até 35% sem sensação de molhado), resistente a chamas, naturalmente anti-odor.",
        "sustentabilidade": "Renovável e biodegradável. Impacto ambiental depende das práticas de pastoreio (uso da terra, emissões de metano).",
        "foto_microscopio_url": "/static/imagens/fibras/naturais/la/microscopio.jpg"
    },
    {
        "nome": "Cânhamo",
        "categoria": "Natural",
        "origem": "Vegetal",
        "detalhes_tecnicos": "Fibra de celulose do caule da planta Cannabis sativa. Fibras longas, fortes e resistentes.",
        "uso_performance": "Muito resistente, durável, boa absorção, resistente a mofo e bactérias, toque melhora com lavagens.",
        "sustentabilidade": "Cultivo de baixo impacto: cresce rápido, pouca água, sem pesticidas, sequestra CO2, enriquece o solo.",
        "foto_microscopio_url": "/static/imagens/fibras/naturais/canhamo/microscopio.jpg"
    },
    {
        "nome": "Rami",
        "categoria": "Natural",
        "origem": "Vegetal",
        "detalhes_tecnicos": "Fibra de celulose da planta Boehmeria nivea. Uma das fibras naturais mais resistentes.",
        "uso_performance": "Alta resistência, toque sedoso, brilho natural, resistente a mofo e bactérias, boa absorção.",
        "sustentabilidade": "Cultivo perene que não esgota o solo, poucos insumos, biodegradável.",
        "foto_microscopio_url": "/static/imagens/fibras/naturais/rami/microscopio.jpg"
    },
    {
        "nome": "Cashmere",
        "categoria": "Natural",
        "origem": "Animal",
        "detalhes_tecnicos": "Fibra finíssima da cabra Cashmere. Diâmetro de 14-19 micrômetros, muito mais fino que a lã comum.",
        "uso_performance": "Extremamente macio, leve, excelente isolamento, toque luxuoso, menos resistente que lã comum.",
        "sustentabilidade": "Preocupações com overgrazing e desertificação. Certificações como Sustainable Cashmere existem.",
        "foto_microscopio_url": "/static/imagens/fibras/naturais/cashmere/microscopio.jpg"
    }
]

FIBRAS_SINTETICAS = [
    {
        "nome": "Poliéster",
        "categoria": "Sintética",
        "origem": "Polímero",
        "detalhes_tecnicos": "Polímero de cadeia longa (PET). Filamentos lisos e uniformes ao microscópio, altamente resistentes.",
        "uso_performance": "Alta durabilidade, resistência a rugas, secagem rápida, boa resistência química, pode acumular oleosidade.",
        "sustentabilidade": "Derivado de petróleo. Reciclagem mecânica e química (rPET) reduz impacto. Libera microplásticos.",
        "foto_microscopio_url": "/static/imagens/fibras/sinteticas/poliester/microscopio.jpg"
    },
    {
        "nome": "Nylon",
        "categoria": "Sintética",
        "origem": "Polímero",
        "detalhes_tecnicos": "Poliamida sintética. Fibras lisas, cilíndricas e muito uniformes ao microscópio.",
        "uso_performance": "Excelente elasticidade e recuperação, muito resistente à abrasão, leve, secagem rápida.",
        "sustentabilidade": "Derivado de petróleo, produção intensiva em energia. Reciclagem possível (ECONYL® usa resíduos oceânicos).",
        "foto_microscopio_url": "/static/imagens/fibras/sinteticas/nylon/microscopio.jpg"
    },
    {
        "nome": "Acrílico",
        "categoria": "Sintética",
        "origem": "Polímero",
        "detalhes_tecnicos": "Polímero acrílico (PAN). Fibras com superfície lisa, estrutura menos cristalina.",
        "uso_performance": "Macio, leve, aquece bem (similar à lã), resistente a mofo e traças, boa estabilidade dimensional.",
        "sustentabilidade": "Derivado de petróleo, produção energívora. Dificuldade de reciclagem. Libera microplásticos.",
        "foto_microscopio_url": "/static/imagens/fibras/sinteticas/acrilico/microscopio.jpg"
    },
    {
        "nome": "Polipropileno",
        "categoria": "Sintética",
        "origem": "Polímero",
        "detalhes_tecnicos": "Polímero termoplástico. Fibras lisas, baixa densidade (flutua na água).",
        "uso_performance": "Muito leve, hidrofóbico (não absorve umidade), boa resistência química, baixa elasticidade.",
        "sustentabilidade": "Derivado de petróleo. Reciclável mas infraestrutura limitada. Usado em roupas térmicas e geotêxteis.",
        "foto_microscopio_url": "/static/imagens/fibras/sinteticas/polipropileno/microscopio.jpg"
    },
    {
        "nome": "Elastano (Lycra/Spandex)",
        "categoria": "Sintética",
        "origem": "Polímero",
        "detalhes_tecnicos": "Poliuretano segmentado. Estrutura que permite estiramento e recuperação excepcionais.",
        "uso_performance": "Alta elasticidade (500-800%), excelente recuperação, leve, resistente a suor e loções.",
        "sustentabilidade": "Derivado de petróleo. Dificuldade de reciclagem. Pequena % em misturas. Alternativas bio-based surgindo.",
        "foto_microscopio_url": "/static/imagens/fibras/sinteticas/elastano/microscopio.jpg"
    },
    {
        "nome": "Rayon (Viscose)",
        "categoria": "Sintética",
        "origem": "Polímero",
        "detalhes_tecnicos": "Fibra semissintética de celulose regenerada. Estrutura uniforme com estrias longitudinais.",
        "uso_performance": "Toque sedoso, boa absorção, confortável, menos resistente quando molhado.",
        "sustentabilidade": "Origem renovável (madeira). Processo químico tradicional usa produtos tóxicos. Versões sustentáveis (Lyocell/Tencel) existem.",
        "foto_microscopio_url": "/static/imagens/fibras/sinteticas/rayon/microscopio.jpg"
    }
]

# ===== POSTS DO BLOG =====
POSTS = [
    {
        "titulo": "A Ciência por trás das Fibras Naturais",
        "conteudo": "Exploramos como a estrutura molecular da celulose define o conforto do algodão, a resistência do linho e o brilho da seda. Entenda a relação entre morfologia da fibra e propriedades têxteis.",
        "foto_url": "/static/imagens/blog/post1.jpg"
    },
    {
        "titulo": "Sustentabilidade e o Futuro da Moda",
        "conteudo": "Analisamos o ciclo de vida das fibras têxteis e os novos biopolímeros. Do cultivo à reciclagem, como a indústria está se transformando para um futuro mais sustentável.",
        "foto_url": "/static/imagens/blog/post2.jpg"
    },
    {
        "titulo": "Microplásticos: O desafio das fibras sintéticas",
        "conteudo": "Roupas de poliéster e nylon liberam microfibras na lavagem. Entenda o impacto ambiental e as soluções emergentes como filtros e novos materiais.",
        "foto_url": "/static/imagens/blog/post3.jpg"
    }
]

def limpar_banco(session: Session):
    print("🧹 Iniciando limpeza do banco de dados...")
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
    print("Iniciando população do banco de dados...")
    create_db_and_tables()
    
    with Session(engine) as session:
        limpar_banco(session)

        # USUÁRIO ADMIN
        print("Criando usuário admin...")
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

        # FIBRAS NATURAIS
        print(f"Adicionando {len(FIBRAS_NATURAIS)} fibras naturais...")
        fibras_criadas = {}
        for item in FIBRAS_NATURAIS:
            fibra = Fibra(**item)
            session.add(fibra)
            session.commit()
            session.refresh(fibra)
            fibras_criadas[fibra.nome] = fibra

        # FIBRAS SINTÉTICAS
        print(f"Adicionando {len(FIBRAS_SINTETICAS)} fibras sintéticas...")
        for item in FIBRAS_SINTETICAS:
            fibra = Fibra(**item)
            session.add(fibra)
            session.commit()
            session.refresh(fibra)
            fibras_criadas[fibra.nome] = fibra

        # GALERIA (imagens extras)
        # print("Adicionando imagens à galeria...")
        # galeria = [
        #     # Algodão
        #     Galeria(url="/static/imagens/fibras/naturais/algodao/jeans.jpg", legenda="Jeans 100% algodão", fibra_id=fibras_criadas["Algodão"].id),
        #     Galeria(url="/static/imagens/fibras/naturais/algodao/camisa.jpg", legenda="Camisa de algodão", fibra_id=fibras_criadas["Algodão"].id),
        #     # Poliéster
        #     Galeria(url="/static/imagens/fibras/sinteticas/poliester/esportivo.jpg", legenda="Tecido esportivo dry-fit", fibra_id=fibras_criadas["Poliéster"].id),
        # ]
        # for foto in galeria:
        #     session.add(foto)

        # POSTS DO BLOG
        print(f"Adicionando {len(POSTS)} posts ao blog...")
        posts_criados = []
        for item in POSTS:
            post = Post(**item)
            session.add(post)
            session.commit()
            session.refresh(post)
            posts_criados.append(post)

        # COMENTÁRIO DE TESTE
        print("Adicionando comentário de teste...")
        comentario = Comentario(
            conteudo="Excelente post! A explicação técnica sobre polímeros ajudou muito.",
            usuario_id=admin.id,
            post_id=posts_criados[0].id
        )
        session.add(comentario)

        # FAVORITOS DE TESTE
        print("Adicionando favoritos de teste...")
        fav_fibra = FavoritoFibra(usuario_id=admin.id, fibra_id=fibras_criadas["Algodão"].id)
        fav_post = FavoritoPost(usuario_id=admin.id, post_id=posts_criados[1].id)
        session.add(fav_fibra)
        session.add(fav_post)

        session.commit()
        
        # Resumo final
        total_fibras = len(fibras_criadas)
        total_posts = len(posts_criados)
        print("\n" + "="*50)
        print("BANCO DE DADOS POPULADO COM SUCESSO!")
        print("="*50)
        print(f"Resumo:")
        print(f"    Usuários: 1")
        print(f"    Fibras naturais: {len(FIBRAS_NATURAIS)}")
        print(f"    Fibras sintéticas: {len(FIBRAS_SINTETICAS)}")
        # print(f"   Imagens na galeria: {len(galeria)}")
        print(f"    Posts no blog: {total_posts}")
        print(f"    Comentários: 1")
        print(f"    Favoritos: 2")
        print("="*50)

if __name__ == "__main__":
    popular_banco()