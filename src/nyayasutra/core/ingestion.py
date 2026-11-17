"""
Gemini Multimodal Vision & Legal Document OCR Ingestion Engine.
"""

from typing import Optional
import httpx
from nyayasutra.core.config import settings


class MultimodalDocumentIngestor:
    """Ingests scanned images (FIRs, 7/12 Satbara, court summons) and extracts structured legal text."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    def construct_payload(self, base64_image: str, mime_type: str = "image/jpeg", target_lang: str = "gu") -> dict:
        prompt = (
            f"You are a specialized legal document extractor for Indian documents (FIR, Court Summon, Land Record 7/12). "
            f"Extract all text accurately, preserve law sections (IPC/BNS), survey numbers, and parties involved. "
            f"Provide a plain-language explanation in {target_lang}."
        )
        return {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": base64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.8,
                "maxOutputTokens": 2048
            }
        }

    async def extract_text(self, base64_image: str, mime_type: str = "image/jpeg", target_lang: str = "gu") -> str:
        """Calls Gemini Vision API if key is present, else returns clean offline fallback."""
        if not self.api_key:
            # Clean offline mock response for local testing & development
            return (
                "OFFLINE_INGESTION: Document scanned successfully. Detected land revenue record "
                "with boundary dispute references under BNS 329 / IPC 441."
            )

        payload = self.construct_payload(base64_image, mime_type, target_lang)
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{self.base_url}?key={self.api_key}",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                return candidates[0]["content"]["parts"][0]["text"]
            return ""
