"""
Unit tests for NyayaSutra BNS Concordance & Legal Analysis Engine.
"""

from nyayasutra.bns_engine.concordance import BNSKnowledgeEngine
from nyayasutra.core.models import LanguageCode
from nyayasutra.drafting.templates import LegalDraftingEngine
from nyayasutra.voice.assistant import VoiceAssistantBridge


def test_bns_engine_direct_lookup():
    engine = BNSKnowledgeEngine()

    # IPC 420 -> BNS 318
    mapping_420 = engine.find_by_ipc("420")
    assert mapping_420 is not None
    assert mapping_420.bns_section == "318"
    assert "धोखाधड़ी" in mapping_420.simplified_summary["hi"]
    assert "છેતરપિંડી" in mapping_420.simplified_summary["gu"]

    # IPC 302 -> BNS 103
    mapping_302 = engine.find_by_ipc("302")
    assert mapping_302 is not None
    assert mapping_302.bns_section == "103"


def test_scan_text_for_laws():
    engine = BNSKnowledgeEngine()

    sample_fir = "આરોપી વિરુદ્ધ IPC 420 અને IPC 506 મુજબ ગુનો નોંધવામાં આવ્યો છે."
    matches = engine.scan_text_for_laws(sample_fir)
    assert len(matches) >= 2
    matched_bns = [m.bns_section for m in matches]
    assert "318" in matched_bns  # 420
    assert "351" in matched_bns  # 506


def test_legal_drafting_engine():
    drafting = LegalDraftingEngine()
    notice = drafting.generate_land_encroachment_notice(
        applicant_name="Rameshbhai Patel",
        applicant_address="Gam: Sanand, Dist: Ahmedabad",
        applicant_contact="+91 9876543210",
        encroacher_name="Suresh Kumar",
        encroacher_address="Gam: Sanand",
        land_survey_number="Survey No. 402/1",
        village_district="Sanand, Ahmedabad",
        incident_date="10-11-2026",
    )
    assert "Rameshbhai Patel" in notice
    assert "Survey No. 402/1" in notice
    assert "Section 329 of the Bharatiya Nyaya Sanhita (BNS 2023)" in notice


def test_voice_assistant_bridge():
    voice = VoiceAssistantBridge()
    prompt_gu = voice.synthesize_response_prompt(LanguageCode.GUJARATI, "તમારો કેસ જમીન વિવાદનો છે.")
    assert "નમસ્તે" in prompt_gu
    assert "તમારો કેસ" in prompt_gu
