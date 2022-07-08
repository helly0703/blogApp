web: gunicorn BlogApp.wsgi
daphne BlogApp.asgi:application
daphne -b 0.0.0.0 -p 8001 BlogApp.asgi:application