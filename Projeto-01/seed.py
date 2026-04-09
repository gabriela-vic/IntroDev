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
        "conteudo": """As fibras naturais representam a base histórica da indústria têxtil, com propriedades únicas derivadas de sua origem biológica. A celulose, principal componente do algodão e linho, forma estruturas cristalinas que conferem resistência e durabilidade excepcional. Sob o microscópio, podemos observar como as convoluções características do algodão criam bolsões de ar que proporcionam isolamento térmico natural e absorção de umidade superior.

A seda, por sua vez, apresenta uma estrutura triangular que refrata a luz de maneira única, criando o brilho característico que a tornou tão valorizada ao longo dos séculos. A lã ovina possui escamas sobrepostas que permitem a formação de feltro e criam uma barreira natural contra o vento e a água. Essas estruturas moleculares não apenas determinam as propriedades físicas das fibras, mas também influenciam diretamente no conforto e na performance dos tecidos finais.""",
        "foto_url": "/static/imagens/blog/post1.jpg"
    },
    {
        "titulo": "Sustentabilidade e o Futuro da Moda",
        "conteudo": """A indústria da moda enfrenta um desafio crítico: reconciliar a demanda crescente por vestuário com a necessidade urgente de reduzir seu impacto ambiental. O ciclo de vida das fibras têxteis, desde o cultivo ou síntese até o descarte, representa uma das maiores fontes de emissões de carbono e consumo de água no setor industrial. As fibras naturais convencionais, como o algodão, requerem quantidades significativas de água e pesticidas, enquanto as sintéticas derivadas de petróleo contribuem para a acumulação de microplásticos nos oceanos.

No entanto, inovações promissoras estão emergindo no horizonte. Novos biopolímeros derivados de fontes renováveis, como o PLA (ácido poliláctico) e o PHA (poli-hidroxialcanoato), oferecem alternativas biodegradáveis às fibras sintéticas tradicionais. Tecnologias de reciclagem química avançada permitem a transformação de resíduos têxteis em novas fibras de alta qualidade, reduzindo a dependência de matérias-primas virgens. A transição para uma moda verdadeiramente sustentável exigirá colaboração entre cientistas, designers e consumidores para reimaginar todo o ecossistema têxtil.""",
        "foto_url": "/static/imagens/blog/post2.jpg"
    },
    {
        "titulo": "Microplásticos: O desafio das fibras sintéticas",
        "conteudo": """Cada lavagem de roupas sintéticas libera milhões de microfibras plásticas que escapam dos sistemas de tratamento de esgoto e acabam nos oceanos. Essas partículas microscópicas, menores que 5 milímetros, são ingeridas por organismos marinhos e entram na cadeia alimentar humana, acumulando toxinas e metais pesados. O poliéster e o nylon, fibras mais comuns na indústria têxtil, são particularmente problemáticos devido à sua durabilidade excepcional - uma qualidade que se transforma em maldição ambiental.

Pesquisas recentes estimam que até 35% dos microplásticos encontrados nos oceanos originam-se da lavagem de roupas sintéticas. Soluções inovadoras estão sendo desenvolvidas, incluindo filtros especializados para máquinas de lavar, enzimas que degradam as fibras durante a lavagem, e novos materiais biodegradáveis que se decompõem naturalmente. A conscientização do consumidor também desempenha papel crucial: programas de coleta de roupas usadas e a preferência por fibras naturais ou recicladas podem reduzir significativamente a contribuição individual para este problema global.""",
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

        # USUÁRIO TESTE
        usuario_teste = Usuario(
            nome="Maria Silva",
            username="maria_s",
            email="maria.silva@email.com",
            senha="123",
            bio="Designer de moda interessada em sustentabilidade e inovação têxtil."
        )
        session.add(usuario_teste)
        session.commit()
        session.refresh(usuario_teste)

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
        print(f"Adicionando {len(POSTS)} posts do blog...")
        posts_criados = {}
        for item in POSTS:
            post = Post(**item)
            session.add(post)
            session.commit()
            session.refresh(post)
            posts_criados[post.titulo] = post

        # COMENTÁRIOS
        print("Adicionando comentários aos posts...")
        comentario1 = Comentario(
            conteudo="Excelente artigo! Como designer, sempre me pergunto sobre o impacto das fibras sintéticas. As soluções mencionadas são muito promissoras.",
            usuario_id=usuario_teste.id,
            post_id=posts_criados["Microplásticos: O desafio das fibras sintéticas"].id
        )
        session.add(comentario1)
        session.commit()

        comentario2 = Comentario(
            conteudo="Muito informativo! Gostaria de saber mais sobre as alternativas biodegradáveis mencionadas no artigo sobre sustentabilidade.",
            usuario_id=usuario_teste.id,
            post_id=posts_criados["Sustentabilidade e o Futuro da Moda"].id
        )
        session.add(comentario2)
        session.commit()

        # COMENTÁRIOS DA MARIA SILVA
        comentario_maria1 = Comentario(
            conteudo="Como estudante de química, adorei a explicação sobre a estrutura molecular das fibras naturais. O algodão realmente tem uma estrutura fascinante!",
            usuario_id=usuario_teste.id,
            post_id=posts_criados["A Ciência por trás das Fibras Naturais"].id
        )
        session.add(comentario_maria1)
        session.commit()

        comentario_maria2 = Comentario(
            conteudo="Concordo totalmente com as soluções apresentadas. Como consumidora consciente, procuro sempre fibras orgânicas. Obrigada pelo artigo esclarecedor!",
            usuario_id=usuario_teste.id,
            post_id=posts_criados["Microplásticos: O desafio das fibras sintéticas"].id
        )
        session.add(comentario_maria2)
        session.commit()

        # FAVORITOS DA MARIA SILVA
        print("Adicionando favoritos da Maria Silva...")
        # Favoritos de fibras
        favorito_fibra_maria1 = FavoritoFibra(
            usuario_id=usuario_teste.id,
            fibra_id=fibras_criadas["Algodão"].id
        )
        session.add(favorito_fibra_maria1)
        session.commit()

        favorito_fibra_maria2 = FavoritoFibra(
            usuario_id=usuario_teste.id,
            fibra_id=fibras_criadas["Linho"].id
        )
        session.add(favorito_fibra_maria2)
        session.commit()

        # Favoritos de posts
        favorito_post_maria1 = FavoritoPost(
            usuario_id=usuario_teste.id,
            post_id=posts_criados["A Ciência por trás das Fibras Naturais"].id
        )
        session.add(favorito_post_maria1)
        session.commit()

        favorito_post_maria2 = FavoritoPost(
            usuario_id=usuario_teste.id,
            post_id=posts_criados["Sustentabilidade e o Futuro da Moda"].id
        )
        session.add(favorito_post_maria2)
        session.commit()

        # FAVORITOS DE TESTE
        print("Adicionando favoritos de teste...")
        fav_fibra = FavoritoFibra(usuario_id=admin.id, fibra_id=fibras_criadas["Algodão"].id)
        fav_post = FavoritoPost(usuario_id=admin.id, post_id=posts_criados["Sustentabilidade e o Futuro da Moda"].id)
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