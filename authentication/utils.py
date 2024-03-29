from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class Util:

  @staticmethod
  def send_password_reset_email(data):
    """
    Method For Sending Password Reset Email
    """
    try:
        user_email = data['to_email']
        subject = data['subject']
        link=data['link']
        
        # ! For Passing Link As Context To The Template
        context={'link':link}
        message=render_to_string('emails/password_reset.html',context)
        
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email],html_message=message)
         
    except Exception as e:
       print(f"Some Error occrured during sending email {e}")


  @staticmethod
  def send_email_for_changing_email(data):
    """
    Method For Sending Email With A
    Link to Change Email
    """
    try:
        user_email = data['to_email']
        subject = data['subject']
        link=data['link']
        
        # ! For Passing Link As Context To The Template
        context={'link':link}
        message=render_to_string('emails/change_email.html',context)
        
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email],html_message=message)
         
    except Exception as e:
       print(f"Some Error occrured during sending email {e}")
