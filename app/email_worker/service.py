import email
import imaplib
import time
from email.header import decode_header
from email.utils import parseaddr

import requests
from bs4 import BeautifulSoup

from app.core.config import settings
from app.email_worker.sender import (
    send_autoreply_task_created,
    send_autoreply_create_folder,
)


def fetch_unseen_messages(mail):
    """
    Получаем список непрочитанных писем из папки ResolveHub.

    Возвращает:
    - None  -> папка не найдена/не выбралась;
    - list  -> список id писем (bytes).
    """
    status, _ = mail.select("ResolveHub")  # имя папки чувствительно к регистру
    if status != "OK":
        # Папка отсутствует или недоступна
        return None

    status, data = mail.search(None, "UNSEEN")
    if status != "OK":
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
    """Отправляем задачу через HTTP API."""
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
    """Подключение к IMAP-серверу."""
    mail = imaplib.IMAP4_SSL(settings.IMAP_HOST, settings.IMAP_PORT, timeout=10)
    mail.login(settings.IMAP_USER, settings.IMAP_PASSWORD.get_secret_value())
    print("IMAP worker started and connected")
    return mail


def process_mails():
    """
    Основной цикл обработки:
    - читает только папку ResolveHub;
    - если папки нет, отправляет письмо владельцу и ждёт;
    - создаёт задачи через API и шлёт автоответ отправителю.
    """
    mail = connect_imap()
    folder_warning_sent = False  # чтобы не спамить инструкциями

    while True:
        try:
            msg_ids = fetch_unseen_messages(mail)

            # Папка не найдена
            if msg_ids is None:
                if not folder_warning_sent:
                    print(
                        "Папка ResolveHub не найдена. "
                        "Отправляем владельцу ящика инструкцию.",
                        flush=True,
                    )
                    # письмо отправляем на IMAP_USER – это владелец ящика
                    send_autoreply_create_folder(to_email=settings.IMAP_USER)
                    folder_warning_sent = True

                # ждём, пока пользователь создаст папку
                time.sleep(30)
                continue

            # Папка появилась — можно снова отправлять задачи и автоответы
            if folder_warning_sent:
                print("Папка ResolveHub обнаружена, продолжаем обработку писем.", flush=True)
            folder_warning_sent = False

            for msg_id in msg_ids:
                _, msg_data = mail.fetch(msg_id, "(RFC822)")
                sender, subject, body = parse_message(msg_data[0][1])

                print(f"\nNew email from: {sender}", flush=True)
                print(f"Subject: {subject}", flush=True)

                created = send_task_to_api(sender, subject, body)
                if created:
                    # Отправка автоответа отправителю письма
                    send_autoreply_task_created(
                        to_email=sender,
                        subject=subject,
                        body=body,
                    )

                # Помечаем письмо как прочитанное
                mail.store(msg_id, "+FLAGS", "\\Seen")

            time.sleep(5)

        except imaplib.IMAP4.error as e:
            print(f"IMAP error: {e}. Reconnecting...", flush=True)
            time.sleep(5)
            mail = connect_imap()

        except Exception as e:
            print(f"Unexpected error: {e}", flush=True)
            time.sleep(5)
