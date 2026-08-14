FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --system --gid 10001 app && \
    useradd --system --uid 10001 --gid app --home-dir /app app

WORKDIR /app
COPY --chown=app:app app ./app

USER 10001:10001
EXPOSE 8080

CMD ["python", "-m", "app.main"]
