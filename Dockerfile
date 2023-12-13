FROM nikolaik/python-nodejs:python3.11-nodejs18-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV PATH="$PATH:/usr/bin/node"

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*  \
    && rm -rf /tmp/*

# Install python dependencies
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev --no-root

RUN mkdir /app
WORKDIR /app

# Copy all contents
COPY . ./

# Install node dependencies and build the index.ts file to dist/index.js
RUN npm install
RUN npm run build

# run app
CMD ["python", "doxxcaster/bot/main.py"]