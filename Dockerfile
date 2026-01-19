FROM python:3.11-slim

WORKDIR /ceps

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFERRED=1

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
 
EXPOSE 8000

CMD python manage.py migrate && \
    uwsgi --http :8000 --module corewsgi --chmod-socket=666
