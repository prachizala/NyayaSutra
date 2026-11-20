"""Statutory bail eligibility evaluator under Bharatiya Nagarik Suraksha Sanhita (BNSS)."""


class BailEligibilityEvaluator:
    """Evaluates bail eligibility and bailable thresholds for BNS statutory offenses."""

    NON_BAILABLE_SECTIONS = {318, 329, 303, 304}

    @classmethod
    def is_bailable(cls, bns_section: int) -> bool:
        """Determines if a section is bailable under BNSS first schedule."""
        return bns_section not in cls.NON_BAILABLE_SECTIONS

    @classmethod
    def evaluate_undertrial_threshold(cls, max_sentence_years: int, served_months: int) -> bool:
        """Section 479 BNSS: Maximum period for which undertrial prisoner can be detained."""
        half_sentence_months = (max_sentence_years * 12) / 2
        return served_months >= half_sentence_months
