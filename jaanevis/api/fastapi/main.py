from fastapi import Cookie, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from jaanevis.domain import note as n
from jaanevis.domain import session as s
from jaanevis.domain import user as u
from jaanevis.repository import Repository, repository
from jaanevis.requests import add_note_request, login_request
from jaanevis.requests.delete_note_request import DeleteNoteRequest
from jaanevis.requests.note_list_request import NoteListRequest
from jaanevis.requests.read_note_request import ReadNoteRequest
from jaanevis.requests.update_note_request import UpdateNoteRequest
from jaanevis.usecases import add_note, authenticate, delete_note
from jaanevis.usecases import login as login_uc
from jaanevis.usecases import note_list, read_note, update_note

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_user(session: str = Cookie(default=None)) -> u.User:
    """dependency function to authenticate user with session"""

    repo = repository()
    auth_usecase = authenticate.AuthenticateUseCase(repo)
    auth_request = authenticate.AuthenticateRequest.build(session=session)
    auth_res = auth_usecase.execute(auth_request)

    if not auth_res:
        raise HTTPException(status_code=401, detail=auth_res.message)
    return auth_res.value


async def get_repository() -> Repository:
    """dependency to get data repository"""

    return repository()


@app.get("/note", response_model=list[n.Note])
def read_notes(repo: Repository = Depends(get_repository)) -> list[n.Note]:
    """read notes"""

    note_list_usecase = note_list.NoteListUseCase(repo)
    request_obj = NoteListRequest.from_dict({"filters": {}})
    response = note_list_usecase.execute(request_obj)

    return response.value


@app.get("/note/geojson", response_model=list[n.NoteGeoJsonFeature])
def read_notes_geojson(
    repo: Repository = Depends(get_repository),
) -> list[n.NoteGeoJsonFeature]:
    """read notes as geojson feature objects"""

    note_list_usecase = note_list.GeoJsonNoteListUseCase(repo)
    request_obj = NoteListRequest.from_dict(data={"filters": {}})
    response = note_list_usecase.execute(request_obj)

    return response.value


@app.get("/note/{code}", response_model=n.Note)
def read_note_by_code(
    code: str, repo: Repository = Depends(get_repository)
) -> n.Note:
    """read note by code"""

    read_note_usecase = read_note.ReadNoteUseCase(repo)
    request_obj = ReadNoteRequest(code=code)
    response = read_note_usecase.execute(request_obj)

    return response.value


@app.delete("/note/{code}")
def delete_note_by_code(
    code: str,
    repo: Repository = Depends(get_repository),
    user: u.User = Depends(get_user),
) -> n.Note:
    """delete note by code"""

    repo = repository()

    delete_note_usecase = delete_note.DeleteNoteUseCase(repo)
    request_obj = DeleteNoteRequest(code=code, user=user)
    response = delete_note_usecase.execute(request_obj)

    return response.value


@app.post("/note")
def create_note(
    note_in: n.NoteCreateApi,
    user: u.User = Depends(get_user),
    repo: Repository = Depends(get_repository),
) -> n.Note:
    """add new note"""

    note = n.Note(**note_in.dict())

    add_note_usecase = add_note.AddNoteUseCase(repo)
    request_obj = add_note_request.AddNoteRequest.build(note=note, user=user)
    response = add_note_usecase.execute(request_obj)

    return response.value


@app.put("/note/{code}", response_model=n.Note)
def update_note_by_code(
    code: str,
    note_in: n.NoteUpdateApi,
    user: u.User = Depends(get_user),
    repo: Repository = Depends(get_repository),
) -> n.Note:
    """update note"""

    update_note_usecase = update_note.UpdateNoteUseCase(repo)
    request_obj = UpdateNoteRequest(code=code, note=note_in, user=user)
    response = update_note_usecase.execute(request_obj)

    return response.value


@app.post("/login")
def login(
    login_data: s.LoginInputApi, repo: Repository = Depends(get_repository)
) -> None:
    """login user and get session"""

    login_usecase = login_uc.LoginUseCase(repo)
    request = login_request.LoginRequest.build(
        username=login_data.username, password=login_data.password
    )
    login_response = login_usecase.execute(request)

    if not login_response:
        raise HTTPException(
            status_code=401, detail=login_response.value["message"]
        )

    response = JSONResponse(content={"session": login_response.value})
    response.set_cookie(key="session", value=login_response.value)

    return response
