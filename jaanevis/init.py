"""setup initial data and check the requirements"""

from rq import Worker

from jaanevis.tasks.core import q, redis_connection


def check_task_worker() -> None:
    workers = Worker.all(queue=q)
    if not workers:
        raise Exception("no rq workers are running")


def check_redis() -> None:
    if not redis_connection.ping():
        raise Exception("redis is not connected")


def check_initial_setup():
    check_task_worker()
    check_redis()


if __name__ == "__main__":
    check_initial_setup()
