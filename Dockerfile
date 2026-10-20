FROM python:3.15.0-slim@sha256:2da676046630d7bf14c6764ae1143dc7fa0377a53f94bf5a642f0b214aca5bce
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
