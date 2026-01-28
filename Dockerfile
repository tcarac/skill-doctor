# Use Python slim image
FROM python:3.14-slim

# Set labels for GitHub Container Registry
LABEL org.opencontainers.image.source="https://github.com/tcarac/skill-doctor"
LABEL org.opencontainers.image.description="Validate Agent Skills against the official specification"
LABEL org.opencontainers.image.licenses="Apache-2.0"

# Install git (needed for changed files detection)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install dependencies
RUN uv sync --frozen --no-dev

# Set Python path
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# Entry point - use the virtual environment's Python directly
ENTRYPOINT ["/app/.venv/bin/python", "-m", "skill_doctor.main"]
