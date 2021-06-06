FROM python:3.9-slim

WORKDIR code
COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

COPY . ./

EXPOSE 80

#CMD poetry run uvicorn --host=0.0.0.0 app.main:app