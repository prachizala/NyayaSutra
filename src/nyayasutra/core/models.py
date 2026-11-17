"""
Core Pydantic models for NyayaSutra.
"""

from enum import Enum
from pydantic import BaseModel, Field


class LanguageCode(str, Enum):
    GUJARATI = "gu"
    HINDI = "hi"
    MARATHI = "mr"
    TAMIL = "ta"
    TELUGU = "te"
    BENGALI = "bn"
    ENGLISH = "en"


class LawMapping(BaseModel):
    ipc_section: str = Field(..., description="Indian Penal Code 1860 Section")
    bns_section: str = Field(..., description="Bharatiya Nyaya Sanhita 2023 Section")
    offense_name: str
    bailable: bool
    cognizable: bool
    simplified_summary: dict[str, str] = Field(
        default_factory=dict,
        description="Vernacular plain explanations by language code"
    )


class LegalDocumentQuery(BaseModel):
    document_text: str
    target_language: LanguageCode = LanguageCode.HINDI
    extract_bns_mappings: bool = True
    generate_summary: bool = True


class LegalSummaryResponse(BaseModel):
    original_language_detected: str
    target_language: str
    plain_explanation: str
    mapped_bns_sections: list[LawMapping] = []
    recommended_actions: list[str] = []
    drafting_eligible: bool = False
    disclaimer: str = (
        "NyayaSutra provides informational guidance and legal translation only. "
        "It does not substitute certified advocate legal representation."
    )
