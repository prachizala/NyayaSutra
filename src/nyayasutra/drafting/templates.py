"""
Automated Legal Notice & Citizen Grievance Drafting Engine.
"""

from datetime import datetime

try:
    from jinja2 import Template
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False


LAND_ENCROACHMENT_NOTICE_TEMPLATE = """
LEGAL NOTICE / FORMAL COMPLAINT (ચેતવણી / ઔપચારિક નોટિસ)
Date / તારીખ: {{ date }}
Place / સ્થળ: {{ place }}

TO / પ્રતિ:
{{ encroacher_name }}
{{ encroacher_address }}

SUBJECT: Immediate cessation of unlawful encroachment and trespass on Survey No. / Land Record: {{ land_survey_number }}

Dear Sir / Madam,

Under instructions from and on behalf of my client / lawful occupant: {{ applicant_name }}, resident of {{ applicant_address }}, I hereby bring the following facts to your urgent notice:

1. My client is the absolute lawful owner and title-holder of agricultural/residential land registered under Survey/Account No. {{ land_survey_number }} in {{ village_district }}.
2. It has been observed that since {{ incident_date }}, you and your associates have unlawfully attempted to encroach, alter boundaries, and trespass upon the aforementioned property without any legal entitlement.
3. Your acts constitute punishable offenses under Section 329 of the Bharatiya Nyaya Sanhita (BNS 2023) [erstwhile Section 441 of the Indian Penal Code (IPC)], along with criminal intimidation under Section 351 of BNS 2023.

DEMAND:
You are hereby called upon to forthwith remove all unauthorized materials, cease illegal ingress, and restore possession within SEVEN (7) DAYS of receipt of this notice, failing which my client shall initiate both civil and criminal legal proceedings before the competent court at your sole risk and costs.

Yours faithfully,

_____________________________
{{ applicant_name }} / Authorized Signatory
Contact: {{ applicant_contact }}
"""


class LegalDraftingEngine:
    """Engine for generating formal Indian legal notices, land grievance letters, and RTI drafts."""

    def __init__(self):
        self._raw_template = LAND_ENCROACHMENT_NOTICE_TEMPLATE.strip()

    def generate_land_encroachment_notice(
        self,
        applicant_name: str,
        applicant_address: str,
        applicant_contact: str,
        encroacher_name: str,
        encroacher_address: str,
        land_survey_number: str,
        village_district: str,
        incident_date: str,
        place: str = "Gujarat, India"
    ) -> str:
        ctx = {
            "date": datetime.now().strftime("%d-%m-%Y"),
            "place": place,
            "applicant_name": applicant_name,
            "applicant_address": applicant_address,
            "applicant_contact": applicant_contact,
            "encroacher_name": encroacher_name,
            "encroacher_address": encroacher_address,
            "land_survey_number": land_survey_number,
            "village_district": village_district,
            "incident_date": incident_date
        }
        if HAS_JINJA:
            return Template(self._raw_template).render(**ctx)
        
        # Safe fallback without Jinja2
        rendered = self._raw_template
        for k, v in ctx.items():
            rendered = rendered.replace(f"{{{{ {k} }}}}", str(v))
        return rendered
