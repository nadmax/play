FROM python:3.14-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:0.10.5 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen --no-cache --no-install-project
COPY src/ src/
RUN uv build --wheel && \
    uv pip install dist/*.whl

FROM python:3.14-alpine AS final
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY --from=builder /app/.venv .venv
ENTRYPOINT ["uvicorn", "play.main:app", "--host", "0.0.0.0"]
CMD ["--port", "8080"]
