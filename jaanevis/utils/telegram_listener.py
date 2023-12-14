from jaanevis.tasks.core import q

from .event import subscribe
from .telegram import send_message_to_channel


def handle_new_note_add_event(note):
    msg = """
    .\n
    creator: {creator}\n
    country: {country}\n
    latitude: {lat}\n
    longitude: {long}\n
    url: <a href="{url}">{url}</a>\n
    text: {text}\n
    """.format(
        creator=note.creator,
        country=note.country,
        url=note.url,
        text=note.text,
        lat=note.lat,
        long=note.long,
    )

    q.enqueue(send_message_to_channel, msg)


def setup_note_add_event_handlers():
    subscribe("note_added", handle_new_note_add_event)
