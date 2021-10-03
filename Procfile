release: python manage.py migrate --no-input
worker: python manage.py rqworker high & python manage.py rqscheduler --queue high
web: gunicorn symptoms_tracker.wsgi