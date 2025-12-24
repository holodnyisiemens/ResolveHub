import email
import imaplib
import os
import time
from email.header import decode_header

IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_PORT = int(os.getenv("IMAP_PORT"))
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")


def print_subject(msg):
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8", errors="ignore")
    print("New email with subject:", subject)


def main():
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(IMAP_USER, IMAP_PASSWORD)

    print("Waiting for new emails...")

    while True:
        try:
            # Выбираем папку входящих
            mail.select("INBOX")

            # Смотрим непрочитанные
            _, response = mail.search(None, "UNSEEN")

            if response[0]:
                new_ids = response[0].split()

                for msg_id in new_ids:
                    _, data = mail.fetch(msg_id, "(RFC822)")

                    if data and data[0]:
                        msg = email.message_from_bytes(data[0][1])
                        print_subject(msg)

                    # Помечаем как прочитанное
                    mail.store(msg_id, "+FLAGS", "\\Seen")

            time.sleep(5)

        except KeyboardInterrupt:
            print("\nStopping...")
            break
        except Exception as e:
            print(f"Error: {e}")
            # Переподключение при ошибке
            try:
                mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
                mail.login(IMAP_USER, IMAP_PASSWORD)
            except:
                time.sleep(30)


if __name__ == "__main__":
    main()
