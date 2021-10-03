release: python manage.py migrate --no-input
rqworker: python manage.py rqworker high
rqscheduler: python manage.py rqscheduler
web: gunicorn symptoms_tracker.wsgi