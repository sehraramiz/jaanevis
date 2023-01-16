import json


class NoteJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "code": str(o.code),
                "creator": o.creator,
                "country": o.country,
                "url": o.url,
                "lat": o.lat,
                "long": o.long,
            }
            return to_serialize
        except AttributeError:
            return super().default(0)


class NoteGeoJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "type": "Feature",
                "coordinates": [o.long, o.lat],
                "properties": {
                    "code": str(o.code),
                    "creator": o.creator,
                    "country": o.country,
                    "url": o.url,
                },
            }
            return to_serialize
        except AttributeError:
            return super().default(0)
