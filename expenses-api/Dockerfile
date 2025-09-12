FROM python:3-slim

# Add build dependencies, for the cryptography package
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD [ "fastapi", "run", "main.py", "--port", "52", "--host", "0.0.0.0" ]
