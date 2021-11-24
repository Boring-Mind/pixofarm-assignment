FROM python:3.10-slim as compile_step

# Don't forget to use Docker BuildKit technology
# https://docs.docker.com/develop/develop-images/build_enhancements/
RUN apt-get update && apt-get install -y gcc g++

# Make a folder where our built packages would be
RUN mkdir -p /build/wheels

# Convert our dependencies from poetry to pip format
COPY backend/pyproject.toml ./backend/poetry.lock* /
RUN pip3 install -U pip wheel poetry
RUN poetry export -f requirements.txt --without-hashes -o /tmp/requirements.txt

# Compile all our dependencies into one wheel
RUN pip3 wheel --wheel-dir=/build/wheels -r /tmp/requirements.txt

FROM python:3.10-slim as run_step

# Import compiled python dependencies from previous step
COPY --from=compile_step /build/wheels /tmp/wheels

# Install python dependencies
RUN pip3 install -U pip wheel
RUN pip3 install --no-cache-dir /tmp/wheels/* && rm -rf /tmp/wheels

WORKDIR /app

COPY ./backend /app

CMD ["python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]