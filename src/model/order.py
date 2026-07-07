"""Module définissant la commande (Order) de la plateforme GreenRoute — classe centrale."""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from src.model.enums import OrderStatus, UrgencyLevel

if TYPE_CHECKING:
    from src.model.client import Client
    from src.model.package import Package
    from src.model.delivery_person import DeliveryPerson


class Order:
    """Commande de livraison — classe centrale du domaine GreenRoute.

    Une commande relie un client, un colis, et éventuellement un livreur.
    Elle suit un cycle de vie : A_ATTRIBUER → EN_COURS_D_ATTRIBUTION →
    EN_COURS_DE_LIVRAISON → LIVRE (ou VERROUILLEE_FRAUDE en cas de fraude).

    Attributes
    ----------
    _order_id : str
        Identifiant unique UUID4.
    _client : Client
        Client ayant passé la commande (many-to-one).
    _package : Package
        Colis à livrer (composition).
    _pickup_address : str
        Adresse de ramassage.
    _delivery_address : str
        Adresse de livraison.
    _urgency : UrgencyLevel
        Niveau d'urgence.
    _status : OrderStatus
        Statut actuel de la commande.
    _delivery_person : Optional[DeliveryPerson]
        Livreur assigné (nullable).
    _qr_code : Optional[str]
        Code QR unique pour le suivi.
    _total_cost : float
        Coût total calculé.
    _carbon_savings : float
        Émissions de CO₂ évitées en grammes.
    _created_at : datetime
        Date de création.
    _paid_at : Optional[datetime]
        Date de paiement.
    _delivered_at : Optional[datetime]
        Date de livraison effective.
    """

    def __init__(
        self,
        client: "Client",
        package: "Package",
        pickup_address: str,
        delivery_address: str,
        urgency: UrgencyLevel,
    ) -> None:
        """Initialise une nouvelle commande.

        Le statut démarre à A_ATTRIBUER et un code QR unique est généré.

        Parameters
        ----------
        client : Client
            Client expéditeur.
        package : Package
            Colis à livrer.
        pickup_address : str
            Adresse de ramassage.
        delivery_address : str
            Adresse de livraison.
        urgency : UrgencyLevel
            Niveau d'urgence.
        """
        self._order_id = str(uuid.uuid4())
        self._client = client
        self._package = package
        self._pickup_address = pickup_address
        self._delivery_address = delivery_address
        self._urgency = urgency
        self._status = OrderStatus.A_ATTRIBUER
        self._delivery_person: Optional[DeliveryPerson] = None
        self._qr_code = str(uuid.uuid4())  # code QR unique généré automatiquement
        self._total_cost = 0.0
        self._carbon_savings = 0.0
        self._created_at = datetime.now(timezone.utc)
        self._paid_at: Optional[datetime] = None
        self._delivered_at: Optional[datetime] = None

    # ── Propriétés (getters) ──────────────────────────────────────────

    @property
    def order_id(self) -> str:
        """Identifiant unique de la commande."""
        return self._order_id

    @property
    def client(self) -> "Client":
        """Client ayant passé la commande."""
        return self._client

    @property
    def package(self) -> "Package":
        """Colis à livrer."""
        return self._package

    @property
    def pickup_address(self) -> str:
        """Adresse de ramassage."""
        return self._pickup_address

    @property
    def delivery_address(self) -> str:
        """Adresse de livraison."""
        return self._delivery_address

    @property
    def urgency(self) -> UrgencyLevel:
        """Niveau d'urgence de la livraison."""
        return self._urgency

    @property
    def status(self) -> OrderStatus:
        """Statut actuel de la commande."""
        return self._status

    @property
    def delivery_person(self) -> Optional["DeliveryPerson"]:
        """Livreur assigné à la commande, ou None."""
        return self._delivery_person

    @property
    def qr_code(self) -> str:
        """Code QR unique de suivi."""
        return self._qr_code

    @property
    def total_cost(self) -> float:
        """Coût total de la livraison en euros."""
        return self._total_cost

    @total_cost.setter
    def total_cost(self, value: float) -> None:
        """Définit le coût total (utilisé par le service de tarification).

        Parameters
        ----------
        value : float
            Coût total en euros.
        """
        self._total_cost = value

    @property
    def carbon_savings(self) -> float:
        """Émissions de CO₂ évitées en grammes."""
        return self._carbon_savings

    @carbon_savings.setter
    def carbon_savings(self, value: float) -> None:
        """Définit les émissions de CO₂ évitées (utilisé par le service de tarification).

        Parameters
        ----------
        value : float
            Grammes de CO₂ évités.
        """
        self._carbon_savings = value

    @property
    def created_at(self) -> datetime:
        """Date et heure de création de la commande."""
        return self._created_at

    @property
    def paid_at(self) -> Optional[datetime]:
        """Date et heure du paiement, ou None."""
        return self._paid_at

    @paid_at.setter
    def paid_at(self, value: Optional[datetime]) -> None:
        """Définit la date de paiement.

        Parameters
        ----------
        value : Optional[datetime]
            Date de paiement.
        """
        self._paid_at = value

    @property
    def delivered_at(self) -> Optional[datetime]:
        """Date et heure de livraison effective, ou None."""
        return self._delivered_at

    # ── Méthodes métier ───────────────────────────────────────────────

    def assign_to(self, delivery_person: "DeliveryPerson") -> None:
        """Assigne un livreur à cette commande.

        Le statut passe à EN_COURS_D_ATTRIBUTION et le livreur est
        notifié via l'ajout dans sa liste de commandes assignées.

        Parameters
        ----------
        delivery_person : DeliveryPerson
            Livreur à assigner.
        """
        self._delivery_person = delivery_person
        self._status = OrderStatus.EN_COURS_D_ATTRIBUTION
        delivery_person._assigned_orders.append(self)

    def confirm_pickup(self) -> None:
        """Confirme le ramassage du colis par le livreur.

        Le statut passe à EN_COURS_DE_LIVRAISON et le livreur passe
        en état EN_TOURNEE.

        Raises
        ------
        ValueError
            Si aucun livreur n'est assigné.
        """
        if self._delivery_person is None:
            raise ValueError("Impossible de confirmer le ramassage : aucun livreur assigné.")
        self._status = OrderStatus.EN_COURS_DE_LIVRAISON
        self._delivery_person.set_on_tour()

    def confirm_delivery(self, qr_code: str) -> None:
        """Confirme la livraison après vérification du code QR.

        Si le code QR correspond, le statut passe à LIVRE et la date
        de livraison est enregistrée.

        Parameters
        ----------
        qr_code : str
            Code QR à vérifier.

        Raises
        ------
        ValueError
            Si le code QR ne correspond pas.
        """
        if qr_code != self._qr_code:
            raise ValueError(
                f"Code QR invalide : {qr_code!r} ne correspond pas "
                f"au code attendu {self._qr_code!r}."
            )
        self._status = OrderStatus.LIVRE
        self._delivered_at = datetime.now(timezone.utc)
        if self._delivery_person is not None:
            self._delivery_person.set_available()

    def mark_fraud(self) -> None:
        """Marque la commande comme frauduleuse.

        Le statut passe à VERROUILLEE_FRAUDE et la commande est bloquée.
        """
        self._status = OrderStatus.VERROUILLEE_FRAUDE

    # ── Représentation ────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"Order(id={self._order_id[:8]}..., "
            f"status={self._status.value}, "
            f"urgency={self._urgency.value})"
        )
