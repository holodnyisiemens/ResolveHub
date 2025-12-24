import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from config import settings

TEMPLATES_DIR = Path(__file__).parent / "templates"


def send_autoreply_task_created(to_email: str, subject: str, body: str) -> None:
    """Отправляет автоответ пользователю после создания задачи"""
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

    template_path = TEMPLATES_DIR / "task_created.txt"
    template = template_path.read_text(encoding="utf-8")

    body_preview = body[:300] + ("..." if len(body) > 300 else "")
    message_text = template.replace("{{ subject }}", subject).replace(
        "{{ body_preview }}", body_preview
    )

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = f"Re: {subject}"
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
