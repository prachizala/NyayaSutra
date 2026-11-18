"""
Unit tests for Satbara Sentinel Engine.
"""

from nyayasutra.bns_engine.sentinel import SatbaraSentinelEngine


def test_sentinel_inspection():
    engine = SatbaraSentinelEngine()
    record = engine.inspect_land_parcel(
        survey_number="402/1", village="Sanand", taluka="Sanand", district="Ahmedabad"
    )
    assert record.survey_number == "402/1"
    assert record.total_area_hectares > 0.0
    assert 0 <= record.dispute_risk_score <= 100
    assert len(record.boundary_coordinates) >= 4
    assert len(record.encroachment_alerts) >= 1
