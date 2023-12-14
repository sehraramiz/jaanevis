from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from jaanevis.domain import note as n
from jaanevis.domain import session as s
from jaanevis.domain import user as u
from jaanevis.i18n import gettext as _
from jaanevis.repository import Repository, repository
from jaanevis.requests import (
    activate_user_request,
    add_note_request,
    login_request,
    logout_request,
    note_list_request,
    register_request,
)
from jaanevis.requests.delete_note_request import DeleteNoteRequest
from jaanevis.requests.read_note_request import ReadNoteRequest
from jaanevis.requests.update_note_request import UpdateNoteRequest
from jaanevis.requests.update_own_user_request import UpdateOwnUserRequest
from jaanevis.usecases import activate_user as activate_user_uc
from jaanevis.usecases import add_note, authenticate, delete_note
from jaanevis.usecases import login as login_uc
from jaanevis.usecases import logout as logout_uc
from jaanevis.usecases import note_list, read_note
from jaanevis.usecases import register as register_uc
from jaanevis.usecases import update_note, update_own_user

router = APIRouter()


async def get_user(session: str = Cookie(default=None)) -> u.UserRead:
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


@router.get("/note")
def read_notes(
    creator: Optional[str] = None,
    country: Optional[str] = None,
    tag: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    repo: Repository = Depends(get_repository),
) -> list[n.NoteRead]:
    """read notes"""

    note_list_usecase = note_list.NoteListUseCase(repo)
    request_obj = note_list_request.NoteListRequest.from_dict(
        data={
            "filters": {
                "creator__eq": creator,
                "country__eq": country,
                "tag__eq": tag,
            },
            "limit": limit,
            "skip": skip,
        }
    )
    response = note_list_usecase.execute(request_obj)

    return response.value


@router.get("/note/geojson", response_model=list[n.NoteGeoJsonFeature])
def read_notes_geojson(
    creator: Optional[str] = None,
    country: Optional[str] = None,
    tag: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    repo: Repository = Depends(get_repository),
) -> list[n.NoteGeoJsonFeature]:
    """read notes as geojson feature objects"""

    note_list_usecase = note_list.GeoJsonNoteListUseCase(repo)
    request_obj = note_list_request.NoteListRequest.from_dict(
        data={
            "filters": {
                "creator__eq": creator,
                "country__eq": country,
                "tag__eq": tag,
            },
            "skip": skip,
            "limit": limit,
        }
    )
    response = note_list_usecase.execute(request_obj)

    return response.value


@router.get("/note/{code}")
def read_note_by_code(
    code: str, repo: Repository = Depends(get_repository)
) -> n.NoteRead:
    """read note by code"""

    read_note_usecase = read_note.ReadNoteUseCase(repo)
    request_obj = ReadNoteRequest(code=code)
    response = read_note_usecase.execute(request_obj)

    return response.value


@router.delete("/note/{code}")
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

    if not response:
        raise HTTPException(status_code=403, detail=response.value["message"])
    return response.value


@router.post("/note")
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


@router.put("/note/{code}")
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

    if not response:
        raise HTTPException(status_code=403, detail=response.value["message"])
    return response.value


@router.post("/user/login")
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
        return JSONResponse(
            login_response.value,
            status_code=401,
        )

    response = JSONResponse(
        content={"session": login_response.value["session"]}
    )
    response.set_cookie(
        key="session",
        value=login_response.value["session"],
        expires=login_response.value["expires"],
        secure=True,
        httponly=True,
    )

    return response


@router.get("/user/logout")
def logout(
    session: str = Cookie(default=None),
    repo: Repository = Depends(get_repository),
) -> None:
    """user logout"""

    logout_usecase = logout_uc.LogoutUseCase(repo)
    request = logout_request.LogoutRequest.build(session=session)
    logout_response = logout_usecase.execute(request)

    if not logout_response:
        return JSONResponse(
            logout_response.value,
            status_code=401,
        )

    response = JSONResponse(content={"success": True})
    yesterday = datetime.now() - timedelta(days=1)
    expire_yesterday = yesterday.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.set_cookie(key="session", value="", expires=expire_yesterday)
    return response


@router.post("/user/register")
def register(
    register_data: s.RegisterInputApi,
    repo: Repository = Depends(get_repository),
) -> None:
    """user registeration"""

    register_usecase = register_uc.RegisterUseCase(repo=repo)
    request = register_request.RegisterRequest.build(
        email=register_data.email,
        username=register_data.username,
        password=register_data.password,
    )
    response = register_usecase.execute(request)

    if not response:
        return JSONResponse(
            response.value,
            status_code=400,
        )

    return response.value


@router.get("/user/activate", response_class=HTMLResponse)
def activate(
    username: str,
    token: str,
    repo: Repository = Depends(get_repository),
) -> None:
    """activate user with activation token"""

    request = activate_user_request.ActivateUserRequest.build(
        username=username, token=token
    )
    activate_user_usecase = activate_user_uc.ActivateUserUseCase(repo=repo)
    response = activate_user_usecase.execute(request)

    success_html = """
    <html>
        <body>
            <p>{}.</p>
        </body>
    </html>
    """.format(
        _("user successfuly activated")
    )
    if response:
        return HTMLResponse(content=success_html, status_code=200)

    failure_html = """
    <html>
        <body>
            <p>{}.<br>{}</p>
        </body>
    </html>
    """.format(
        _("activation failure"), response.value["message"]
    )
    return HTMLResponse(content=failure_html, status_code=200)


@router.put("/user/own")
def update_own_user_api(
    user_in: u.UserUpdateApi,
    user: u.User = Depends(get_user),
    repo: Repository = Depends(get_repository),
) -> u.UserRead:
    """update own user"""

    update_user_usecase = update_own_user.UpdateOwnUserUseCase(repo)
    request_obj = UpdateOwnUserRequest.build(update_user=user_in, user=user)
    response = update_user_usecase.execute(request_obj)

    if not response:
        raise HTTPException(status_code=403, detail=response.value["message"])
    return response.value
