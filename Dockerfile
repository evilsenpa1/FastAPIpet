FROM python:3.12-slim

WORKDIR /app

# Create non-root user before copying any files
RUN useradd -m -u 1000 appuser

# Dependencies in a separate layer for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh && \
    mkdir -p /app/uploads && \
    chown -R appuser:appuser /app/uploads

# Drop root privileges
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')" || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]