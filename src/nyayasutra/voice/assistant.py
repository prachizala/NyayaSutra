"""
Vernacular Voice & Dialect Translation Interface.
"""

from nyayasutra.core.models import LanguageCode


class VoiceAssistantBridge:
    """Manages audio transcription, vernacular dialect normalization, and speech response routing."""

    def __init__(self):
        self.supported_dialects = {
            "gu": ["standard", "kathiyawadi", "surati"],
            "hi": ["standard", "bhojpuri", "awadhi"],
            "mr": ["standard", "deshi", "konkani"]
        }

    def synthesize_response_prompt(self, target_lang: LanguageCode, simplified_summary: str) -> str:
        """Constructs culturally natural, vernacular voice prompt for citizen playback."""
        if target_lang == LanguageCode.GUJARATI:
            return f"નમસ્તે. તમારા દસ્તાવેજનો સરળ સારાંશ: {simplified_summary} વધુ માહિતી માટે તમે પ્રશ્ન પૂછી શકો છો."
        elif target_lang == LanguageCode.HINDI:
            return f"नमस्ते। आपके दस्तावेज़ का सरल सारांश इस प्रकार है: {simplified_summary} अधिक जानकारी के लिए आप प्रश्न पूछ सकते हैं।"
        else:
            return f"Hello. Here is the plain summary of your legal document: {simplified_summary}"
