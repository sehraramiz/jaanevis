"""serializing note model object to geojson features"""

from jaanevis.domain import geojson as geo
from jaanevis.domain import note as n


def notes_to_geojson(notes: list[n.Note]) -> list[dict]:
    """convert note model list to list of geojson features"""

    geojson_notes = []
    for note in notes:
        geojson_notes.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [note.long, note.lat],
                },
                "properties": {
                    "code": note.code,
                    "creator": note.creator,
                    "text": note.text,
                    "country": note.country,
                    "url": note.url,
                },
            }
        )
    return geojson_notes


def notes_to_geojson_features(
    notes: list[n.Note],
) -> list[n.NoteGeoJsonFeature]:
    """convert note model list to note geojson feature model list"""

    geojson_notes = []
    for note in notes:
        properties = n.NoteGeoJsonProperties(
            url=note.url,
            creator=note.creator,
            text=note.text,
            code=note.code,
            country=note.country,
        )
        geometry = geo.GeoJsonPoint(coordinates=[note.long, note.lat])
        geojson_notes.append(
            n.NoteGeoJsonFeature(geometry=geometry, properties=properties)
        )
    return geojson_notes
