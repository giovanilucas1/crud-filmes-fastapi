from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

class FilmeService:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(models.Filme).all()

    def buscar(self, filme_id: int):
        filme = self.db.query(models.Filme).filter(models.Filme.id == filme_id).first()
        if not filme:
            raise HTTPException(status_code=404, detail="Filme não encontrado")
        return filme

    def criar(self, dados: schemas.FilmeCreate):
        novo = models.Filme(**dados.dict())
        self.db.add(novo)
        self.db.commit()
        self.db.refresh(novo)
        return novo

    def atualizar(self, filme_id: int, dados: schemas.FilmeCreate):
        filme = self.buscar(filme_id)
        for campo, valor in dados.dict().items():
            setattr(filme, campo, valor)
        self.db.commit()
        self.db.refresh(filme)
        return filme

    def deletar(self, filme_id: int):
        filme = self.buscar(filme_id)
        self.db.delete(filme)
        self.db.commit()
        return {"mensagem": "Filme deletado com sucesso"}
