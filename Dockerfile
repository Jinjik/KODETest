FROM python:3.9

COPY app/requirements.txt ./requirements.txt
COPY ./app app/

RUN pip3 install -r requirements.txt
WORKDIR app/
RUN alembic revision -m "first migration" && alembic upgrade head
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "15400"]