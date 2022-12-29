from geonotes.domain import note as n


class MemRepo:
    def __init__(self, data: dict) -> None:
        self.data = data

    def list(self, filters: dict = None) -> list[n.Note]:
        result = [n.Note.from_dict(d) for d in self.data]

        if filters is None:
            return result

        if "code__eq" in filters:
            result = [r for r in result if r.code == filters["code__eq"]]

        if "url__eq" in filters:
            result = [r for r in result if r.url == filters["url__eq"]]

        if "lat__eq" in filters:
            result = [r for r in result if r.lat == filters["lat__eq"]]

        if "long__eq" in filters:
            result = [r for r in result if r.long == filters["long__eq"]]

        return result
