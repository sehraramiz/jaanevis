from fastapi import FastAPI

from geonotes.domain import note as n
from geonotes.repository import memrepo as mr
from geonotes.requests.add_note_request import AddNoteRequest
from geonotes.requests.note_list_request import NoteListRequest
from geonotes.serializers import note_geojson_serializer as geo_serializer
from geonotes.usecases import add_note, note_list

from .sample_data import note_dicts

app = FastAPI()


@app.get("/note", response_model=list[n.Note])
def read_notes() -> list[n.Note]:
    """read notes"""

    repo = mr.MemRepo(note_dicts)

    note_list_usecase = note_list.NoteListUseCase(repo)
    request_obj = NoteListRequest(filters={})
    response = note_list_usecase.execute(request_obj)

    return response.value


@app.get("/note/geojson", response_model=list[n.NoteGeoJsonFeature])
def read_notes_geojson() -> list[n.NoteGeoJsonFeature]:
    """read notes as geojson feature objects"""

    repo = mr.MemRepo(note_dicts)

    note_list_usecase = note_list.NoteListUseCase(repo)
    request_obj = NoteListRequest(filters={})
    response = note_list_usecase.execute(request_obj)
    geojson_response = geo_serializer.notes_to_geojson_features(response.value)

    return geojson_response


@app.post("/note", response_model=n.Note)
def create_note(note_in: n.NoteCreateApi) -> n.Note:
    """add new note"""

    note = n.Note(**note_in.dict(), creator="default")
    repo = mr.MemRepo(note_dicts)

    add_note_usecase = add_note.AddNoteUseCase(repo)
    request_obj = AddNoteRequest(note)
    response = add_note_usecase.execute(request_obj)

    return response.value
