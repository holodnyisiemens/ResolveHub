import email
import imaplib
import time
from email.header import decode_header
from email.utils import parseaddr

import requests
from bs4 import BeautifulSoup

from app.core.config import settings
from app.email_worker.sender import send_autoreply_task_created


def fetch_unseen_messages(mail):
    """Получаем список непрочитанных писем"""
    mail.select("INBOX")
    _, data = mail.search(None, "UNSEEN")
    return data[0].split()


def decode_header_field(header_value):
    """Декодировка заголовков (Subject, From и т.д.)"""
    if not header_value:
        return ""
    decoded_parts = decode_header(header_value)
    parts = []
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            parts.append(part.decode(encoding or "utf-8", errors="ignore"))
        else:
            parts.append(part)
    return "".join(parts)


def get_body(msg):
    """Возвращает текст письма, поддерживая text/plain и text/html"""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and not part.get_filename():
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="ignore")
            elif part.get_content_type() == "text/html" and not part.get_filename():
                charset = part.get_content_charset() or "utf-8"
                html = part.get_payload(decode=True).decode(charset, errors="ignore")
                return BeautifulSoup(html, "html.parser").get_text()
    else:
        charset = msg.get_content_charset() or "utf-8"
        payload = msg.get_payload(decode=True).decode(charset, errors="ignore")
        if msg.get_content_type() == "text/html":
            return BeautifulSoup(payload, "html.parser").get_text()
        return payload


def parse_message(msg_bytes):
    """Парсим письмо и возвращаем sender, subject, body"""
    msg = email.message_from_bytes(msg_bytes)

    # Парсинг заголовка From: имя и email отправителя
    raw_from = msg.get("From")
    _, sender_email = parseaddr(raw_from)
    sender_email = decode_header_field(sender_email)

    # Получаем заголовок Subject
    subject = decode_header_field(msg.get("Subject"))

    body = get_body(msg)

    return sender_email, subject, body


def send_task_to_api(sender, subject, body) -> bool:
    """Отправляем задачу через HTTP API"""
    try:
        response = requests.post(
            f"{settings.API_URL}/tasks",
            json={
                "title": subject,
                "description": body,
                "creator_email": sender,
            },
            timeout=10,
        )
        response.raise_for_status()
        return True

    except requests.RequestException as e:
        print(f"Failed to send task: {e}")
        return False


def connect_imap():
    mail = imaplib.IMAP4_SSL(settings.IMAP_HOST, settings.IMAP_PORT, timeout=10)
    mail.login(settings.IMAP_USER, settings.IMAP_PASSWORD.get_secret_value())
    print("IMAP worker started and connected")
    return mail


def process_mails():
    mail = connect_imap()

    while True:
        try:
            for msg_id in fetch_unseen_messages(mail):
                _, msg_data = mail.fetch(msg_id, "(RFC822)")
                sender, subject, body = parse_message(msg_data[0][1])

                print(f"\nNew email from: {sender}")
                print(f"Subject: {subject}")

                created = send_task_to_api(sender, subject, body)
                if created:
                    # Отправка автоответа
                    send_autoreply_task_created(
                        to_email=sender,
                        subject=subject,
                        body=body,
                    )

                # Пометка письма как прочитанного
                mail.store(msg_id, "+FLAGS", "\\Seen")

            time.sleep(5)

        except imaplib.IMAP4.error as e:
            print(f"IMAP error: {e}. Reconnecting...")
            time.sleep(5)
            mail = connect_imap()

        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)
