FROM python:3.14.7-slim
WORKDIR /app
COPY requirements.lock pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.lock \
    && python -m pip install --no-cache-dir --no-deps .
COPY examples ./examples
USER 65532:65532
CMD ["ha-scenario", "run", "examples/presence_timeout.json"]
