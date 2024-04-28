# Copyright 2023 Enersense PN Oy
# This file is subject to the terms and conditions of the MIT License.  
# See LICENSE file in the top-level directory

# Energy Meter application
# ----------------------------

FROM python:3.12.0-slim-bullseye


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
# httptools doesn't have wheel files published on PyPI, only source files, 
# so install g++ prior to installing fastapi[all], and remove it later.
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        g++ \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove g++ \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /requirements.txt

WORKDIR /app
COPY . /app


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# build executable
#ENTRYPOINT ["python3","-u","./example-app/main.py"]
CMD ["sleep", "infinity"]
#CMD ["python3","-u","./main.py"]
