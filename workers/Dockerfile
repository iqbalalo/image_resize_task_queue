FROM python:3.7
RUN pip install rq redis Pillow
WORKDIR /app/src
CMD rq worker --url redis://redis