"""Service de routage GreenRoute — interface simulée avec l'API ToulouseMap."""

import math
from typing import List, Tuple


class RoutingService:
    """Service de calcul d'itinéraire simulant l'API externe ToulouseMap.

    Les distances et itinéraires sont simulés car l'API réelle n'est pas
    connectée dans cette implémentation.
    """

    # Coordonnées approximatives pour la simulation (Toulouse, France)
    DEFAULT_PICKUP_COORDS: Tuple[float, float] = (43.6045, 1.4440)   # Centre de Toulouse
    DEFAULT_DELIVERY_COORDS: Tuple[float, float] = (43.6100, 1.4500)  # À 1 km environ

    @staticmethod
    def calculate_distance(
        pickup_address: str,
        delivery_address: str,
    ) -> float:
        """Calcule une distance simulée entre deux adresses.

        Dans une implémentation réelle, cette méthode interrogerait
        l'API ToulouseMap. Ici, elle retourne une valeur fixe pour
        la démonstration.

        Parameters
        ----------
        pickup_address : str
            Adresse de ramassage.
        delivery_address : str
            Adresse de livraison.

        Returns
        -------
        float
            Distance en kilomètres.
        """
        # Simulation : on utilise une distance fixe de 5.0 km
        return 5.0

    @staticmethod
    def calculate_route(
        pickup_address: str,
        delivery_address: str,
    ) -> List[Tuple[float, float]]:
        """Calcule un itinéraire simulé entre deux adresses.

        Retourne une liste de coordonnées (lat, lon) représentant
        le trajet.

        Parameters
        ----------
        pickup_address : str
            Adresse de ramassage.
        delivery_address : str
            Adresse de livraison.

        Returns
        -------
        List[Tuple[float, float]]
            Liste de points (latitude, longitude) formant l'itinéraire.
        """
        # Simulation : on génère quelques points intermédiaires
        lat1, lon1 = RoutingService.DEFAULT_PICKUP_COORDS
        lat2, lon2 = RoutingService.DEFAULT_DELIVERY_COORDS

        steps = 5
        route = []
        for i in range(steps + 1):
            t = i / steps
            lat = lat1 + (lat2 - lat1) * t
            lon = lon1 + (lon2 - lon1) * t
            route.append((round(lat, 6), round(lon, 6)))

        return route
