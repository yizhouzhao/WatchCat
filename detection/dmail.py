import sendgrid
import os
from sendgrid.helpers.mail import *
import requests

from dotenv import load_dotenv
load_dotenv() 
invoke_url = "https://ai.api.nvidia.com/v1/vlm/adept/fuyu-8b"

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# print("SENDGRID_API_KEY: ", SENDGRID_API_KEY)

def send_email(html_content):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("home@digitalbotlab.com")
    to_email = To("yizhou@digitalbotlab.com")
    subject = "Cat Alert!"
    content = Content("text/html", html_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

def describe_cat_image(image_base64):
    try:
        assert len(image_base64) < 180_000, \
        "To upload larger images, use the assets API (see docs)"

        headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept": "application/json"
        }

        payload = {
        "messages": [
            {
            "role": "user",
            "content": f'Where is the cat and what is he doing? <img src="data:image/png;base64,{image_base64}" />'
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.20,
        "top_p": 0.70,
        "seed": 0,
        "stream": False
        }

        response = requests.post(invoke_url, headers=headers, json=payload)
        print(response.json())

        return str(response.json()["choices"][0]["message"]["content"])

    except Exception as e:
        print(f"[NVIDIA AI FOUNDATION ERROR] An error occurred: {e}")
        return "Cat is just here!"