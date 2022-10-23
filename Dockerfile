FROM python:3.9.12

ARG MLFLOW_ENV

ENV YOUR_ENV=${MLFLOW_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2


# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /
COPY poetry.lock pyproject.toml /


# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$MLFLOW_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . .

EXPOSE 8050

# Install the code as a package
RUN pip install -e ."[dev]"

# Run your app
CMD [ "python", "./dashapp_skeleton/apps/simple_dashapp.py" ]