FROM python:3.14.9-slim@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8
WORKDIR /app
COPY requirements.lock pyproject.toml README.md LICENSE ./
COPY src ./src
COPY tools/check_lock.py ./tools/check_lock.py
RUN python tools/check_lock.py \
    && python -m pip install --no-cache-dir --require-hashes -r requirements.lock \
    && python -m pip install --no-cache-dir --no-deps . \
    && python -m pip check
COPY examples ./examples
USER 65532:65532
CMD ["ha-scenario", "run", "examples/presence_timeout.json"]
