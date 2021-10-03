release: python manage.py migrate --no-input
rqworker: python manage.py rqworker high
rqscheduler: python manage.py rqscheduler --queue high
web: gunicorn symptoms_tracker.wsgi