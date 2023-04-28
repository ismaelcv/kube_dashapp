FROM python:3.11.2


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV APP_DIR="/app"
ENV POETRY_VERSION=1.4.2
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8


WORKDIR ${APP_DIR}/

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./


# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Creating folders, and files for a project:
COPY . .

# Install the code as a package
RUN  poetry install --only-root

EXPOSE 8094

# Run your app
CMD ["gunicorn", "--bind", "0.0.0.0:8094", "dashapp_skeleton.apps.simple_dashapp:server"]
