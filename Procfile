web: gunicorn BlogApp.wsgi
web: daphne BlogApp.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker --settings=BlogApp.settings -v2