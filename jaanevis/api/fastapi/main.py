from fastapi import Cookie, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from jaanevis.domain import note as n
from jaanevis.repository import repository
from jaanevis.requests import add_note_request
from jaanevis.requests.delete_note_request import DeleteNoteRequest
from jaanevis.requests.note_list_request import NoteListRequest
from jaanevis.requests.read_note_request import ReadNoteRequest
from jaanevis.requests.update_note_request import UpdateNoteRequest
from jaanevis.usecases import (
    add_note,
    authenticate,
    delete_note,
    note_list,
    read_note,
    update_note,
)

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
    request_obj = NoteListRequest.from_dict({"filters": {}})
    response = note_list_usecase.execute(request_obj)

    return response.value


@app.get("/note/geojson", response_model=list[n.NoteGeoJsonFeature])
def read_notes_geojson() -> list[n.NoteGeoJsonFeature]:
    """read notes as geojson feature objects"""

    repo = repository()

    note_list_usecase = note_list.GeoJsonNoteListUseCase(repo)
    request_obj = NoteListRequest.from_dict(data={"filters": {}})
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


@app.post("/note")
def create_note(
    note_in: n.NoteCreateApi,
    session: str = Cookie(default=None),
) -> n.Note:
    """add new note"""

    repo = repository()
    auth_usecase = authenticate.AuthenticateUseCase(repo)
    auth_request = authenticate.AuthenticateRequest.build(session=session)
    auth_res = auth_usecase.execute(auth_request)

    if not auth_res:
        raise HTTPException(status_code=401, detail=auth_res.message)

    note = n.Note(**note_in.dict())

    add_note_usecase = add_note.AddNoteUseCase(repo)
    request_obj = add_note_request.AddNoteRequest.build(
        note=note, user=auth_res.value
    )
    response = add_note_usecase.execute(request_obj)

    return response.value


@app.put("/note/{code}", response_model=n.Note)
def update_note_by_code(code: str, note_in: n.NoteUpdateApi) -> n.Note:
    """update note"""

    repo = repository()

    update_note_usecase = update_note.UpdateNoteUseCase(repo)
    request_obj = UpdateNoteRequest(code=code, note=note_in)
    response = update_note_usecase.execute(request_obj)

    return response.value
