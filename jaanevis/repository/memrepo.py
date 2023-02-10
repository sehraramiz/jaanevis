import json
import os
import pathlib
from typing import Optional

from jaanevis.config import settings
from jaanevis.domain import note as n
from jaanevis.domain import session as s
from jaanevis.domain import user as u


class MemRepo:
    def __init__(self, data: list[dict] = None) -> None:
        base_data_path = settings.DATA_BASE_DIR / "data"
        os.makedirs(base_data_path, exist_ok=True)
        self.db_path = base_data_path / "db.json"
        if data is not None:
            self.data = data
        else:
            self.data = self._read_data_from_file()

    def _read_data_from_file(self) -> Optional[list[dict]]:
        if not pathlib.Path(self.db_path).is_file():
            return {"notes": [], "users": [], "sessions": []}

        with open(self.db_path, "r") as db:
            data = json.load(db)
            return data

    def _write_data_to_file(self) -> None:
        with open(self.db_path, "w") as db:
            db.write(json.dumps(self.data))

    def list(
        self, filters: dict = None, limit: int = None, skip: int = 0
    ) -> list[n.Note]:
        result = [n.Note.from_dict(d) for d in self.data["notes"]]

        if filters is None:
            sorted_notes = sorted(result, key=lambda n: n.created)[::-1]
            if limit:
                return sorted_notes[skip: limit + skip]
            return sorted_notes[skip:]

        if "code__eq" in filters:
            result = [r for r in result if str(r.code) == filters["code__eq"]]

        if "creator__eq" in filters:
            result = [
                r for r in result if str(r.creator) == filters["creator__eq"]
            ]

        if "country__eq" in filters:
            result = [
                r for r in result if str(r.country) == filters["country__eq"]
            ]

        if "url__eq" in filters:
            result = [r for r in result if r.url == filters["url__eq"]]

        if "tag__eq" in filters:
            result = [r for r in result if filters["tag__eq"] in r.tags]

        if "lat__eq" in filters:
            result = [r for r in result if r.lat == filters["lat__eq"]]

        if "long__eq" in filters:
            result = [r for r in result if r.long == filters["long__eq"]]

        sorted_notes = sorted(result, key=lambda n: n.created)[::-1]
        if limit:
            return sorted_notes[skip : limit + skip]
        return sorted_notes[skip:]

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

    def get_user_by_username(self, username: str) -> u.User:
        for user in self.data["users"]:
            if user["username"] == username:
                return u.User.from_dict(user)
        return None

    def create_user(
        self, username: str, password: str, is_active: bool = False
    ) -> u.User:
        user = u.User(
            username=username, password=password, is_active=is_active
        )
        self.data["users"].append(user.to_dict())
        self._write_data_to_file()
        return user

    def update_user(self, obj: u.User, data: str) -> u.User:
        updated_user = obj
        for _index, user in enumerate(self.data["users"]):
            if user["username"] == str(obj.username):
                for field in data:
                    user[field] = data[field]
                updated_user = u.User.from_dict(user)
                break
        self._write_data_to_file()
        return updated_user

    def delete_user(self, username: str) -> bool:
        for index, user in enumerate(self.data["users"]):
            if user["username"] == username:
                del self.data["users"][index]
                break
        self._write_data_to_file()
        return True

    def get_session_by_session_id(self, session_id: str) -> s.Session:
        for session in self.data["sessions"]:
            if session["session_id"] == session_id:
                return s.Session.from_dict(session)
        return None

    def get_session_by_session_id_and_username(
        self, session_id: str, username: str
    ) -> s.Session:
        for session in self.data["sessions"]:
            if (
                session["session_id"] == session_id
                and session["username"] == username
            ):
                return s.Session.from_dict(session)
        return None

    def delete_session_by_session_id(self, session_id: str) -> bool:
        for index, session in enumerate(self.data["sessions"]):
            if session["session_id"] == session_id:
                del self.data["sessions"][index]
                break
        self._write_data_to_file()
        return True

    def create_or_update_session(
        self, username: str, session_id: str, expire_time: float
    ) -> s.Session:
        new_session = s.Session(
            username=username, session_id=session_id, expire_time=expire_time
        )
        for session in self.data["sessions"]:
            if session["username"] == username:
                session["session_id"] = session_id
                break
        else:
            self.data["sessions"].append(new_session.to_dict())
        self._write_data_to_file()
        return new_session

    def create_session(
        self, username: str, session_id: str, expire_time: float
    ) -> s.Session:
        new_session = s.Session(
            username=username, session_id=session_id, expire_time=expire_time
        )
        self.data["sessions"].append(new_session.to_dict())
        self._write_data_to_file()
        return new_session
