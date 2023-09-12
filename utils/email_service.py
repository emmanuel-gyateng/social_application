import os

from django.core.mail import send_mail

FROM_EMAIL = os.getenv("EMAIL_HOST_USER")
HOST_LINK = os.getenv("VERIFY_HOSTNAME")


def send_email_verification_mail(username, email, token):
    """Sending email service"""
    link = f"{HOST_LINK}accounts/verify-email/?iam={email}&def={token}"
    subject = "Email Verification Link"
    message = f"Hello {username}, \n\n Please use the link below to verify your account\n\n {link}"
    send_mail(subject, message, FROM_EMAIL, [email])


def send_reset_password_email(username, email, token):
    """Sending email service"""
    link = f"{HOST_LINK}accounts/reset-password/confirm/?iam={email}&def={token}"
    subject = "Password Reset Confirmation"
    message = f"Hello {username},\n\n Please use the link below to reset your account password \n\n {link}"
    send_mail(subject, message, FROM_EMAIL, [email])
