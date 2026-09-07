"""Ponto de entrada da API do KeySight.

Este arquivo cria a aplicação FastAPI e define as primeiras rotas.
Por enquanto não fala com o banco de dados nem com nenhuma API externa —
isso vem nos próximos módulos. O objetivo aqui é só validar que o
backend sobe e responde.
"""

from fastapi import FastAPI

# `FastAPI()` cria a aplicação em si. É esse objeto `app` que o uvicorn
# (o servidor) vai importar e rodar. `title` e `version` não têm efeito
# funcional na API, mas aparecem na documentação automática
# (disponível em /docs quando o servidor estiver rodando).
app = FastAPI(
    title="KeySight API",
    version="0.1.0",
)


# `@app.get("/")` é um "decorator": ele registra a função logo abaixo
# como a responsável por atender requisições HTTP GET na rota "/".
# Quando alguém acessa http://localhost:8000/, o FastAPI chama `read_root()`.
@app.get("/")
def read_root():
    # FastAPI converte automaticamente o dicionário Python retornado
    # em uma resposta JSON. Não precisamos fazer isso manualmente.
    return {"status": "ok", "service": "KeySight API"}


# Rota extra só para provar que dá pra ter mais de um endpoint e que
# parâmetros simples funcionam sem configuração extra.
@app.get("/health")
def health_check():
    return {"healthy": True}
