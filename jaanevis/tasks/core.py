from redis import Redis
from rq import Queue, Worker

from jaanevis.config import settings

redis_connection = Redis(
    host=settings.REDIS_DSN.host,
    port=settings.REDIS_DSN.port,
)
q = Queue(connection=redis_connection)
w = Worker([q], connection=redis_connection)


def run_worker() -> None:
    w.work()


def send_test_email() -> None:
    from jaanevis.utils.mail import send_email

    q.enqueue(
        send_email,
        email_to=settings.SMTP_USER,
        text="test",
        subject="test",
    )


if __name__ == "__main__":
    run_worker()
    # send_test_email()
