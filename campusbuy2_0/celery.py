import os
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusbuy2_0.settings')
app = Celery('campusbuy2_0')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task
def send_welcome_mail(is_merchant=False, **data):
    """
    send welcome email to new users
    """

    name = data.get("name")
    email = data.get("email")

    if is_merchant:

        try:
            send_mail("Welcome to the CampusBuy Family",
                      f"Hi {name}, you've taken the first step in making your business grow exponentially. Well done",
                      "welcome@campusbuy.online", [f'{email}'])
            print("email sent ================================")
            return {"status": "success"}
        except Exception as e:
            print("email not sent ================================")
            print(f"An exception occurred ====> {e}")
            return {"status": "fail"}

    else:
        try:
            send_mail("Welcome to the CampusBuy Family",
                      f"Hi {name}, You've chosen comfort over hardship, welcome to the campusbuy family.",
                      "welcome@campusbuy.online", [f'{email}'])
            print("email sent ================================")
            return {"status": "success"}
        except Exception as e:
            print("email not sent ================================")
            print(f"An exception occurred ====> {e}")
            return {"status": "fail"}


