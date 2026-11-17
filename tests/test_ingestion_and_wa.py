"""
Unit tests for Multimodal Ingestion and WhatsApp Dispatcher.
"""

import pytest

from nyayasutra.api.whatsapp import WhatsAppWebhookDispatcher
from nyayasutra.core.ingestion import MultimodalDocumentIngestor


def test_gemini_payload_construction():
    ingestor = MultimodalDocumentIngestor(api_key="mock_key")
    payload = ingestor.construct_payload(base64_image="aGVsbG8=", mime_type="image/jpeg", target_lang="gu")
    
    assert "contents" in payload
    assert payload["contents"][0]["parts"][1]["inline_data"]["data"] == "aGVsbG8="
    assert "generationConfig" in payload


@pytest.mark.asyncio
async def test_offline_document_extraction():
    ingestor = MultimodalDocumentIngestor(api_key="")
    text = await ingestor.extract_text(base64_image="mock_data")
    assert "OFFLINE_INGESTION" in text
    assert "BNS 329" in text


def test_whatsapp_webhook_parser():
    dispatcher = WhatsAppWebhookDispatcher()
    sample_payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "from": "919876543210",
                                    "id": "wamid.HBgL...",
                                    "timestamp": "1731800000",
                                    "type": "text",
                                    "text": {"body": "મારી જમીનનો સાતબારા તપાસો"}
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
    msgs = dispatcher.parse_inbound_payload(sample_payload)
    assert len(msgs) == 1
    assert msgs[0].from_number == "919876543210"
    assert "સાતબારા" in msgs[0].text_body

    reply = dispatcher.format_whatsapp_reply("919876543210", "તમારો દસ્તાવેજ મળી ગયો છે.")
    assert reply["to"] == "919876543210"
    assert "દસ્તાવેજ" in reply["text"]["body"]
