from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jaanevis.domain import note as n
from jaanevis.repository import memrepo as mr
from jaanevis.requests.add_note_request import AddNoteRequest
from jaanevis.requests.note_list_request import NoteListRequest
from jaanevis.usecases import add_note, note_list

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/note", response_model=list[n.Note])
def read_notes() -> list[n.Note]:
    """read notes"""

    repo = mr.MemRepo()

    note_list_usecase = note_list.NoteListUseCase(repo)
    request_obj = NoteListRequest(filters={})
    response = note_list_usecase.execute(request_obj)

    return response.value


@app.get("/note/geojson", response_model=list[n.NoteGeoJsonFeature])
def read_notes_geojson() -> list[n.NoteGeoJsonFeature]:
    """read notes as geojson feature objects"""

    repo = mr.MemRepo()

    note_list_usecase = note_list.GeoJsonNoteListUseCase(repo)
    request_obj = NoteListRequest(filters={})
    response = note_list_usecase.execute(request_obj)

    return response.value


@app.post("/note", response_model=n.Note)
def create_note(note_in: n.NoteCreateApi) -> n.Note:
    """add new note"""

    note = n.Note(**note_in.dict(), creator="default")
    repo = mr.MemRepo()

    add_note_usecase = add_note.AddNoteUseCase(repo)
    request_obj = AddNoteRequest(note)
    response = add_note_usecase.execute(request_obj)

    return response.value
