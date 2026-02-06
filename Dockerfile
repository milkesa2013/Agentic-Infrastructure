# Project Chimera - Multi-stage Docker build
# Stage 1: Dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv for fast Python package management
RUN pip install uv==0.1.35

# Copy pyproject.toml and install dependencies
COPY pyproject.toml uv.lock* ./
RUN uv pip install --system --no-dev --frozen --out /app/wheels . || true

# Install dev dependencies for testing
COPY pyproject.toml uv.lock* ./
RUN uv pip install --system --dev --frozen --out /app/wheels . || true

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed wheels from builder
COPY --from=builder /app/wheels /app/wheels

# Install packages from wheels
RUN pip install --no-index --find-links /app/wheels \
    pydantic>=2.0.0 \
    httpx>=0.27.0 \
    && rm -rf /app/wheels

# Copy source code
COPY --from=builder /app/src /app/src

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash chimera
USER chimera

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Default command
CMD ["python", "-m", "chimera.cli"]
