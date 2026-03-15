from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, to_email: str, subject: str, body: str):
    try:
        from app.config import settings
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        if not settings.SMTP_USER:
            logger.warning(f"SMTP not configured, would send email to {to_email}: {subject}")
            return {"status": "skipped", "reason": "SMTP not configured"}

        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        return {"status": "sent", "to": to_email}
    except Exception as exc:
        logger.error(f"Email send failed: {exc}")
        self.retry(exc=exc, countdown=60 * (self.request.retries + 1))


@celery_app.task(bind=True, max_retries=3)
def send_bulk_email_task(self, recipients: list, subject: str, body: str):
    results = []
    for email in recipients:
        result = send_email_task.delay(email, subject, body)
        results.append({"email": email, "task_id": result.id})
    return {"status": "queued", "count": len(results), "tasks": results}


@celery_app.task
def send_notification_email(user_email: str, notification_title: str, notification_message: str):
    subject = f"Nexus CRM: {notification_title}"
    body = f"""
    <html>
    <body>
    <h2>{notification_title}</h2>
    <p>{notification_message}</p>
    <hr>
    <p><small>This is an automated notification from Nexus CRM</small></p>
    </body>
    </html>
    """
    return send_email_task.delay(user_email, subject, body)
