import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from app.core.config import settings

TEMPLATES_DIR = Path("app") / "templates" / "email"


def send_autoreply(template_file: str, to_email: str, subject: str, body: str) -> None:
    """Отправляет автоответ пользователю по шаблону."""
    if not all(
        [
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            settings.SMTP_USER,
            settings.SMTP_PASSWORD,
        ]
    ):
        print("SMTP настройки отсутствуют, автоответ пропущен", flush=True)
        return

    if to_email == settings.IMAP_USER:
        print(
            f"Пользователю {settings.IMAP_USER} письма не отправляются для избежания цикла",
            flush=True,
        )
        return

    template_path = TEMPLATES_DIR / template_file
    try:
        template = template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Шаблон письма не найден: {template_path}", flush=True)
        return

    body_preview = body[:300] + ("..." if len(body) > 300 else "")
    message_text = template.replace("{{ subject }}", subject).replace(
        "{{ body_preview }}", body_preview
    )

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Reply-To"] = settings.SMTP_USER

    msg.attach(MIMEText(message_text, "plain", "utf-8"))

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            context=context,
            timeout=10,
        ) as server:
            server.login(
                settings.SMTP_USER,
                settings.SMTP_PASSWORD.get_secret_value(),
            )
            server.sendmail(
                settings.SMTP_USER,
                to_email,
                msg.as_string(),
            )

        print(f"Автоответ отправлен: {to_email}", flush=True)

    except Exception as e:
        print(f"Ошибка отправки автоответа {to_email}: {e}", flush=True)


def send_autoreply_task_created(to_email: str, subject: str, body: str) -> None:
    """Автоответ при создании задачи из письма."""
    send_autoreply(
        template_file="task_created.txt",
        to_email=to_email,
        subject=f"Re: {subject}",
        body=body,
    )


def send_autoreply_error_creating_task(to_email: str, subject: str, body: str) -> None:
    """Автоответ при ошибке создания задачи."""
    send_autoreply(
        template_file="error_creating_task.txt",
        to_email=to_email,
        subject=f"Re: {subject}",
        body=body,
    )


def send_autoreply_task_done(to_email: str, subject: str, body: str) -> None:
    """Автоответ при завершении задачи (если понадобится)."""
    send_autoreply(
        template_file="task_done.txt",
        to_email=to_email,
        subject=f"Re: {subject}",
        body=body,
    )


def send_message_no_folder() -> None:
    """Сообщение при отсутсвии папки"""
    send_autoreply(
        template_file="create_folder.txt",
        to_email=settings.IMAP_USER,
        subject="[resolvehub] Internal ResolveHub Error",
        body="",
    )
