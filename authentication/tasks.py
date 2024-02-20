from celery import shared_task
from .utils import Util

    
@shared_task(name="password_reset_email")
def password_reset_task(data):
    """
    Celery task for calling the function which sends
    email password reset email
    """
    try:
        Util.send_password_reset_email(data)
    except Exception as e:
        print(f"An error occurred while running task --> {e}")



@shared_task(name="change_email_task")
def change_email_task(data):
    """
    Celery task for calling the function which sends
    email for changing email
    """
    try:
        Util.send_email_for_changing_email(data)
    except Exception as e:
        print(f"An error occurred while running task --> {e}")
    

