from jaanevis.config import settings
from jaanevis.i18n import gettext as _
from jaanevis.tasks.core import q

from .event import subscribe
from .mail import send_email


def handle_user_registered_event(data):
    email = data["email"]
    username = data["username"]
    token = data["activation_token"]

    activation_params = f"username={username}&token={token}"
    activation_url = "{}{}/user/activate?{}".format(
        settings.PROJECT_URL, settings.API_V1_STR, activation_params
    )
    mail_text = f"visit this link to activate your account {activation_url}"
    mail_subject = _("Jaanevis Account Activation")
    q.enqueue(
        send_email,
        email_to=email,
        text=mail_text,
        subject=mail_subject,
    )


def setup_email_event_handlers():
    subscribe("user_registered", handle_user_registered_event)
