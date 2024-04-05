import sendgrid
import os
from sendgrid.helpers.mail import *

from dotenv import load_dotenv
load_dotenv() 

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# print("SENDGRID_API_KEY: ", SENDGRID_API_KEY)

def send_email():
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("home@digitalbotlab.com")
    to_email = To("yizhou@digitalbotlab.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/html", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)