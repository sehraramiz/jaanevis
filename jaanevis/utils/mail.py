import logging
import sys

import emails

if __name__ == "__main__":
    sys.path = ["", ".."] + sys.path[1:]

from jaanevis.config import settings

logger = logging.getLogger(__name__)


def send_email(email_to: str, text: str, subject: str) -> None:
    message = emails.Message(
        subject=subject,
        text=text,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    environment = {
        "project_name": settings.PROJECT_NAME,
        "email": email_to,
    }
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logger.info(f"email send response {response}")

    return True


if __name__ == "__main__":
    send_email(
        email_to=settings.SMTP_USER,
        text="activate",
        subject="Account Activation",
    )
