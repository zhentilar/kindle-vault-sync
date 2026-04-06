from __future__ import annotations

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def send_attachment(
    smtp_host: str,
    smtp_port: int,
    sender_email: str,
    sender_password: str,
    target_email: str,
    subject: str,
    attachment_path: Path,
) -> None:
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = target_email

    with attachment_path.open("rb") as handle:
        part = MIMEApplication(handle.read(), Name=attachment_path.name)

    part["Content-Disposition"] = f'attachment; filename="{attachment_path.name}"'
    msg.attach(part)

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, target_email, msg.as_string())
