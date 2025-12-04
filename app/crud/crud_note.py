from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()

def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Note).offset(skip).limit(limit).all()

def create_note(db: Session, note: NoteCreate):
    db_note = Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: int, note: NoteUpdate):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return None
    
    update_data = note.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_note, key, value)
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note
