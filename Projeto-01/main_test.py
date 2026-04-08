from fastapi import FastAPI, Depends, Request, HTTPException, Form, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from typing import Optional

from database import get_session, create_db_and_tables
from models import Fibra, Post, Usuario, Comentario, FavoritoFibra, FavoritoPost

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Verificar usuário logado
async def get_usuario_logado(
    request: Request, 
    session: Session = Depends(get_session), 
    usuario_id: Optional[str] = Cookie(None)
) -> Optional[Usuario]:
    if not usuario_id:
        return None
    return session.get(Usuario, int(usuario_id))


# **** NAVEGAÇÃO PRINCIPAL ****

# Ler página home 
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, usuario: Optional[Usuario] = Depends(get_usuario_logado)):
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/home_content.html", {"request": request, "usuario": usuario})
    return templates.TemplateResponse("index.html", {"request": request, "usuario": usuario})

# Ler página sobre 
@app.get("/sobre", response_class=HTMLResponse)
async def sobre(request: Request, usuario: Optional[Usuario] = Depends(get_usuario_logado)):
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/sobre_content.html", {"request": request, "usuario": usuario})
    
    return templates.TemplateResponse("sobre.html", {"request": request, "usuario": usuario})

# **** GERENCIAMENTO DA CONTA DO USUÁRIO ****

# Formulário de cadastro 
@app.get("/usuarios/cadastro", response_class=HTMLResponse)
async def form_cadastro(request: Request):
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/cadastro_form.html", {"request": request})
    
    return templates.TemplateResponse("cadastro.html", {"request": request})

# Cadastrar usuário (POST)
@app.post("/usuarios/cadastro", response_class=HTMLResponse)
async def criar_usuario(
    request: Request,
    nome: str = Form(...), 
    username: str = Form(...), 
    email: str = Form(...), 
    senha: str = Form(...),
    session: Session = Depends(get_session)
):
    # Verificar se usuário já existe
    existing = session.exec(select(Usuario).where(Usuario.username == username)).first()
    if existing:
        return HTMLResponse(content="<p style='color: red;'>Usuário já existe!</p>", status_code=400)
    
    novo_usuario = Usuario(nome=nome, username=username, email=email, senha=senha)
    session.add(novo_usuario)
    session.commit()
    
    
    if "HX-Request" in request.headers:
        return HTMLResponse(content=f"<p style='color: green;'>Conta criada, {novo_usuario.username}! <a href='/login'>Faça login</a></p>")
    
    return RedirectResponse(url="/login", status_code=303)

# Formulário de login 
@app.get("/login", response_class=HTMLResponse)
async def form_login(request: Request):
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/login_form.html", {"request": request})
    
    return templates.TemplateResponse("login.html", {"request": request})

# Logar 
@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    senha: str = Form(...),
    session: Session = Depends(get_session)
):
    statement = select(Usuario).where(Usuario.username == username, Usuario.senha == senha)
    usuario = session.exec(statement).first()
    
    if not usuario:
        return HTMLResponse(content="<p style='color: red;'>Usuário ou senha incorretos.</p>", status_code=401)
    
    response.set_cookie(key="usuario_id", value=str(usuario.id), httponly=True)
    
    
    if "HX-Request" in request.headers:
        return HTMLResponse(content=f"""
            <div>
                <p>Bem-vindo, {usuario.nome}!</p>
                <script>window.location.href = '/'</script>
            </div>
        """)
    
    return RedirectResponse(url="/", status_code=303)

# Logout
@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request, response: Response):
    response.delete_cookie(key="usuario_id")
    
    if "HX-Request" in request.headers:
        return HTMLResponse(content="<p>Logout realizado! <a href='/'>Home</a></p>")
    
    return RedirectResponse(url="/", status_code=303)

