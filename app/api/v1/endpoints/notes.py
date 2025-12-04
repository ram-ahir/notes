from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import crud_note
from app.schemas.note import Note, NoteCreate, NoteUpdate
from app.db.session import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return crud_note.create_note(db=db, note=note)

@router.get("/", response_model=List[Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = crud_note.get_notes(db, skip=skip, limit=limit)
    return notes

@router.get("/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud_note.get_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.put("/{note_id}", response_model=Note)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = crud_note.update_note(db, note_id=note_id, note=note)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.delete("/{note_id}", response_model=Note)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud_note.delete_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note
