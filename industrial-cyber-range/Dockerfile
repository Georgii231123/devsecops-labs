FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --uid 10001 --create-home otlab
COPY --chown=otlab:otlab . .
USER 10001

CMD ["python", "-m", "otlab.protocols.modbus_server"]
