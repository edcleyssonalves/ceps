FROM python:3.11

WORKDIR /ceps

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60 --preload
