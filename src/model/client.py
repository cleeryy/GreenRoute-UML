"""Module définissant le client (expéditeur) de la plateforme GreenRoute."""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.model.order import Order
    from src.model.package import Package
    from src.model.enums import UrgencyLevel


class Client:
    """Représente un client expéditeur sur la plateforme GreenRoute.

    Un client peut passer plusieurs commandes ; la relation est une
    composition : les commandes appartiennent au client et sont détruites
    avec lui.

    Attributes
    ----------
    _client_id : str
        Identifiant unique UUID4 généré automatiquement.
    _name : str
        Nom complet du client.
    _email : str
        Adresse e-mail du client.
    _phone : str
        Numéro de téléphone.
    _registered_on : datetime
        Date et heure d'inscription (UTC).
    _orders : List[Order]
        Liste des commandes passées par ce client (composition).
    """

    def __init__(self, name: str, email: str, phone: str) -> None:
        """Initialise un nouveau client.

        Parameters
        ----------
        name : str
            Nom complet du client.
        email : str
            Adresse e-mail.
        phone : str
            Numéro de téléphone.
        """
        self._client_id = str(uuid.uuid4())
        self._name = name
        self._email = email
        self._phone = phone
        self._registered_on = datetime.now(timezone.utc)
        self._orders: List[Order] = []

    # ── Propriétés (getters) ──────────────────────────────────────────

    @property
    def client_id(self) -> str:
        """Identifiant unique du client."""
        return self._client_id

    @property
    def name(self) -> str:
        """Nom complet du client."""
        return self._name

    @property
    def email(self) -> str:
        """Adresse e-mail du client."""
        return self._email

    @property
    def phone(self) -> str:
        """Numéro de téléphone du client."""
        return self._phone

    @property
    def registered_on(self) -> datetime:
        """Date et heure d'inscription."""
        return self._registered_on

    @property
    def orders(self) -> List["Order"]:
        """Liste des commandes passées par ce client (lecture seule)."""
        return list(self._orders)

    # ── Méthodes métier ───────────────────────────────────────────────

    def place_order(
        self,
        package: "Package",
        pickup_address: str,
        delivery_address: str,
        urgency: "UrgencyLevel",
    ) -> "Order":
        """Crée une nouvelle commande pour ce client.

        La commande est automatiquement ajoutée à la liste des commandes
        du client (relation de composition).

        Parameters
        ----------
        package : Package
            Colis à livrer.
        pickup_address : str
            Adresse de ramassage.
        delivery_address : str
            Adresse de livraison.
        urgency : UrgencyLevel
            Niveau d'urgence de la livraison.

        Returns
        -------
        Order
            La commande créée et rattachée au client.
        """
        # Import tardif pour éviter les dépendances circulaires
        from src.model.order import Order

        order = Order(
            client=self,
            package=package,
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            urgency=urgency,
        )
        self._orders.append(order)
        return order

    # ── Représentation ────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"Client(name={self._name!r}, email={self._email!r})"
