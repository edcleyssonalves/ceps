FROM python:3.11

WORKDIR /ceps

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFERRED=1

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD python manage.py migrate && \
    gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60 --preload
