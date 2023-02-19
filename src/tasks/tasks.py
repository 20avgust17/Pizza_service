import os

import smtplib
from email.message import EmailMessage

from celery import Celery
from dotenv import load_dotenv

load_dotenv("../../.env")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

SMTP_PASSWORD = "cwmplzttisrwrkhd"
SMTP_USER = "ladinkodima@gmail.com"


def send_email_order_create(username: str, email_address: str):
    email = EmailMessage()
    email["Subject"] = 'Pizza'
    email["From"] = SMTP_USER
    email["To"] = email_address

    email.set_content(
        '<div>'
        f'<h1 style="color: black;">Здравствуйте, {username}, спасибо за заказ! Зацените  нашу пиццу 😊</h1>'
        '<p>Мы очень рады, что довеярете нашему сервису, уверены, что вам точно понравится пицца, приятного аппетита!'
        '</div>',
        subtype='html'
    )
    return email


def send_email_create_user(username: str, email_address: str):
    email = EmailMessage()
    email["Subject"] = 'Pizza'
    email["From"] = SMTP_USER
    email["To"] = email_address

    email.set_content(
        '<div>'
        f'<h1 style="color: black;">Здравствуйте, {username}, спасибо за регистрацию! Зацените  нашу пиццу 😊</h1>'
        '<p>Мы очень рады, что вы зарегистрировали на нашем сервисе, теперь вы сможете сделать заказ '
        'самой вкусной пиццы в вашем городе, рекомендую сделать заказ уже сейчас'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_order(username: str, email_address: str):
    email = send_email_order_create(username, email_address)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email, email_address)


@celery.task
def send_email_user_add(username: str, email_address: str):
    email = send_email_create_user(username, email_address)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email, email_address)
