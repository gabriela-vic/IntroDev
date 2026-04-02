from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
import time
import logging
from fastapi import Depends, HTTPException, status, Cookie, Response
from typing import Annotated


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class Usuario(BaseModel):
    nome: str
    senha: str
    bio: str

db_usuarios = []

# 1. Rota de EXIBIÇÃO cadastro
@app.get("/", response_class=HTMLResponse)
async def pagina_cadastro(request: Request):
    return templates.TemplateResponse(
        request = request,
        name="cadastro.html", 
        context={"request": request}
    )

# 2. Rota de AÇÃO cadastro
@app.post("/users")
async def criar_usuario(user: Usuario):
    db_usuarios.append(user.model_dump()) 
    return {"status": "sucesso", "usuario": user.nome}

# 3. Rota de EXIBIÇÃO login
@app.get("/login", response_class=HTMLResponse)
async def pagina_login(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={"request": request}
    )

# 4. Rota de AÇÃO login
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), response: Response = None):
    usuario_encontrado = next(
        (u for u in db_usuarios if u["nome"] == username and u["senha"] == password), 
        None
    )
    
    if not usuario_encontrado:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    
    
    res = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    
    
    res.set_cookie(key="session_user", value=username)
    
    return res


def get_active_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado: você não está logado."
        )
    
    
    user = next((u for u in db_usuarios if u["nome"] == session_user), None)
    
    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    return user

@app.get("/home", response_class=HTMLResponse)
async def pagina_home(request: Request, user: dict = Depends(get_active_user)):
    return templates.TemplateResponse(
        request=request, 
        name="home.html", 
        context={
            "request": request, 
            "username": user["nome"], 
            "bio": user["bio"]
        }
    )