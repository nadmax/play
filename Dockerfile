FROM python:3.14-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:0.10.5 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen --no-cache --no-install-project
COPY src/ src/
RUN uv sync --no-dev --frozen --no-cache --no-editable

FROM python:3.14-alpine AS final
ENV PATH="/app/.venv/bin:$PATH"
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --chown=appuser:appgroup --from=builder /app/.venv .venv
USER appuser
ENTRYPOINT ["uvicorn", "play:app", "--host", "0.0.0.0", "--port", "8080"]
