FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app ./app

EXPOSE 8000

RUN chmod +x ./prestart.sh

CMD ["./boot/alembic_script.sh", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]