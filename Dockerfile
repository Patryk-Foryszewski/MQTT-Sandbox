FROM python:3.8

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.13

# syntax=docker/dockerfile:1

WORKDIR /app

# COPY ["/mqtt/", "light_tower.py", "live_stream.py", "poetry.lock", "pyproject.toml"] ./

RUN apt-get update \
    && apt-get --yes install apt-utils \
    && apt-get --yes install curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
# install dependencies
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi


COPY . .

# Installing Poetry (1.1.13)
# Installing Poetry (1.1.13): Creating environment
# Installing Poetry (1.1.13): Installing Poetry
# Installing Poetry (1.1.13): Creating script
# Installing Poetry (1.1.13): Done
#
# Poetry (1.1.13) is installed now. Great!
#
# To get started you need Poetry's bin directory (/root/.local/bin) in your `PATH`
# environment variable.
#
# Add `export PATH="/root/.local/bin:$PATH"` to your shell configuration file.
#
# Alternatively, you can call Poetry explicitly with `/root/.local/bin/poetry`.
#
# You can test that everything is set up by executing:
#
# `poetry --version`



