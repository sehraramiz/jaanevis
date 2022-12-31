from fastapi import FastAPI

from geonotes.domain import note as n
from geonotes.repository import memrepo as mr
from geonotes.requests.add_note_request import AddNoteRequest
from geonotes.requests.note_list_request import NoteListRequest
from geonotes.usecases import add_note, note_list

from .sample_data import note_dicts

app = FastAPI()


@app.get("/note")
def read_notes() -> list[n.Note]:
    repo = mr.MemRepo(note_dicts)

    note_list_usecase = note_list.NoteListUseCase(repo)
    request_obj = NoteListRequest(filters={})
    response = note_list_usecase.execute(request_obj)

    return response.value


@app.post("/note")
def create_note(note_in: n.NoteCreateApi) -> n.Note:
    note = n.Note(**note_in.dict(), creator="default")
    repo = mr.MemRepo(note_dicts)

    add_note_usecase = add_note.AddNoteUseCase(repo)
    request_obj = AddNoteRequest(note)
    response = add_note_usecase.execute(request_obj)

    return response.value
