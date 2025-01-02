import logging
from pathlib import Path
from typing import Any, Dict
import emails
from emails.template import JinjaTemplate
from fastapi import BackgroundTasks
from app.main.core.config import Config
from app.main.core.i18n import get_language, __
from app.main.models.db.session import SessionLocal
# from app.main.worker import celery



def send_email(
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment: Dict[str, Any] = {},
        file: Any = []
) -> None:
    assert Config.EMAILS_ENABLED, "aucune configuration fournie pour les variables de messagerie"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(Config.EMAILS_FROM_NAME, Config.EMAILS_FROM_EMAIL)
    )
    for attachment in file:
        message.attach(data=open(attachment, 'rb'), filename=attachment.split("/")[-1])

    smtp_options = {"host": Config.SMTP_HOST, "port": Config.SMTP_PORT}
    if Config.SMTP_TLS:
        smtp_options["tls"] = Config.SMTP_TLS
    if Config.SMTP_SSL:
        smtp_options["ssl"] = Config.SMTP_SSL
    if Config.SMTP_USER:
        smtp_options["user"] = Config.SMTP_USER
    if Config.SMTP_PASSWORD:
        smtp_options["password"] = Config.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"résultat de l'email envoyé: {response}")


def send_test_email(email_to: str) -> None:
    project_name = Config.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(Config.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    task = send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": Config.PROJECT_NAME, "email": email_to},
    )
    logging.info(f"new send mail task with id {task.id}")


def send_reset_password_email(backgroundTasks:BackgroundTasks,email_to: str, token: str, prefered_language: str, name: str,valid_minutes: int) -> None:
    if str(prefered_language) in ["en", "EN", "en-EN"]:
        subject = f"AUTO BOOKING & BUYING & LOCATE APP | Password reset"

        with open(Path(Config.EMAIL_TEMPLATES_DIR) /"en"/"reset_password.html") as f:
            template_str = f.read()
    else:
        subject = f"AUTO BOOKING & BUYING & LOCATE APP | Réinitialisation de mot de passe"

        with open(Path(Config.EMAIL_TEMPLATES_DIR) /"fr"/"reset_password.html") as f:
            template_str = f.read()

    # task = send_email(
    #     email_to=email_to,
    #     subject_template=subject,
    #     html_template=template_str,
    #     environment={
    #         "code": token,
    #         "name": name,
    #         "email": email_to,
    #         "valid_minutes": valid_minutes,
    #     },
    # )

    subject_template=subject
    html_template=template_str
    environment={
        "code": token,
        "name": name,
        "email": email_to,
        "valid_minutes": valid_minutes,
    }

    backgroundTasks.add_task(
        send_email,
        email_to,
        subject_template,
        html_template,
        environment
    )


    # logging.info(f"new send mail task with id {task.id}")