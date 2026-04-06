from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="Templates")

# Variável global para manter estado das curtidas
likes_count = 0

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"likes": likes_count})

@app.get("/abas/curtidas", response_class=HTMLResponse)
async def aba_curtidas(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"likes": likes_count, "pagina_inicial": "/abas/curtidas"})
    return templates.TemplateResponse(request, "curtidas.html", {"likes": likes_count})

@app.post("/curtir", response_class=HTMLResponse)
async def curtir(request: Request):
    global likes_count
    likes_count += 1
    return templates.TemplateResponse(request, "curtidas.html", {"likes": likes_count})

@app.post("/resetar", response_class=HTMLResponse)
async def resetar(request: Request):
    global likes_count
    likes_count = 0
    return templates.TemplateResponse(request, "curtidas.html", {"likes": likes_count})

@app.get("/abas/jupiter", response_class=HTMLResponse)
async def aba_jupiter(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", {"pagina_inicial": "/abas/jupiter"})
    return templates.TemplateResponse(request, "jupiter.html")

@app.get("/abas/professor", response_class=HTMLResponse)
async def aba_professor(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", {"pagina_inicial": "/abas/professor"})
    return templates.TemplateResponse(request, "professor.html")

@app.get("/proxima_aba")
def proxima_aba(request: Request):
    url_atual = request.headers.get("HX-Current-URL", "")
    
    if "jupiter" in url_atual:
        proxima = "professor.html"
        nova_url = "/abas/professor"
    elif "professor" in url_atual:
        proxima = "curtidas.html"
        nova_url = "/abas/curtidas"
    else:
        proxima = "jupiter.html"
        nova_url = "/abas/jupiter"
    
    
    resposta = templates.TemplateResponse(request, proxima, {"likes": likes_count})
    resposta.headers["HX-Push-Url"] = nova_url
    
    return resposta