# Arquivo main.py

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import col
from Models import Aluno
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi.responses import RedirectResponse

@asynccontextmanager
async def initFunction(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=initFunction)

app.mount("/Static", StaticFiles(directory="static"), name="static")

arquivo_sqlite = "HTMX2.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"

engine = create_engine(url_sqlite)

templates = Jinja2Templates(directory=["Templates", "Templates/Partials"])

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ===== ROTA PRINCIPAL =====

@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/busca")
@app.get("/busca", response_class=HTMLResponse)
def busca(request: Request):
    return templates.TemplateResponse(request, "index.html")


# ===== FUNÇÃO DE BUSCA COM FILTRO =====
def buscar_alunos(busca: str = '', pagina: int = 1, itens_por_pagina: int = 5):
    with Session(engine) as session:
        # Query base
        query = select(Aluno)
        
        # Aplica filtro de busca se existir
        if busca:
            query = query.where(Aluno.nome.contains(busca))
        
        # Conta total de registros 
        total = len(session.exec(query).all())  # ← MUDANÇA AQUI
        
        # Aplica ordenação
        query = query.order_by(Aluno.nome)
        
        # Aplica paginação
        offset = (pagina - 1) * itens_por_pagina
        query = query.offset(offset).limit(itens_por_pagina)
        
        alunos = session.exec(query).all()
        
        # Calcula total de páginas
        total_paginas = (total + itens_por_pagina - 1) // itens_por_pagina
        
        return {
            "alunos": alunos,
            "total": total,
            "total_paginas": total_paginas,
            "pagina_atual": pagina,
            "itens_por_pagina": itens_por_pagina
        }

# ===== ROTA LISTA (COM BUSCA) =====
@app.get("/lista", response_class=HTMLResponse)
def lista(request: Request, busca: str = '', pagina: int = 1):
    resultado = buscar_alunos(busca, pagina)
    
    return templates.TemplateResponse(request, "lista.html", {
        "alunos": resultado["alunos"],
        "busca": busca,
        "pagina_atual": resultado["pagina_atual"],
        "total_paginas": resultado["total_paginas"],
        "total": resultado["total"]
    })


# ===== ROTA FORMULÁRIO DE EDIÇÃO =====
@app.get("/editarAlunos", response_class=HTMLResponse)
def editar_alunos(request: Request):
    return templates.TemplateResponse(request, "options.html")


# ===== ROTA CRIAR ALUNO (POST) =====
@app.post("/novoAluno", response_class=HTMLResponse)
def criar_aluno(nome: str = Form(...)):
    with Session(engine) as session:
        novo_aluno = Aluno(nome=nome)
        session.add(novo_aluno)
        session.commit()
        session.refresh(novo_aluno)
        return HTMLResponse(content=f"<p>O(a) aluno(a) {novo_aluno.nome} foi registrado(a)!</p>")


# ===== ROTA DELETAR ALUNO =====
@app.delete("/deletaAluno", response_class=HTMLResponse)
def deletar_aluno(id: int):
    with Session(engine) as session:
        query = select(Aluno).where(Aluno.id == id)
        aluno = session.exec(query).first()
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        session.delete(aluno)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) aluno(a) {aluno.nome} foi deletado(a)!</p>")


# ===== ROTA ATUALIZAR ALUNO =====
@app.put("/atualizaAluno", response_class=HTMLResponse)
def atualizar_aluno(id: int = Form(...), novoNome: str = Form(...)):
    with Session(engine) as session:
        query = select(Aluno).where(Aluno.id == id)
        aluno = session.exec(query).first()
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        nomeAntigo = aluno.nome
        aluno.nome = novoNome
        session.commit()
        session.refresh(aluno)
        return HTMLResponse(content=f"<p>O(a) aluno(a) {nomeAntigo} foi atualizado(a) para {aluno.nome}!</p>")


# ===== ROTA APAGAR SITE =====
@app.delete("/apagar", response_class=HTMLResponse)
def apagar():
    return ""



@app.get("/debug/alunos")
def debug_alunos():
    with Session(engine) as session:
        alunos = session.exec(select(Aluno)).all()
        return {"total": len(alunos), "alunos": [{"id": a.id, "nome": a.nome} for a in alunos]}