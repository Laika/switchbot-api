FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libglib2.0-dev \
  libbluetooth-dev \
  curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false

COPY . /app/

RUN poetry install

CMD ["poetry", "run", "python", "src/api.py"]
