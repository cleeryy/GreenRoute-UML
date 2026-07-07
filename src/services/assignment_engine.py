"""Moteur d'attribution GreenRoute — assigne les commandes aux livreurs disponibles."""

import math
from typing import List, Optional

from src.model.delivery_person import DeliveryPerson, DeliveryPersonState
from src.model.order import Order, OrderStatus


class AssignmentEngine:
    """Moteur d'attribution des commandes aux livreurs disponibles.

    Maintient une file d'attente des commandes en attente et un registre
    des livreurs disponibles. L'attribution se fait par proximité
    géographique (distance euclidienne/Haversine dans un rayon donné).

    Attributes
    ----------
    _pending_orders : List[Order]
        Commandes en attente d'attribution.
    _available_delivery_persons : List[DeliveryPerson]
        Livreurs actuellement disponibles.
    """

    def __init__(self) -> None:
        """Initialise le moteur d'attribution."""
        self._pending_orders: List[Order] = []
        self._available_delivery_persons: List[DeliveryPerson] = []

    @property
    def pending_orders(self) -> List[Order]:
        """Commandes en attente d'attribution (lecture seule)."""
        return list(self._pending_orders)

    @property
    def available_delivery_persons(self) -> List[DeliveryPerson]:
        """Livreurs disponibles (lecture seule)."""
        return list(self._available_delivery_persons)

    # ── Méthodes de registre ──────────────────────────────────────────

    def register_order(self, order: Order) -> None:
        """Ajoute une commande à la file d'attente d'attribution.

        Parameters
        ----------
        order : Order
            Commande à enregistrer.
        """
        if order not in self._pending_orders:
            self._pending_orders.append(order)

    def register_delivery_person(self, dp: DeliveryPerson) -> None:
        """Enregistre un livreur comme disponible.

        Parameters
        ----------
        dp : DeliveryPerson
            Livreur à enregistrer.
        """
        if dp not in self._available_delivery_persons:
            self._available_delivery_persons.append(dp)

    # ── Méthodes de calcul de distance ────────────────────────────────

    @staticmethod
    def _haversine_distance(
        lat1: float, lon1: float,
        lat2: float, lon2: float,
    ) -> float:
        """Calcule la distance en kilomètres entre deux points GPS.

        Utilise la formule de Haversine pour une estimation précise
        sur la surface terrestre.

        Parameters
        ----------
        lat1, lon1 : float
            Coordonnées du premier point en degrés.
        lat2, lon2 : float
            Coordonnées du second point en degrés.

        Returns
        -------
        float
            Distance en kilomètres.
        """
        R = 6371.0  # Rayon de la Terre en km

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    # ── Méthodes d'attribution ────────────────────────────────────────

    def find_nearby_delivery_person(
        self,
        order: Order,
        max_radius_km: float = 3.0,
    ) -> Optional[DeliveryPerson]:
        """Trouve le livreur disponible le plus proche dans un rayon donné.

        Parcourt les livreurs disponibles et retourne celui qui est
        à la fois dans le rayon et le plus proche de l'adresse de
        ramassage.

        Parameters
        ----------
        order : Order
            Commande pour laquelle trouver un livreur.
        max_radius_km : float, optional
            Rayon de recherche en km (par défaut 3.0).

        Returns
        -------
        Optional[DeliveryPerson]
            Le livreur le plus proche dans le rayon, ou None si aucun
            livreur disponible n'est trouvé.
        """
        # Coordonnées simulées pour le point de ramassage
        pickup_lat, pickup_lon = 43.6045, 1.4440  # Centre de Toulouse

        best_dp: Optional[DeliveryPerson] = None
        best_distance = float("inf")

        for dp in self._available_delivery_persons:
            if dp.current_state != DeliveryPersonState.DISPONIBLE:
                continue

            dist = self._haversine_distance(
                dp.latitude, dp.longitude,
                pickup_lat, pickup_lon,
            )

            if dist <= max_radius_km and dist < best_distance:
                best_distance = dist
                best_dp = dp

        return best_dp

    def assign_order_to_nearest(self, order: Order) -> Optional[Order]:
        """Assigne la commande au livreeur disponible le plus proche.

        Si un livreur est trouvé, la commande lui est assignée,
        retirée de la file d'attente, et le statut est mis à jour.

        Parameters
        ----------
        order : Order
            Commande à assigner.

        Returns
        -------
        Optional[Order]
            La commande assignée, ou None si aucun livreur n'a été trouvé.
        """
        dp = self.find_nearby_delivery_person(order)
        if dp is None:
            return None

        order.assign_to(dp)
        self._pending_orders.remove(order)
        return order
