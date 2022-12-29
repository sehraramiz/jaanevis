import sys
import uuid

sys.path = ["", ".."] + sys.path[1:]

from geonotes.repository import memrepo as mr
from geonotes.requests import note_list_request as req
from geonotes.usecases import note_list as uc

note_1 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/1",
    "lat": 1,
    "long": 1,
}

note_2 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/2",
    "lat": 2,
    "long": 2,
}

note_3 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/3",
    "lat": 1,
    "long": 1,
}

note_4 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/4",
    "lat": 4,
    "long": 4,
}

if __name__ == "__main__":
    qrystr_params = {"filters": {}}

    request_obj = req.NoteListRequest.from_dict(qrystr_params)

    repo = mr.MemRepo([note_1, note_2, note_3, note_4])
    usecase = uc.NoteListUseCase(repo)
    response = usecase.execute(request_obj)
    print(response.value)
