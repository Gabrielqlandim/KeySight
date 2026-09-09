"""Ponto de entrada da API do KeySight.

Este arquivo cria a aplicação FastAPI e define as primeiras rotas.
Por enquanto não fala com o banco de dados nem com nenhuma API externa —
isso vem nos próximos módulos. O objetivo aqui é só validar que o
backend sobe e responde.
"""
from app import itad_client
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.post("/games/{game_id}/refresh-price")
async def refresh_price(game_id: int, db: Session = Depends(get_db)):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail= "Jogo não encontrado")
    try:
        itad_id = await itad_client.lookup_game_id(db_game.name)
        if itad_id is None:
            raise HTTPException(status_code=404, detail="Jogo nao encontado na base da api do itad")
        deals = await itad_client.get_current_prices(itad_id)
    except itad_client.ITADClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    updated_offers = []
    for deal in deals:
        shop_name = deal["shop"]["name"]
        price = deal["price"]["amount"]
        url = deal["url"]
        offer = (
            db.query(models.StoreOffer).filter(
                models.StoreOffer.game_id == game_id,
                models.StoreOffer.store_name == shop_name,
            ).first()
        )
        if offer is None:
            offer = models.StoreOffer(
                game_id=game_id,
                store_name = shop_name,
                current_price = price,
                url = url,
            )
            db.add(offer)
            db.flush()
        else:
            offer.current_price = price
            offer.url = url

        db.add(models.PriceHistory(offer_id = offer.id, price=price))
        updated_offers.append(shop_name)
    db.commit()
    return { "game": db_game.name, "stores_updated": updated_offers}

@app.get("/games/{game_id}/offers", response_model=list[schemas.StoreOfferRead])
def list_offers(game_id: int, db: Session = Depends(get_db)):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()

    if db_game is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    return db.query(models.StoreOffer).filter(models.StoreOffer.game_id == game_id).all()

@app.get("/games/{game_id}/price-history", response_model=list[schemas.PricePoint])
def price_history(game_id: int, db: Session = Depends(get_db)):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()

    if db_game is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    history = (
        db.query(models.PriceHistory)
        .join(models.StoreOffer, models.PriceHistory.offer_id == models.StoreOffer.id)
        .filter(models.StoreOffer.game_id == game_id)
        .order_by(models.PriceHistory.recorded_at)
        .all()
    )
    return history