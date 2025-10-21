FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app
ENV PYTHONPATH=/app

COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt

COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini

COPY ./scripts /app/scripts

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
