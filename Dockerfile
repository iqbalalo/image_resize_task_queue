FROM python:3.7

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
WORKDIR /app/src
EXPOSE 5000
ENTRYPOINT [ "gunicorn" ]
CMD ["--bind", "0.0.0.0:5000", "wsgi:app"]
