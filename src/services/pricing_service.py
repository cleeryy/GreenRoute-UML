"""Service de tarification GreenRoute — calcule le coût et les économies carbone."""

from typing import Dict

from src.model.enums import UrgencyLevel
from src.model.package import Package


class PricingService:
    """Service de calcul des coûts de livraison et des économies carbone.

    Règles de tarification :
    - Tarif de base : 5 € par kg (plafonné à 10 kg)
    - Supplément distance : 0,50 € par km
    - Supplément Express : +30 % sur le total
    - Économies carbone : 150 g CO₂ évitées par km (vs diesel)
    """

    BASE_RATE_PER_KG: float = 5.0
    MAX_WEIGHT_FOR_BASE_RATE: float = 10.0
    DISTANCE_RATE_PER_KM: float = 0.50
    EXPRESS_SURCHARGE: float = 0.30
    CARBON_PER_KM: float = 150.0  # grammes de CO₂ évités par km

    @staticmethod
    def calculate_cost(package: Package, distance_km: float, urgency: UrgencyLevel) -> Dict[str, float]:
        """Calcule le coût total et les économies carbone pour une livraison.

        Parameters
        ----------
        package : Package
            Colis à livrer.
        distance_km : float
            Distance en kilomètres.
        urgency : UrgencyLevel
            Niveau d'urgence.

        Returns
        -------
        Dict[str, float]
            Dictionnaire contenant :
            - 'total_cost' : coût total en euros
            - 'carbon_savings' : grammes de CO₂ évités
        """
        # Tarif de base basé sur le poids (plafonné à 10 kg)
        effective_weight = min(package.weight, PricingService.MAX_WEIGHT_FOR_BASE_RATE)
        base_cost = effective_weight * PricingService.BASE_RATE_PER_KG

        # Supplément distance
        distance_cost = distance_km * PricingService.DISTANCE_RATE_PER_KM

        # Total avant supplément urgence
        subtotal = base_cost + distance_cost

        # Supplément Express
        if urgency == UrgencyLevel.EXPRESS:
            subtotal *= (1 + PricingService.EXPRESS_SURCHARGE)

        # Économies carbone
        carbon_savings = distance_km * PricingService.CARBON_PER_KM

        return {
            "total_cost": round(subtotal, 2),
            "carbon_savings": round(carbon_savings, 2),
        }
