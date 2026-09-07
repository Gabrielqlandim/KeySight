"""Ponto de entrada da API do KeySight.

Este arquivo cria a aplicação FastAPI e define as primeiras rotas.
Por enquanto não fala com o banco de dados nem com nenhuma API externa —
isso vem nos próximos módulos. O objetivo aqui é só validar que o
backend sobe e responde.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import engine, get_db, Base
from app import models, schemas

Base.metadata.create_all(bind=engine)

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


@app.post("/games", response_model=schemas.GameRead, status_code=201)
def create_game(game: schemas.GameCreate, db: Session=Depends(get_db)):
    db_game = models.Game(**game.model_dump())
    db.add(db_game)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Slug já cadastrado")
    db.refresh(db_game)
    return db_game

@app.get("/games", response_model=list[schemas.GameRead])
def list_games(db: Session = Depends(get_db)):
    return db.query(models.Game).all()

@app.get("/games/{game_id}", response_model=schemas.GameRead)
def get_game(game_id: int, db: Session = Depends(get_db)):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return db_game

@app.delete("/games/{game_id}", status_code=204)
def delete_game(game_id: int, db: Session= Depends(get_db)):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    db.delete(db_game)
    db.commit()