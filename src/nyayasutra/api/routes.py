"""
FastAPI Endpoints for NyayaSutra Citizen Intelligence Suite.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from nyayasutra.core.config import settings
from nyayasutra.core.models import LegalDocumentQuery, LegalSummaryResponse
from nyayasutra.bns_engine.concordance import BNSKnowledgeEngine
from nyayasutra.drafting.templates import LegalDraftingEngine
from nyayasutra.voice.assistant import VoiceAssistantBridge

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Democratizing legal & civic entitlements across Bharat via voice-first vernacular AI."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bns_engine = BNSKnowledgeEngine()
drafting_engine = LegalDraftingEngine()
voice_bridge = VoiceAssistantBridge()


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.env
    }


@app.get("/api/v1/bns/lookup/{section}")
async def lookup_bns(section: str):
    mapping = bns_engine.find_by_bns(section) or bns_engine.find_by_ipc(section)
    if not mapping:
        raise HTTPException(status_code=404, detail=f"Law section '{section}' not found in registry.")
    return mapping


@app.post("/api/v1/analyze", response_model=LegalSummaryResponse)
async def analyze_document(query: LegalDocumentQuery):
    matched_laws = bns_engine.scan_text_for_laws(query.document_text)
    
    # Generate contextual vernacular explanation
    lang_key = query.target_language.value
    summaries = []
    for law in matched_laws:
        summary_text = law.simplified_summary.get(lang_key) or law.simplified_summary.get("en", "")
        summaries.append(f"{law.bns_section} BNS (Old IPC {law.ipc_section}): {summary_text}")
    
    explanation = "\n".join(summaries) if summaries else (
        "No severe penal offenses found in scanned excerpt. Standard civil/regulatory terms detected."
    )
    
    actions = [
        "Consult local District Legal Services Authority (DLSA) for free government legal aid.",
        "Verify your land title or account details on official state portal (AnyRoR / Bhulekh)."
    ]
    if any(m.bns_section in ["329", "351"] for m in matched_laws):
        actions.append("Draft a formal land dispute cessation notice using NyayaSutra Drafting Engine.")

    return LegalSummaryResponse(
        original_language_detected="gu/hi/en",
        target_language=query.target_language.value,
        plain_explanation=explanation,
        mapped_bns_sections=matched_laws,
        recommended_actions=actions,
        drafting_eligible=len(matched_laws) > 0
    )
