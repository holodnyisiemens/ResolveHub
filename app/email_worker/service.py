import email
import imaplib
import time
from email.header import decode_header
from email.utils import parseaddr

import requests
from bs4 import BeautifulSoup

from app.core.config import settings
from app.email_worker.sender import (
    send_autoreply_error_creating_task,
    send_autoreply_task_created,
    send_message_no_folder,
)

FOLDER_NAME = "resolvehub"

# Таймауты перепроверки наличия писем / переподключения по IMAP
check_emails_timeout = 5
reconnect_timeout = 5

# Таймаут проверки наличия папки
folder_retry_timeout = 60


def ensure_folder_selected(mail, folder=FOLDER_NAME):
    """Проверяет наличие папки"""
    status, _ = mail.select(folder)
    if status != "OK":
        raise RuntimeError(f"Folder '{folder}' not found or not accessible")


def fetch_unseen_messages(mail):
    """Возвращает список ID непрочитанных писем в уже выбранной папке"""
    status, data = mail.search(None, "UNSEEN")
    if status != "OK" or not data or not data[0]:
        return []
    return data[0].split()


def decode_header_field(header_value):
    """Декодировка заголовков (Subject, From и т.д.)."""
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
    """Возвращает текст письма, поддерживая text/plain и text/html."""
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
    """Парсим письмо и возвращаем sender, subject, body."""
    msg = email.message_from_bytes(msg_bytes)

    # Парсинг From: имя и email отправителя
    raw_from = msg.get("From")
    _, sender_email = parseaddr(raw_from)
    sender_email = decode_header_field(sender_email)

    # Заголовок Subject
    subject = decode_header_field(msg.get("Subject"))

    body = get_body(msg)

    return sender_email, subject, body


def send_task_to_api(sender, subject, body) -> bool:
    """Отправляем задачу через API"""
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
        print(f"Failed to send task: {e}", flush=True)
        return False


def connect_imap():
    """Подключение к IMAP-серверу."""
    mail = imaplib.IMAP4_SSL(settings.IMAP_HOST, settings.IMAP_PORT, timeout=10)
    mail.login(settings.IMAP_USER, settings.IMAP_PASSWORD.get_secret_value())
    print("IMAP worker started and connected", flush=True)
    return mail


def handle_messages(mail, folder, auto_reply_fn=None, need_create_task=False):
    """Обрабатывает все непрочитанные письма в папке"""
    ensure_folder_selected(mail, folder)

    msg_ids = fetch_unseen_messages(mail)

    for msg_id in msg_ids:
        status, msg_data = mail.fetch(msg_id, "(RFC822)")
        if status != "OK" or not msg_data or not msg_data[0]:
            print(f"Failed to fetch message {msg_id}, skipping...", flush=True)
            continue

        sender, subject, body = parse_message(msg_data[0][1])
        print(f"\nNew email from: {sender} in folder '{folder}'", flush=True)
        print(f"Subject: {subject}", flush=True)

        if need_create_task:
            created = send_task_to_api(sender, subject, body)
            if created and auto_reply_fn:
                auto_reply_fn(sender, subject, body)
            elif not created:
                send_autoreply_error_creating_task(sender, subject, body)
        elif auto_reply_fn:
            auto_reply_fn(sender, subject, body)

        mail.store(msg_id, "+FLAGS", "\\Seen")

    return True


def main():
    mail = connect_imap()
    no_folder_message_sent = False

    while True:
        try:
            try:
                # Обработка resolvehub
                handle_messages(
                    mail,
                    folder=FOLDER_NAME,
                    auto_reply_fn=send_autoreply_task_created,
                    need_create_task=True,
                )
                # Обработка INBOX
                handle_messages(
                    mail,
                    folder="INBOX",
                    auto_reply_fn=send_autoreply_error_creating_task,
                    need_create_task=False,
                )
                no_folder_message_sent = False

            except RuntimeError as e:
                print(f"Folder error: {e}", flush=True)
                if not no_folder_message_sent:
                    send_message_no_folder()
                    no_folder_message_sent = True
                try:
                    mail.logout()
                except Exception:
                    pass
                time.sleep(folder_retry_timeout)
                mail = connect_imap()
                continue

            time.sleep(check_emails_timeout)

        except (imaplib.IMAP4.abort, imaplib.IMAP4.error) as e:
            print(f"IMAP error: {e}, reconnecting...", flush=True)
            try:
                mail.logout()
            except Exception:
                pass
            time.sleep(reconnect_timeout)
            mail = connect_imap()

        except Exception as e:
            print(f"Unexpected error: {e}", flush=True)
            time.sleep(check_emails_timeout)
