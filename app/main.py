from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database
from .services import FilmeService

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API de Filmes")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/filmes", response_model=list[schemas.Filme])
def listar_filmes(db: Session = Depends(get_db)):
    return FilmeService(db).listar()

@app.post("/filmes", response_model=schemas.Filme)
def criar_filme(filme: schemas.FilmeCreate, db: Session = Depends(get_db)):
    return FilmeService(db).criar(filme)

@app.get("/filmes/{filme_id}", response_model=schemas.Filme)
def obter_filme(filme_id: int, db: Session = Depends(get_db)):
    return FilmeService(db).buscar(filme_id)

@app.put("/filmes/{filme_id}", response_model=schemas.Filme)
def atualizar_filme(filme_id: int, filme: schemas.FilmeCreate, db: Session = Depends(get_db)):
    return FilmeService(db).atualizar(filme_id, filme)

@app.delete("/filmes/{filme_id}")
def deletar_filme(filme_id: int, db: Session = Depends(get_db)):
    return FilmeService(db).deletar(filme_id)
