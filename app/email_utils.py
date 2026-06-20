import os
import smtplib
from email.message import EmailMessage


def send_password_reset_email(to_email: str, reset_url: str) -> bool:
    server = os.environ.get("MAIL_SERVER")
    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    sender = os.environ.get("MAIL_DEFAULT_SENDER", username)
    port = int(os.environ.get("MAIL_PORT", "587"))

    if not all([server, username, password]):
        print(f"[PetCare] Password reset link for {to_email}: {reset_url}")
        return False

    msg = EmailMessage()
    msg["Subject"] = "PetCare Password Reset"
    msg["From"] = sender
    msg["To"] = to_email
    msg.set_content(
        "Reset your PetCare password using this link (valid for 1 hour):\n\n"
        f"{reset_url}\n\n"
        "If you did not request this, you can ignore this email."
    )

    with smtplib.SMTP(server, port) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)
    return True
