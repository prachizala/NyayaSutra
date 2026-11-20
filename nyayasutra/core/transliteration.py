"""Gujarati and Hindi vernacular legal term normalization engine."""


class VernacularLegalNormalizer:
    """Normalizes Gujarati revenue terminology into standardized legal terms."""

    GLOSSARY_MAP = {
        "satbara": "Record of Rights (Form 7/12)",
        "pedhinamu": "Family Tree Pedigree Certificate",
        "dastavej": "Registered Sale Deed",
        "ferfar": "Mutation Entry (Form 6)",
        "bojo": "Encumbrance / Bank Lien",
        "khedut khatedar": "Recognized Agricultural Landholder",
    }

    @classmethod
    def normalize_term(cls, vernacular_input: str) -> str:
        """Maps vernacular term to official English legal concordance."""
        cleaned = vernacular_input.strip().lower()
        return cls.GLOSSARY_MAP.get(cleaned, cleaned.title())
