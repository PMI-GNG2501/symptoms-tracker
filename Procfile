release: python manage.py migrate --no-input
worker: python manage.py rqworker high
worker: python manage.py rqscheduler
web: gunicorn symptoms_tracker.wsgi