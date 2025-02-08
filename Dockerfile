# Dockerfile
FROM python:3.10


WORKDIR /app

RUN mkdir -p /app/media
RUN chmod -R 755 /app/media

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

EXPOSE 8000