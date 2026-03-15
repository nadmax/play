FROM python:3.14-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:0.10.5 /uv /usr/local/bin/uv
RUN apk upgrade --no-cache
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-dev --frozen --no-install-project --no-editable

COPY pyproject.toml uv.lock ./
COPY src/ src/
COPY alembic/ alembic/
COPY alembic.ini ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen --no-editable

FROM python:3.14-alpine AS final
ENV PATH="/app/.venv/bin:$PATH"
RUN apk upgrade --no-cache
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --chown=appuser:appgroup --from=builder /app/.venv .venv
COPY --chown=appuser:appgroup --from=builder /app/src src/
COPY --chown=appuser:appgroup --from=builder /app/alembic alembic/
COPY --chown=appuser:appgroup --from=builder /app/alembic.ini .
USER appuser
ENTRYPOINT ["uvicorn", "play:app", "--host", "0.0.0.0", "--port", "8080"]
