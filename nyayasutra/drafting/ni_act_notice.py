"""Statutory legal notice generator for Negotiable Instruments Act dishonour of cheque."""

from datetime import datetime


class NIActNoticeBuilder:
    """Builds formal legal notice under Section 138 of Negotiable Instruments Act."""

    @staticmethod
    def build_notice(
        payee_name: str,
        drawer_name: str,
        cheque_number: str,
        amount_inr: float,
        cheque_date: str,
        memo_date: str,
    ) -> dict:
        """Constructs statutory notice structure with 15-day cure demand timeline."""
        return {
            "statutory_act": "Negotiable Instruments Act, 1881",
            "section": "Section 138 & 142",
            "payee": payee_name,
            "drawer": drawer_name,
            "cheque_number": cheque_number,
            "amount_inr": amount_inr,
            "dishonour_reason": "Funds Insufficient",
            "demand_timeline_days": 15,
            "generated_at": datetime.utcnow().isoformat(),
        }
