FROM python:3-alpine

LABEL AUTHOR=msirovy@gmail.com
LABEL COMMENT="Flask application using sqlite3"

ENV PORT="5000"
ENV HOST="0.0.0.0"
ENV DB_PATH="/mnt/db-prod.db"
ENV DEBUG="False"


COPY . /app
WORKDIR /app


RUN ls -al; pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]

