import json


class NoteJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "code": str(o.code),
                "creator": o.creator,
                "url": o.url,
                "lat": o.lat,
                "long": o.long,
            }
            return to_serialize
        except AttributeError:
            return super().default(0)
