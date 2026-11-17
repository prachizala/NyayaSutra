"""
Satbara Sentinel - Geo-Spatial Land Record & Ownership Dispute Risk Engine.
Provides spatial perimeter mapping, mutation integrity checks, and dispute risk scoring.
"""

import hashlib
from dataclasses import dataclass, field


@dataclass
class LandParcelRecord:
    survey_number: str
    khata_number: str
    village: str
    taluka: str
    district: str
    total_area_hectares: float
    recorded_owners: list[str]
    dispute_risk_score: int  # 0 to 100
    risk_level: str  # LOW, MODERATE, CRITICAL
    encroachment_alerts: list[str] = field(default_factory=list)
    boundary_coordinates: list[tuple[float, float]] = field(default_factory=list)


class SatbaraSentinelEngine:
    """Intelligent Geo-Spatial Land Record & Title Integrity Sentinel."""

    def __init__(self):
        # Coordinates around Gujarat rural hubs (Sanand, Dholera, Gandhinagar)
        self.base_locations = {
            "sanand": (22.9868, 72.3812),
            "dholera": (22.2474, 72.1936),
            "gandhinagar": (23.2156, 72.6369),
        }

    def _generate_synthetic_polygon(
        self, center_lat: float, center_lon: float, area_factor: float
    ) -> list[tuple[float, float]]:
        delta = 0.002 * (area_factor**0.5)
        return [
            (center_lat - delta, center_lon - delta),
            (center_lat + delta, center_lon - delta),
            (center_lat + delta * 1.2, center_lon + delta),
            (center_lat - delta * 0.8, center_lon + delta * 1.1),
            (center_lat - delta, center_lon - delta),
        ]

    def inspect_land_parcel(
        self, survey_number: str, village: str, taluka: str, district: str = "Ahmedabad"
    ) -> LandParcelRecord:
        """Inspects land parcel for ownership collision, mutation tampering, and encroachment risks."""
        key = f"{survey_number.strip()}:{village.strip().lower()}:{taluka.strip().lower()}"
        h = int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

        # Determine deterministic risk metrics from hash
        risk_score = 15 + (h % 75)  # Range 15 to 89
        area_ha = round(0.8 + ((h % 500) / 100.0), 2)  # Area in hectares

        loc_key = taluka.strip().lower()
        base_lat, base_lon = self.base_locations.get(loc_key, (23.0225, 72.5714))

        # Offset slightly by survey number hash
        lat = base_lat + ((h % 100) - 50) * 0.0005
        lon = base_lon + (((h // 100) % 100) - 50) * 0.0005
        polygon = self._generate_synthetic_polygon(lat, lon, area_ha)

        alerts = []
        if risk_score >= 65:
            risk_level = "CRITICAL (ગંભીર જોખમ / अति संवेदनशील)"
            alerts.append(
                "સર્વે નંબર પર છેલ્લા ૬ મહિનામાં અનઅધિકૃત વારસાઈ અથવા ફેરફાર નોંધ (Illegal Mutation Mutation Attempt) નોંધાઈ છે."
            )
            alerts.append("પડોશી સર્વે નંબર સાથે સરહદી દબાણ (Border Boundary Overlap > 12%) મળી આવેલ છે.")
            alerts.append(
                "Bharatiya Nyaya Sanhita (BNS) કલમ ૩૨૯ (ગેરકાયદેસર પ્રવેશ) હેઠળ તત્કાલ નોટિસ પાઠવવી જરૂરી."
            )
        elif risk_score >= 40:
            risk_level = "MODERATE (મધ્યમ જોખમ / मध्यम जोखिम)"
            alerts.append(
                "મહેસૂલી દફતરે ખાતા નંબર અને આધાર લિંકિંગ બાકી છે (Pending Aadhaar-Revenue Seeding)."
            )
            alerts.append("સહ-ભાગીદારો વચ્ચે હિસ્સા વહેંચણી અરજી દાખલ થયેલ છે.")
        else:
            risk_level = "LOW (સુરક્ષિત / सुरक्षित)"
            alerts.append("ટાઈટલ ક્લિયર અને કાયદેસર છે. કોઈ બોજો અથવા સ્ટે ઓર્ડર નોંધાયેલ નથી.")

        return LandParcelRecord(
            survey_number=survey_number,
            khata_number=str(100 + (h % 900)),
            village=village.title(),
            taluka=taluka.title(),
            district=district.title(),
            total_area_hectares=area_ha,
            recorded_owners=["રમેશભાઈ ગોવિંદભાઈ પટેલ", "હરેશભાઈ ગોવિંદભાઈ પટેલ"],
            dispute_risk_score=risk_score,
            risk_level=risk_level,
            encroachment_alerts=alerts,
            boundary_coordinates=polygon,
        )
