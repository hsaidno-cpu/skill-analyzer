FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    PORT=8080

WORKDIR /app

COPY requirements-cloud.txt ./requirements-cloud.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-cloud.txt

COPY . .

RUN useradd --create-home --uid 10001 gateway \
    && chown -R gateway:gateway /app

USER gateway

EXPOSE 8080

CMD ["uvicorn", "service.app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1", "--no-access-log"]
