from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jaanevis.domain import note as n
from jaanevis.repository import repository
from jaanevis.requests.add_note_request import AddNoteRequest
from jaanevis.requests.delete_note_request import DeleteNoteRequest
from jaanevis.requests.note_list_request import NoteListRequest
from jaanevis.requests.read_note_request import ReadNoteRequest
from jaanevis.usecases import add_note, delete_note, note_list, read_note

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

    repo = repository()

    note_list_usecase = note_list.NoteListUseCase(repo)
    request_obj = NoteListRequest(filters={})
    response = note_list_usecase.execute(request_obj)

    return response.value


@app.get("/note/geojson", response_model=list[n.NoteGeoJsonFeature])
def read_notes_geojson() -> list[n.NoteGeoJsonFeature]:
    """read notes as geojson feature objects"""

    repo = repository()

    note_list_usecase = note_list.GeoJsonNoteListUseCase(repo)
    request_obj = NoteListRequest(filters={})
    response = note_list_usecase.execute(request_obj)

    return response.value


@app.get("/note/{code}", response_model=n.Note)
def read_note_by_code(code: str) -> n.Note:
    """read note by code"""

    repo = repository()

    read_note_usecase = read_note.ReadNoteUseCase(repo)
    request_obj = ReadNoteRequest(code=code)
    response = read_note_usecase.execute(request_obj)

    return response.value


@app.delete("/note/{code}", response_model=n.Note)
def delete_note_by_code(code: str) -> n.Note:
    """delete note by code"""

    repo = repository()

    delete_note_usecase = delete_note.DeleteNoteUseCase(repo)
    request_obj = DeleteNoteRequest(code=code)
    response = delete_note_usecase.execute(request_obj)

    return response.value


@app.post("/note", response_model=n.Note)
def create_note(note_in: n.NoteCreateApi) -> n.Note:
    """add new note"""

    note = n.Note(**note_in.dict(), creator="default")
    repo = repository()

    add_note_usecase = add_note.AddNoteUseCase(repo)
    request_obj = AddNoteRequest(note)
    response = add_note_usecase.execute(request_obj)

    return response.value
