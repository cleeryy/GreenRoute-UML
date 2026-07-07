"""Module définissant le livreur (DeliveryPerson) de la plateforme GreenRoute."""

import uuid
from typing import TYPE_CHECKING, List

from src.model.enums import DeliveryPersonState, OrderStatus

if TYPE_CHECKING:
    from src.model.order import Order


class DeliveryPerson:
    """Représente un livreur indépendant sur la plateforme GreenRoute.

    Le livreur utilise un moyen de transport écologique (vélo cargo,
    triporteur, camionnette électrique) et peut être assigné à plusieurs
    commandes au fil du temps.

    Attributes
    ----------
    _delivery_person_id : str
        Identifiant unique UUID4 généré automatiquement.
    _name : str
        Nom complet du livreur.
    _email : str
        Adresse e-mail.
    _phone : str
        Numéro de téléphone.
    _transport_mode : str
        Moyen de transport (ex: "Vélo cargo", "Triporteur", "Camionnette électrique").
    _current_state : DeliveryPersonState
        État opérationnel actuel.
    _latitude : float
        Latitude de la position actuelle.
    _longitude : float
        Longitude de la position actuelle.
    _assigned_orders : List[Order]
        Liste des commandes assignées à ce livreur.
    """

    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        transport_mode: str,
        latitude: float = 0.0,
        longitude: float = 0.0,
    ) -> None:
        """Initialise un nouveau livreur.

        Parameters
        ----------
        name : str
            Nom complet du livreur.
        email : str
            Adresse e-mail.
        phone : str
            Numéro de téléphone.
        transport_mode : str
            Moyen de transport écologique.
        latitude : float, optional
            Latitude initiale (par défaut 0.0).
        longitude : float, optional
            Longitude initiale (par défaut 0.0).
        """
        self._delivery_person_id = str(uuid.uuid4())
        self._name = name
        self._email = email
        self._phone = phone
        self._transport_mode = transport_mode
        self._current_state = DeliveryPersonState.DISPONIBLE
        self._latitude = latitude
        self._longitude = longitude
        self._assigned_orders: List[Order] = []

    # ── Propriétés (getters) ──────────────────────────────────────────

    @property
    def delivery_person_id(self) -> str:
        """Identifiant unique du livreur."""
        return self._delivery_person_id

    @property
    def name(self) -> str:
        """Nom complet du livreur."""
        return self._name

    @property
    def email(self) -> str:
        """Adresse e-mail du livreur."""
        return self._email

    @property
    def phone(self) -> str:
        """Numéro de téléphone du livreur."""
        return self._phone

    @property
    def transport_mode(self) -> str:
        """Moyen de transport du livreur."""
        return self._transport_mode

    @property
    def current_state(self) -> DeliveryPersonState:
        """État opérationnel actuel du livreur."""
        return self._current_state

    @current_state.setter
    def current_state(self, state: DeliveryPersonState) -> None:
        """Modifie l'état opérationnel du livreur.

        Parameters
        ----------
        state : DeliveryPersonState
            Nouvel état.
        """
        self._current_state = state

    @property
    def latitude(self) -> float:
        """Latitude de la position actuelle."""
        return self._latitude

    @latitude.setter
    def latitude(self, lat: float) -> None:
        """Met à jour la latitude.

        Parameters
        ----------
        lat : float
            Nouvelle latitude.
        """
        self._latitude = lat

    @property
    def longitude(self) -> float:
        """Longitude de la position actuelle."""
        return self._longitude

    @longitude.setter
    def longitude(self, lon: float) -> None:
        """Met à jour la longitude.

        Parameters
        ----------
        lon : float
            Nouvelle longitude.
        """
        self._longitude = lon

    @property
    def assigned_orders(self) -> List["Order"]:
        """Liste des commandes assignées à ce livreur (lecture seule)."""
        return list(self._assigned_orders)

    # ── Méthodes métier ───────────────────────────────────────────────

    def set_available(self) -> None:
        """Passe le livreur en état Disponible."""
        self._current_state = DeliveryPersonState.DISPONIBLE

    def set_on_tour(self) -> None:
        """Passe le livreur en état En Tournée."""
        self._current_state = DeliveryPersonState.EN_TOURNEE

    def update_location(self, lat: float, lon: float) -> None:
        """Met à jour la position géographique du livreur.

        Parameters
        ----------
        lat : float
            Nouvelle latitude.
        lon : float
            Nouvelle longitude.
        """
        self._latitude = lat
        self._longitude = lon

    def accept_order(self, order: "Order") -> None:
        """Accepte une commande et la marque comme étant en cours d'attribution.

        Parameters
        ----------
        order : Order
            Commande à accepter.
        """
        order._status = OrderStatus.EN_COURS_D_ATTRIBUTION
        order._delivery_person = self
        self._assigned_orders.append(order)

    # ── Représentation ────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"DeliveryPerson(name={self._name!r}, "
            f"transport={self._transport_mode!r}, "
            f"state={self._current_state.value})"
        )
