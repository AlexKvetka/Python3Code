from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename
import logs_init_code
import smtplib
import static_code

def send_mail(send_from, password, send_to, subject, text, att_path):
    """
    Sends an email with optional attachment.

    Args:
        send_from (str): Sender's email address.
        password (str): Sender's email password.
        send_to (str): Recipient's email address.
        subject (str): Email subject.
        text (str): Email body text.
        att_path (str): Path to the attachment file (optional).

    Returns:
        None

    Raises:
        smtplib.SMTPException: If there's an issue sending the email.

    Example:
        send_mail("sender@example.com", "password123", "recipient@example.com",
                  "Important Report", "Please find attached the report.", "/path/to/report.pdf")
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    if att_path:
        with open(att_path, "rb") as file:
            part = MIMEApplication(file.read(), Name=basename(att_path))
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(att_path))
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)
        server.ehlo()
        server.starttls()
        server.login(send_from, password)
        server.sendmail(send_from, send_to, msg.as_string())
        server.close()
        logs_init_code.backend_logger.debug(f"Message to {send_to} has been successfully sent!")
    except Exception as e:
        static_code.is_no_exeptions = False
        logs_init_code.backend_logger.critical(f"Could not send e-mail to {send_to} Exception {e}")