# Formulário de edição de perfil 
@app.get("/usuarios/editar", response_class=HTMLResponse)
async def form_editar_usuario(
    request: Request,
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        if "HX-Request" in request.headers:
            return HTMLResponse(content="<p>Faça login primeiro</p>", status_code=401)
        return RedirectResponse(url="/login", status_code=303)
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/editar_usuario_form.html", {"request": request, "usuario": usuario})
    
    return templates.TemplateResponse("editar_usuario.html", {"request": request, "usuario": usuario})

# Editar perfil
@app.put("/usuarios/editar", response_class=HTMLResponse)
async def editar_usuario(
    request: Request,
    nome: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    senha: Optional[str] = Form(None),
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        return HTMLResponse(content="<p style='color: red;'>Não autenticado</p>", status_code=401)
    
    if nome:
        usuario.nome = nome
    if email:
        usuario.email = email
    if senha:
        usuario.senha = senha
    
    session.add(usuario)
    session.commit()
    
    return HTMLResponse(content="<p style='color: green;'>Informações atualizadas com sucesso!</p>")

# Deletar conta
@app.delete("/usuarios/excluir-minha-conta", response_class=HTMLResponse)
async def excluir_conta(
    request: Request,
    response: Response,
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        return HTMLResponse(content="<p style='color: red;'>Precisa estar logado</p>", status_code=401)
    
    session.delete(usuario)
    session.commit()
    response.delete_cookie(key="usuario_id")
    
    if "HX-Request" in request.headers:
        return HTMLResponse(content="<p>Conta excluída! <a href='/'>Voltar à Home</a></p>")
    
    return RedirectResponse(url="/", status_code=303)


# **** LABORATÓRIO ****

@app.get("/laboratorio/microscopio", response_class=HTMLResponse)
async def listar_fibras(
    request: Request, 
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    fibras = session.exec(select(Fibra)).all()
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/fibras_list.html", {"request": request, "fibras": fibras, "usuario": usuario})
    
    return templates.TemplateResponse("laboratorio/catalogo.html", {"request": request, "fibras": fibras, "usuario": usuario})

@app.get("/laboratorio/fibra/{fibra_id}", response_class=HTMLResponse)
async def detalhes_fibra(
    request: Request, 
    fibra_id: int, 
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    fibra = session.get(Fibra, fibra_id)
    if not fibra:
        raise HTTPException(status_code=404, detail="Fibra não encontrada")
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/fibra_detalhes.html", {"request": request, "fibra": fibra, "usuario": usuario})
    
    return templates.TemplateResponse("laboratorio/detalhes.html", {"request": request, "fibra": fibra, "usuario": usuario})


# **** BLOG ****

@app.get("/blog", response_class=HTMLResponse)
async def listar_posts(
    request: Request, 
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    posts = session.exec(select(Post)).all()
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/posts_list.html", {"request": request, "posts": posts, "usuario": usuario})
    
    return templates.TemplateResponse("blog/lista_posts.html", {"request": request, "posts": posts, "usuario": usuario})

@app.get("/blog/{post_id}", response_class=HTMLResponse)
async def ler_post(
    request: Request, 
    post_id: int, 
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    post = session.get(Post, post_id)
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/post_detalhes.html", {"request": request, "post": post, "usuario": usuario})
    
    return templates.TemplateResponse("blog/post.html", {"request": request, "post": post, "usuario": usuario})


# **** INTERAÇÕES  ****

# Favoritar uma fibra
@app.post("/favoritar/{fibra_id}", response_class=HTMLResponse)
async def favoritar_fibra(
    request: Request,
    fibra_id: int, 
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        return HTMLResponse(content="<a href='/login'>Faça login para favoritar</a>", status_code=401)
    
    # Verificar se já existe
    existing = session.exec(
        select(FavoritoFibra).where(
            FavoritoFibra.usuario_id == usuario.id,
            FavoritoFibra.fibra_id == fibra_id
        )
    ).first()
    
    if existing:
        return HTMLResponse(content="Já favoritado", status_code=400)
    
    novo_fav = FavoritoFibra(usuario_id=usuario.id, fibra_id=fibra_id)
    session.add(novo_fav)
    session.commit()
    
    # Retornar botão atualizado 
    return HTMLResponse(content=f"Favoritado! <button hx-delete='/favorito/fibra/{fibra_id}' hx-target='this' hx-swap='outerHTML'>Desfavoritar</button>")

# Deletar uma fibra favoritada
@app.delete("/favorito/fibra/{fibra_id}", response_class=HTMLResponse)
async def deletar_favorito_fibra(
    request: Request,
    fibra_id: int, 
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        return HTMLResponse(status_code=401)
    
    statement = select(FavoritoFibra).where(
        FavoritoFibra.usuario_id == usuario.id, 
        FavoritoFibra.fibra_id == fibra_id
    )
    favorito = session.exec(statement).first()
    if favorito:
        session.delete(favorito)
        session.commit()
        return HTMLResponse(content="☆ Favoritar")
    return HTMLResponse(content="Erro", status_code=400)

# Postar um comentário
@app.post("/blog/{post_id}/comentar", response_class=HTMLResponse)
async def criar_comentario(
    request: Request,
    post_id: int, 
    conteudo: str = Form(...), 
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        return HTMLResponse(content="<p>Faça login para comentar</p>", status_code=401)
    
    novo_comentario = Comentario(conteudo=conteudo, usuario_id=usuario.id, post_id=post_id)
    session.add(novo_comentario)
    session.commit()
    session.refresh(novo_comentario)
    
    # Retorna o novo comentário para ser inserido na página
    return templates.TemplateResponse("partials/comentario_item.html", {
        "request": request, 
        "comentario": novo_comentario, 
        "usuario": usuario
    })

# Deletar comentário
@app.delete("/comentario/{comentario_id}", response_class=HTMLResponse)
async def deletar_comentario(
    request: Request,
    comentario_id: int,
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        return HTMLResponse(content="Não autenticado", status_code=401)
    
    comentario = session.get(Comentario, comentario_id)
    
    if not comentario:
        return HTMLResponse(content="Comentário não encontrado", status_code=404)
    
    if comentario.usuario_id != usuario.id:
        return HTMLResponse(content="Você só pode deletar seus próprios comentários", status_code=403)
    
    session.delete(comentario)
    session.commit()
    
    return HTMLResponse(content="")  # Retorna vazio para remover o elemento

# Favoritar post
@app.post("/blog/{post_id}/favoritar", response_class=HTMLResponse)
async def favoritar_post(
    request: Request,
    post_id: int,
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        return HTMLResponse(content="<a href='/login'>Faça login</a>", status_code=401)
    
    existing = session.exec(
        select(FavoritoPost).where(
            FavoritoPost.usuario_id == usuario.id,
            FavoritoPost.post_id == post_id
        )
    ).first()
    
    if existing:
        return HTMLResponse(content="Já favoritado", status_code=400)
    
    novo_fav = FavoritoPost(usuario_id=usuario.id, post_id=post_id)
    session.add(novo_fav)
    session.commit()
    
    return HTMLResponse(content="Favoritado!")

# Remover post favorito
@app.delete("/favorito/post/{post_id}", response_class=HTMLResponse)
async def deletar_favorito_post(
    request: Request,
    post_id: int,
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        return HTMLResponse(status_code=401)
    
    statement = select(FavoritoPost).where(
        FavoritoPost.usuario_id == usuario.id,
        FavoritoPost.post_id == post_id
    )
    favorito = session.exec(statement).first()
    
    if not favorito:
        return HTMLResponse(content="Favorito não encontrado", status_code=404)
    
    session.delete(favorito)
    session.commit()
    
    return HTMLResponse(content="☆ Favoritar")


# **** ROTAS PARA LISTAS DE FAVORITOS ****

@app.get("/usuarios/favoritos/fibras", response_class=HTMLResponse)
async def listar_fibras_favoritas(
    request: Request,
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        if "HX-Request" in request.headers:
            return HTMLResponse(content="<p>Faça login para ver seus favoritos</p>", status_code=401)
        return RedirectResponse(url="/login", status_code=303)
    
    favoritos = session.exec(
        select(Fibra).join(FavoritoFibra).where(FavoritoFibra.usuario_id == usuario.id)
    ).all()
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/favoritos_fibras_list.html", {"request": request, "favoritos": favoritos})
    
    return templates.TemplateResponse("favoritos_fibras.html", {"request": request, "favoritos": favoritos, "usuario": usuario})

@app.get("/usuarios/favoritos/posts", response_class=HTMLResponse)
async def listar_posts_favoritos(
    request: Request,
    session: Session = Depends(get_session),
    usuario: Optional[Usuario] = Depends(get_usuario_logado)
):
    if not usuario:
        if "HX-Request" in request.headers:
            return HTMLResponse(content="<p>Faça login para ver seus favoritos</p>", status_code=401)
        return RedirectResponse(url="/login", status_code=303)
    
    favoritos = session.exec(
        select(Post).join(FavoritoPost).where(FavoritoPost.usuario_id == usuario.id)
    ).all()
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse("partials/favoritos_posts_list.html", {"request": request, "favoritos": favoritos})
    
    return templates.TemplateResponse("favoritos_posts.html", {"request": request, "favoritos": favoritos, "usuario": usuario})