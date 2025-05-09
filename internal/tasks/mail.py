from fastapi_mail import FastMail, MessageSchema
from internal.core import config
from internal.core.logging import logger
from internal.tasks.task import celery
from fastapi_mail import ConnectionConfig
import asyncio

conf = ConnectionConfig(
    MAIL_USERNAME=config.settings.MAIL_USERNAME,
    MAIL_PASSWORD=config.settings.MAIL_PASSWORD,
    MAIL_FROM=config.settings.MAIL_FROM,
    MAIL_PORT=config.settings.MAIL_PORT,
    MAIL_SERVER=config.settings.MAIL_SERVER,
    MAIL_STARTTLS=config.settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=config.settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=config.settings.USE_CREDENTIALS
)

@celery.task
def send_verification_email(gmail: str, verify_url: str):
    try:
        message = MessageSchema(
            subject="Verify Your Email",
            recipients=[gmail],
            body=f"Click this link to verify your email: {verify_url}",
            subtype="plain"
        )
        fm = FastMail(conf)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fm.send_message(message))
    except Exception as e:
        logger.error(f"send_verification_email error: {e}")
