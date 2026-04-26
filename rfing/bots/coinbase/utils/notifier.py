"""
utils/notifier.py — Optional Telegram / email alerts (Coinbase bot copy)
"""
from __future__ import annotations
import os
import smtplib
from email.mime.text import MIMEText

import requests
from loguru import logger


def send_alert(message: str) -> None:
    """Send an alert via Telegram and/or email if configured."""
    _telegram(message)
    _email(message)


def _telegram(message: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=10)
    except Exception as exc:
        logger.warning(f"Telegram alert failed: {exc}")


def _email(message: str) -> None:
    host = os.getenv("SMTP_HOST", "")
    if not host:
        return
    try:
        port = int(os.getenv("SMTP_PORT", "587"))
        user = os.getenv("SMTP_USER", "")
        password = os.getenv("SMTP_PASS", "")
        to_addr = os.getenv("ALERT_EMAIL_TO", "")
        msg = MIMEText(message)
        msg["Subject"] = "[Coinbase Bot] Alert"
        msg["From"] = user
        msg["To"] = to_addr
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(user, [to_addr], msg.as_string())
    except Exception as exc:
        logger.warning(f"Email alert failed: {exc}")
