"""
Notification system for alerts
"""
import logging
from typing import List
from .core import Alert
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Notifier:
    """Handles sending notifications"""
    
    def __init__(self, email_config: dict = None, alert_service=None):
        self.email_config = email_config or {}
        self.alert_service = alert_service
        self.notification_history: List[Alert] = []
        
    async def send_notification(self, alert: Alert, db_session=None):
        """Send notification for an alert"""
        self.notification_history.append(alert)
        
        # Save to database if alert_service is available
        if self.alert_service and db_session:
            try:
                self.alert_service.create_alert(db_session, alert)
            except Exception as e:
                logging.error(f"Error saving alert to database: {str(e)}")
        
        # Send via multiple channels
        await self._send_email(alert)
        await self._send_console_log(alert)
        # Could add: SMS, Push notifications, Webhooks, etc.
    
    async def _send_email(self, alert: Alert):
        """Send email notification"""
        if not self.email_config.get('enabled', False):
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config.get('sender_email')
            msg['To'] = self.email_config.get('receiver_email')
            msg['Subject'] = f"🚨 NAV Alert: {alert.fund.scheme_name}"
            
            body = f"""
            <html>
            <body>
                <h2>Mutual Fund NAV Alert</h2>
                <p><strong>Fund:</strong> {alert.fund.scheme_name}</p>
                <p><strong>Scheme Code:</strong> {alert.fund.scheme_code}</p>
                <p><strong>Drop Percentage:</strong> {alert.drop_percentage:.2f}%</p>
                <p><strong>Current NAV:</strong> ₹{alert.current_nav:.2f}</p>
                <p><strong>Previous NAV:</strong> ₹{alert.previous_nav:.2f}</p>
                <p><strong>Severity:</strong> {alert.severity.upper()}</p>
                <p><strong>Time:</strong> {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <hr>
                <p>{alert.message}</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(
                self.email_config.get('smtp_server', 'smtp.gmail.com'),
                self.email_config.get('smtp_port', 587)
            ) as server:
                server.starttls()
                server.login(
                    self.email_config.get('sender_email'),
                    self.email_config.get('password')
                )
                server.send_message(msg)
            
            logger.info(f"Email notification sent for {alert.fund.scheme_name}")
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
    
    async def _send_console_log(self, alert: Alert):
        """Log alert to console"""
        logger.warning(
            f"ALERT [{alert.severity.upper()}]: {alert.fund.scheme_name} - "
            f"{alert.drop_percentage:.2f}% drop | NAV: ₹{alert.current_nav:.2f}"
        )
    
    def get_notification_history(self, limit: int = 50) -> List[Alert]:
        """Get recent notification history"""
        return self.notification_history[-limit:]

