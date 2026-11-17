"""
BNS (Bharatiya Nyaya Sanhita 2023) Knowledge Database & IPC Concordance Engine.
"""


from nyayasutra.core.models import LawMapping

# Comprehensive foundational concordance mappings between Indian Penal Code (1860)
# and Bharatiya Nyaya Sanhita (2023) with vernacular vernacular breakdowns.
CONCORDANCE_REGISTRY: list[LawMapping] = [
    LawMapping(
        ipc_section="420",
        bns_section="318",
        offense_name="Cheating and dishonestly inducing delivery of property",
        bailable=False,
        cognizable=True,
        simplified_summary={
            "en": "Cheating or financial fraud against someone to dishonestly obtain money or property.",
            "hi": "धोखाधड़ी या बेईमानी से किसी की संपत्ति या पैसे हड़पने का अपराध।",
            "gu": "છેતરપિંડી અથવા અપ્રમાણિકપણે કોઈની મિલકત કે પૈસા પડાવી લેવાનો ગુનો."
        }
    ),
    LawMapping(
        ipc_section="302",
        bns_section="103",
        offense_name="Punishment for Murder",
        bailable=False,
        cognizable=True,
        simplified_summary={
            "en": "Causing intentional death of a person.",
            "hi": "हत्या (कत्ल) का गंभीर अपराध।",
            "gu": "કોઈ વ્યક્તિની ઈરાદાપૂર્વક હત્યા કરવાનો ગુનો."
        }
    ),
    LawMapping(
        ipc_section="378",
        bns_section="303",
        offense_name="Theft",
        bailable=False,
        cognizable=True,
        simplified_summary={
            "en": "Taking movable property out of possession without consent.",
            "hi": "चोरी का अपराध (बिना अनुमति किसी की चल संपत्ति ले जाना)।",
            "gu": "ચોરીનો ગુનો (પરવાનગી વગર કોઈની વસ્તુ લઈ લેવી)."
        }
    ),
    LawMapping(
        ipc_section="498A",
        bns_section="85",
        offense_name="Husband or relative of husband subjecting woman to cruelty",
        bailable=False,
        cognizable=True,
        simplified_summary={
            "en": "Domestic cruelty and harassment of a woman by husband or in-laws.",
            "hi": "पति या उसके रिश्तेदारों द्वारा महिला पर घरेलू क्रूरता और प्रताड़ना।",
            "gu": "પતિ અથવા સાસરિયાઓ દ્વારા સ્ત્રી પર માનસિક કે શારીરિક ત્રાસ."
        }
    ),
    LawMapping(
        ipc_section="506",
        bns_section="351",
        offense_name="Criminal Intimidation",
        bailable=True,
        cognizable=False,
        simplified_summary={
            "en": "Threatening injury to person, reputation, or property.",
            "hi": "जान से मारने या नुकसान पहुँचाने की धमकी देना (आपराधिक धमकी)।",
            "gu": "જાનથી મારી નાખવાની કે નુકસાન પહોંચાડવાની ધમકી આપવી."
        }
    ),
    LawMapping(
        ipc_section="441",
        bns_section="329",
        offense_name="Criminal Trespass (Land / Property encroachment)",
        bailable=True,
        cognizable=False,
        simplified_summary={
            "en": "Entering someone's land or property unlawfully to commit an offense or intimidate.",
            "hi": "किसी की ज़मीन या मकान पर अवैध कब्ज़ा या बिना अनुमति घुसपैठ करना।",
            "gu": "કોઈની જમીન કે મકાનમાં ગેરકાયદેસર રીતે ઘૂસી જવું કે કબજો કરવાનો પ્રયાસ."
        }
    )
]


class BNSKnowledgeEngine:
    """Intelligent Concordance and Legal Mapping Engine."""

    def __init__(self):
        self._ipc_lookup: dict[str, LawMapping] = {
            m.ipc_section.strip().upper(): m for m in CONCORDANCE_REGISTRY
        }
        self._bns_lookup: dict[str, LawMapping] = {
            m.bns_section.strip().upper(): m for m in CONCORDANCE_REGISTRY
        }

    def find_by_ipc(self, ipc_section: str) -> LawMapping | None:
        cleaned = ipc_section.strip().upper().replace("SECTION", "").replace("SEC", "").strip()
        return self._ipc_lookup.get(cleaned)

    def find_by_bns(self, bns_section: str) -> LawMapping | None:
        cleaned = bns_section.strip().upper().replace("SECTION", "").replace("SEC", "").strip()
        return self._bns_lookup.get(cleaned)

    def scan_text_for_laws(self, text: str) -> list[LawMapping]:
        """Scans arbitrary legal text, FIRs, or notices for mentions of IPC/BNS sections."""
        matches: list[LawMapping] = []
        lower_text = text.lower()

        for ipc_sec, mapping in self._ipc_lookup.items():
            patterns = [
                f"{ipc_sec.lower()}",
                f"ipc {ipc_sec.lower()}",
                f"section {ipc_sec.lower()}",
                f"sec {ipc_sec.lower()}",
                f"कलम {ipc_sec.lower()}",
                f"धारा {ipc_sec.lower()}"
            ]
            if any(p in lower_text for p in patterns) and mapping not in matches:
                matches.append(mapping)

        for bns_sec, mapping in self._bns_lookup.items():
            patterns = [
                f"bns {bns_sec.lower()}",
                f"bns section {bns_sec.lower()}",
                f"ન્યાય સંહિતા {bns_sec.lower()}",
                f"न्याय संहिता {bns_sec.lower()}"
            ]
            if any(p in lower_text for p in patterns) and mapping not in matches:
                matches.append(mapping)

        return matches
