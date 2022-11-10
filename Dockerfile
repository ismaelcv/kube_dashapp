FROM python:3.9.12

ENV YOUR_ENV=${MLFLOW_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    APP_DIR="/code" \
    POETRY_VERSION=1.2.2

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR ${APP_DIR}/


COPY poetry.lock pyproject.toml ${APP_DIR}/


# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY dashapp_skeleton ${APP_DIR}/dashapp_skeleton/


EXPOSE 8094

# Install the code as a package
RUN pip install -e ."[dev]"

# Run your app
CMD ["gunicorn", "--bind", "0.0.0.0:8094", "dashapp_skeleton.apps.simple_dashapp:server"]
