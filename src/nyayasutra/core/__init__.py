"""NyayaSutra Core package."""
from nyayasutra.core.config import settings
from nyayasutra.core.models import (
    LanguageCode,
    LawMapping,
    LegalDocumentQuery,
    LegalSummaryResponse,
)

__all__ = ["LanguageCode", "LawMapping", "LegalDocumentQuery", "LegalSummaryResponse", "settings"]
