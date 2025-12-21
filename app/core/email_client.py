import smtplib
from app.core.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, EMAIL_FROM

def send_email(to, subject, body):
    # Используется любой SMTP-клиент (например, email.message, yagmail, aiosmtplib)
    pass  # Вместо этого импортировать и реализовать отправку

def send_auto_reply(ticket):
    send_email(
        to=ticket.user_email,
        subject="Ваше обращение принято!",
        body=f"Обращение по теме «{ticket.subject}» зарегистрировано. Скоро с вами свяжется оператор."
    )

def send_operator_reply(ticket, message):
    send_email(
        to=ticket.user_email,
        subject=f"Ответ по обращению «{ticket.subject}»",
        body=message.body
    )

def send_resolved_notification(ticket):
    send_email(
        to=ticket.user_email,
        subject=f"Обращение «{ticket.subject}» закрыто",
        body="Ваша проблема решена. Спасибо за обращение!"
    )
