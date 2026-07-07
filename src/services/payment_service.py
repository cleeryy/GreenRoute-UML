"""Service de paiement GreenRoute — interface simulée avec l'API ToulousePay."""

from typing import Optional

from src.model.client import Client


class PaymentService:
    """Service de traitement des paiements simulant l'API externe ToulousePay.

    Dans une implémentation réelle, cette classe interrogerait l'API
    ToulousePay pour valider et traiter les transactions.
    """

    # Seuil de rejet simulé (à des fins de démonstration)
    _reject_threshold: Optional[float] = None

    @classmethod
    def set_reject_threshold(cls, amount: Optional[float]) -> None:
        """Configure un seuil au-dessus duquel les paiements sont rejetés (simulation).

        Parameters
        ----------
        amount : Optional[float]
            Montant seuil, ou None pour désactiver.
        """
        cls._reject_threshold = amount

    @staticmethod
    def process_payment(client: Client, amount: float) -> bool:
        """Traite un paiement pour un client.

        Simule l'appel à l'API ToulousePay. Retourne True si le
        paiement est accepté, False s'il est refusé.

        Parameters
        ----------
        client : Client
            Client effectuant le paiement.
        amount : float
            Montant à payer en euros.

        Returns
        -------
        bool
            True si le paiement est accepté, False sinon.
        """
        # Simulation : on vérifie le seuil de rejet
        if PaymentService._reject_threshold is not None and amount > PaymentService._reject_threshold:
            return False

        # Simulation : les paiements ≤ 1000 € sont toujours acceptés
        if amount > 1000.0:
            return False

        return True
