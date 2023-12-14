FROM python:3.10-rc-bullseye

WORKDIR /app/
RUN pip install fastapi uvicorn
RUN pip install poetry && poetry config virtualenvs.create false
COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry install

COPY jaanevis /app/jaanevis
COPY script /app/script

CMD sh /app/script/fastapi.sh
