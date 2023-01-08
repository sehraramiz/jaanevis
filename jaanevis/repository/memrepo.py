import json
import pathlib
from typing import Optional

from jaanevis.domain import note as n


class MemRepo:
    def __init__(self, data: list[dict] = []) -> None:
        if data:
            self.data = data
        else:
            self.data = self._read_data_from_file()

    def _read_data_from_file(self) -> Optional[list[dict]]:
        if not pathlib.Path("db.json").is_file():
            return []

        with open("db.json", "r") as db:
            data = json.load(db)
            return data

    def _write_data_to_file(self) -> None:
        with open("db.json", "w") as db:
            db.write(json.dumps(self.data))

    def list(self, filters: dict = None) -> list[n.Note]:
        result = [n.Note.from_dict(d) for d in self.data["notes"]]

        if filters is None:
            return result

        if "code__eq" in filters:
            result = [r for r in result if str(r.code) == filters["code__eq"]]

        if "url__eq" in filters:
            result = [r for r in result if r.url == filters["url__eq"]]

        if "lat__eq" in filters:
            result = [r for r in result if r.lat == filters["lat__eq"]]

        if "long__eq" in filters:
            result = [r for r in result if r.long == filters["long__eq"]]

        return result

    def add(self, note: n.Note) -> None:
        self.data["notes"].append(note.to_dict())
        self._write_data_to_file()

    def get_by_code(self, code: str) -> Optional[n.Note]:
        for note in self.data["notes"]:
            if note["code"] == code:
                return n.Note.from_dict(note)
        return None

    def delete_by_code(self, code: str) -> Optional[n.Note]:
        note = None
        for index, note in enumerate(self.data["notes"]):
            if note["code"] == code:
                note = n.Note.from_dict(self.data["notes"].pop(index))
                break
        self._write_data_to_file()
        return note

    def update(self, obj: n.Note, data: str) -> n.Note:
        updated_note = obj
        for _index, note in enumerate(self.data["notes"]):
            if note["code"] == str(obj.code):
                for field in data:
                    note[field] = data[field]
                updated_note = n.Note.from_dict(note)
                break
        self._write_data_to_file()
        return updated_note
