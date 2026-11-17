"""
WhatsApp Cloud API Webhook Handler & Citizen Inbound Message Pipeline.
"""

from typing import Optional
from pydantic import BaseModel, Field


class WhatsAppMessageContact(BaseModel):
    wa_id: str
    name: Optional[str] = None


class WhatsAppMedia(BaseModel):
    id: str
    mime_type: str
    sha256: Optional[str] = None


class WhatsAppInboundMessage(BaseModel):
    from_number: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: str  # "text", "audio", "image", "document"
    text_body: Optional[str] = None
    media: Optional[WhatsAppMedia] = None


class WhatsAppWebhookDispatcher:
    """Dispatches citizen WhatsApp messages to NyayaSutra Voice and BNS engines."""

    def __init__(self):
        self.supported_message_types = ["text", "audio", "image", "document"]

    def parse_inbound_payload(self, raw_payload: dict) -> list[WhatsAppInboundMessage]:
        messages: list[WhatsAppInboundMessage] = []
        entries = raw_payload.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                val = change.get("value", {})
                raw_msgs = val.get("messages", [])
                for rm in raw_msgs:
                    m_type = rm.get("type")
                    text_content = rm.get("text", {}).get("body") if m_type == "text" else None
                    media_content = None
                    if m_type in ["audio", "image", "document"]:
                        media_obj = rm.get(m_type, {})
                        media_content = WhatsAppMedia(
                            id=media_obj.get("id", ""),
                            mime_type=media_obj.get("mime_type", "")
                        )
                    messages.append(
                        WhatsAppInboundMessage(
                            **{
                                "from": rm.get("from", ""),
                                "id": rm.get("id", ""),
                                "timestamp": rm.get("timestamp", ""),
                                "type": m_type,
                                "text_body": text_content,
                                "media": media_content
                            }
                        )
                    )
        return messages

    def format_whatsapp_reply(self, recipient_number: str, text_message: str) -> dict:
        """Formats standard outbound WhatsApp message body."""
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_number,
            "type": "text",
            "text": {"preview_url": False, "body": text_message}
        }
