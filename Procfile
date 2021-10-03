release: python manage.py migrate --no-input
worker: python manage.py rqworker high & python manage.py rqscheduler --queue default
web: gunicorn symptoms_tracker.wsgi