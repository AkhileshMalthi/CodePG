# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock* README.md LICENSE ./
COPY codepg/ codepg/

# Install without dev dependencies
RUN uv sync --frozen --no-dev --no-editable || uv sync --no-dev --no-editable

FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=base /app /app
COPY --from=ghcr.io/astral-sh/uv:0.11.23 /uv /usr/local/bin/uv

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Default playground dir inside container (mount host dir to override)
ENV CODEPG_BASE_DIR=/playgrounds

RUN mkdir -p /playgrounds

ENTRYPOINT ["codepg"]
CMD ["--help"]
