import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

RECIEVER_EMAIL = os.getenv("EMAIL_FOR_TESTS")
SUBJECT = "TEST_EMAIL"
MESSAGE = "TEST"


def main():
    context = ssl.create_default_context()

    try:
        # Creating the email message
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = RECIEVER_EMAIL
        msg["Subject"] = SUBJECT
        msg.attach(MIMEText(MESSAGE, "plain"))

        # Connecting to the SMTP server using SSL and sending the email
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            print(f"Email successfully sent to: {RECIEVER_EMAIL}")

    except Exception as e:
        print(f"An error occurred while sending email to {RECIEVER_EMAIL}: {e}")


if __name__ == "__main__":
    main()
