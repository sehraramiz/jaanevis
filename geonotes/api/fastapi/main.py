from fastapi import FastAPI

from geonotes.domain import note as n
from geonotes.repository import memrepo as mr
from geonotes.requests.note_list_request import NoteListRequest
from geonotes.usecases import note_list

from .sample_data import note_dicts

app = FastAPI()


@app.get("/note", response_model=list[n.Note])
def read_notes() -> list[n.Note]:
    repo = mr.MemRepo(note_dicts)
    note_list_usecase = note_list.NoteListUseCase(repo)
    request_obj = NoteListRequest(filters={})
    response = note_list_usecase.execute(request_obj)
    return response.value
