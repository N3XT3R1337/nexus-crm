from app.tasks.celery_app import celery_app
import logging
import json

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def trigger_webhook_task(self, webhook_url: str, webhook_secret: str, event: str, payload: dict):
    try:
        import httpx
        import hmac
        import hashlib

        body = json.dumps(payload)
        headers = {"Content-Type": "application/json"}

        if webhook_secret:
            signature = hmac.new(webhook_secret.encode(), body.encode(), hashlib.sha256).hexdigest()
            headers["X-Webhook-Signature"] = signature

        headers["X-Webhook-Event"] = event

        with httpx.Client(timeout=30) as client:
            response = client.post(webhook_url, content=body, headers=headers)
            response.raise_for_status()

        return {"status": "delivered", "status_code": response.status_code}
    except Exception as exc:
        logger.error(f"Webhook delivery failed: {exc}")
        self.retry(exc=exc, countdown=60 * (self.request.retries + 1))


@celery_app.task
def process_deal_stage_change(deal_id: str, old_stage: str, new_stage: str, user_id: str):
    logger.info(f"Deal {deal_id} stage changed from {old_stage} to {new_stage} by {user_id}")
    return {"deal_id": deal_id, "old_stage": old_stage, "new_stage": new_stage}
