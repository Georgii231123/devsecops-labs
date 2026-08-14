FROM python:3.13-alpine

RUN addgroup -S app && adduser -S -G app -u 10001 app
WORKDIR /app
COPY app.py .
USER 10001:10001
EXPOSE 8000
CMD ["python", "app.py"]
