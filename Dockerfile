FROM python:3.9

    # Don't periodically check PyPI to determine whether a new version of pip is available for download.
ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    # Disable package cache.
    PIP_NO_CACHE_DIR=off \
    # The python output is sent straight to terminal (e.g. your container log) without being first buffered
    PYTHONUNBUFFERED=on \
    # Prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=on \
    # set workdir as PYTHON PATH
    PYTHONPATH=/code \
    # to run scripts
    PATH="app/scripts:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends build-essential\
    && apt-get autoclean && apt-get autoremove \
    && pip install poetry \
    && poetry config virtualenvs.create false

# don't have to create direcotry with mkdir
WORKDIR /code

# requirements (poetry)
COPY ./poetry.lock poetry.lock
COPY ./pyproject.toml pyproject.toml

RUN poetry install

COPY ./app app
COPY ./Makefile Makefile

COPY ./init_db.py init_db.py

ENTRYPOINT ["entrypoint.sh"]