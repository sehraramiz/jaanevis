import uuid

note_1 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/1",
    "lat": 29,
    "long": 52,
}

note_2 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/2",
    "lat": 30,
    "long": 52,
}

note_3 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/3",
    "lat": 29,
    "long": 51,
}

note_4 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/4",
    "lat": 29.5,
    "long": 52.5,
}

note_dicts = [note_1, note_2, note_3, note_4]
